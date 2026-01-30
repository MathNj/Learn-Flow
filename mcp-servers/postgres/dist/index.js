#!/usr/bin/env node
/**
 * LearnFlow PostgreSQL MCP Server
 *
 * Provides MCP tools for querying LearnFlow database:
 * - List users, modules, topics, exercises, quizzes
 * - Get student progress and mastery levels
 * - Query code submissions and results
 * - Check struggle patterns and alerts
 *
 * Token Efficiency: Queries return aggregated summaries, not full datasets
 * Target: >80% token savings vs direct MCP data loading
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { Pool } from "pg";
// Database connection
const pool = new Pool({
    host: process.env.PGHOST || "localhost",
    port: parseInt(process.env.PGPORT || "5432"),
    database: process.env.PGDATABASE || "learnflow",
    user: process.env.PGUSER || "postgres",
    password: process.env.PGPASSWORD || "postgres",
});
/**
 * Get student progress summary (aggregated, not full data)
 * Token Efficient: Returns counts and averages instead of all records
 */
async function getProgressSummary(studentId) {
    const result = await pool.query(`SELECT
      COUNT(DISTINCT topic_id) as total_topics,
      COUNT(CASE WHEN mastery_score >= 90 THEN 1 END) as mastered_topics,
      AVG(mastery_score) as avg_mastery,
      SUM(streak_days) as total_streak_days
    FROM progress
    WHERE user_id = $1
    GROUP BY user_id`, [studentId]);
    return result.rows[0] || { total_topics: 0, mastered_topics: 0, avg_mastery: 0, total_streak_days: 0 };
}
/**
 * Get user with their role (minimal data returned)
 */
async function getUserById(userId) {
    const result = await pool.query(`SELECT id, email, full_name, role, is_active, created_at
     FROM users WHERE id = $1`, [userId]);
    return result.rows[0];
}
/**
 * Get module topics summary (aggregated)
 */
async function getModuleTopics(moduleId) {
    const result = await pool.query(`SELECT
      t.id,
      t.title,
      t.difficulty,
      COUNT(DISTINCT e.id) as exercise_count,
      COUNT(DISTINCT q.id) as quiz_count,
      AVG(p.mastery_score) as avg_mastery
     FROM topics t
     LEFT JOIN exercises e ON e.topic_id = t.id
     LEFT JOIN quizzes q ON q.topic_id = t.id
     LEFT JOIN progress p ON p.topic_id = t.id
     WHERE t.module_id = $1
     GROUP BY t.id
     ORDER BY t.order_index`, [moduleId]);
    return result.rows;
}
/**
 * Get struggling students (aggregated summary)
 */
async function getStrugglingStudents(threshold = 3) {
    const result = await pool.query(`SELECT
      u.id,
      u.email,
      u.full_name,
      COUNT(sp.id) as struggle_count,
      MAX(sp.occurrence_count) as max_occurrences
     FROM users u
     JOIN struggle_patterns sp ON sp.user_id = u.id
     WHERE sp.resolved_at IS NULL
     GROUP BY u.id
     HAVING COUNT(sp.id) >= $1
     ORDER BY struggle_count DESC`, [threshold]);
    return result.rows;
}
/**
 * Get recent code submissions (summary only)
 */
async function getRecentSubmissions(limit = 10) {
    const result = await pool.query(`SELECT
      s.id,
      s.user_id,
      s.exercise_id,
      s.score,
      s.submitted_at,
      e.title as exercise_title
     FROM submissions s
     JOIN exercises e ON e.id = s.exercise_id
     ORDER BY s.submitted_at DESC
     LIMIT $1`, [limit]);
    return result.rows;
}
// Create MCP server
const server = new Server({
    name: "learnflow-postgres",
    version: "1.0.0",
}, {
    capabilities: {
        resources: {},
        tools: {},
    },
});
// Register MCP tools
server.setRequestHandler(async (request) => {
    const { method, params } = request;
    if (method === "tools/list") {
        // List available tools
        return {
            tools: [
                {
                    name: "get_user_by_id",
                    description: "Get user by ID with minimal fields (id, email, role, is_active)",
                    inputSchema: {
                        type: "object",
                        properties: {
                            userId: {
                                type: "string",
                                description: "User UUID",
                            },
                        },
                        required: ["userId"],
                    },
                },
                {
                    name: "get_progress_summary",
                    description: "Get student progress summary (total topics, mastered topics, avg mastery, streak days)",
                    inputSchema: {
                        type: "object",
                        properties: {
                            studentId: {
                                type: "string",
                                description: "Student UUID",
                            },
                        },
                        required: ["studentId"],
                    },
                },
                {
                    name: "get_module_topics",
                    description: "Get module topics with exercise/quiz counts and average mastery",
                    inputSchema: {
                        type: "object",
                        properties: {
                            moduleId: {
                                type: "string",
                                description: "Module UUID",
                            },
                        },
                        required: ["moduleId"],
                    },
                },
                {
                    name: "get_struggling_students",
                    description: "Get list of struggling students with struggle counts",
                    inputSchema: {
                        type: "object",
                        properties: {
                            threshold: {
                                type: "number",
                                description: "Minimum struggle patterns (default: 3)",
                            },
                        },
                        required: [],
                    },
                },
                {
                    name: "get_recent_submissions",
                    description: "Get recent code submissions with scores",
                    inputSchema: {
                        type: "object",
                        properties: {
                            limit: {
                                type: "number",
                                description: "Number of submissions (default: 10)",
                            },
                        },
                        required: [],
                    },
                },
            ],
        };
    }
    if (method === "tools/call") {
        const { name, arguments } = params;
        try {
            switch (name) {
                case "get_user_by_id":
                    const user = await getUserById(arguments.userId);
                    return {
                        content: [{
                                type: "text",
                                text: JSON.stringify(user, null, 2),
                            }],
                    };
                case "get_progress_summary":
                    const summary = await getProgressSummary(arguments.studentId);
                    return {
                        content: [{
                                type: "text",
                                text: JSON.stringify(summary, null, 2),
                            }],
                    };
                case "get_module_topics":
                    const topics = await getModuleTopics(arguments.moduleId);
                    return {
                        content: [{
                                type: "text",
                                text: JSON.stringify(topics, null, 2),
                            }],
                    };
                case "get_struggling_students":
                    const struggling = await getStrugglingStudents(arguments.threshold || 3);
                    return {
                        content: [{
                                type: "text",
                                text: JSON.stringify(struggling, null, 2),
                            }],
                    };
                case "get_recent_submissions":
                    const submissions = await getRecentSubmissions(arguments.limit || 10);
                    return {
                        content: [{
                                type: "text",
                                text: JSON.stringify(submissions, null, 2),
                            }],
                    };
                default:
                    throw new Error(`Unknown tool: ${name}`);
            }
        }
        catch (error) {
            return {
                content: [{
                        type: "text",
                        text: JSON.stringify({
                            error: error instanceof Error ? error.message : String(error),
                        }),
                    }],
                isError: true,
            };
        }
    }
    return {};
});
async function main() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("LearnFlow PostgreSQL MCP server running on stdio");
}
main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
});
