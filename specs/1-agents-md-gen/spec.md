# Feature Specification: Agents MD Generator

**Feature Branch**: `1-agents-md-gen`
**Created**: 2025-01-26
**Status**: Draft
**Input**: Create a skill that generates AGENTS.md files for code repositories

## User Scenarios & Testing

### User Story 1 - Auto-generate Repository Documentation (Priority: P1)

An AI coding agent needs to understand a new codebase structure and conventions. The agent uses the agents-md-gen skill to scan the repository and generate a comprehensive AGENTS.md file that documents the project structure, coding conventions, and guidelines.

**Why this priority**: This is the foundation skill - without it, agents cannot effectively understand or work with new codebases. This enables all subsequent agentic development.

**Independent Test**: Can be tested by running the skill against any Git repository and verifying a valid AGENTS.md file is created with accurate project information.

**Acceptance Scenarios**:

1. **Given** a repository with source code, **When** the skill is invoked, **Then** an AGENTS.md file is created at the repository root
2. **Given** an existing AGENTS.md file, **When** the skill runs, **Then** it offers to update or regenerate the file
3. **Given** a repository with multiple languages, **When** the skill scans, **Then** it detects and documents all programming languages used

---

### User Story 2 - Detect Project Conventions (Priority: P2)

The skill analyzes the codebase to identify and document coding conventions, patterns, and architectural decisions that AI agents should follow when working with the code.

**Why this priority**: Helps agents write code that matches the existing style and patterns, reducing review cycles and improving code quality.

**Independent Test**: Run against a repository with established patterns (e.g., React components, API routes) and verify the generated documentation accurately describes the patterns.

**Acceptance Scenarios**:

1. **Given** a repository with consistent naming conventions, **When** the skill analyzes, **Then** it documents the convention (e.g., camelCase for variables, PascalCase for components)
2. **Given** a repository using specific frameworks, **When** the skill scans, **Then** it identifies and documents the frameworks and their versions
3. **Given** a repository with test files, **When** the skill analyzes, **Then** it documents the testing approach and patterns used

---

### User Story 3 - Customizable Output Sections (Priority: P3)

Users can specify which sections to include in the generated AGENTS.md file, allowing customization based on project needs.

**Why this priority**: Provides flexibility for different project types while maintaining a sensible default.

**Independent Test**: Run with custom section flags and verify only requested sections are included in output.

**Acceptance Scenarios**:

1. **Given** a user requests specific sections only, **When** the skill generates, **Then** only those sections appear in the output
2. **Given** no section preferences, **When** the skill generates, **Then** all default sections are included

---

### Edge Cases

- What happens when a repository has no source code (only docs/configs)?
- How does the system handle extremely large repositories (10,000+ files)?
- What happens when the repository is not a Git repo?
- How does the system handle monorepos with multiple projects?
- What happens when directory names contain special characters or spaces?

## Requirements

### Functional Requirements

- **FR-001**: System MUST scan the entire repository directory structure
- **FR-002**: System MUST detect all programming languages used in the codebase
- **FR-003**: System MUST identify common frameworks and libraries from configuration files
- **FR-004**: System MUST analyze code patterns to determine naming conventions
- **FR-005**: System MUST generate a valid AGENTS.md file at repository root
- **FR-006**: System MUST preserve existing AGENTS.md content when updating
- **FR-007**: System MUST complete scanning within 30 seconds for repositories up to 1,000 files
- **FR-008**: System MUST handle symbolic links without following circular references
- **FR-009**: System MUST exclude common non-source directories (node_modules, .git, build, dist)
- **FR-010**: System MUST output in Markdown format compatible with Agent Skills specification

### Key Entities

- **Repository**: The codebase being analyzed, including all source files and configuration
- **AGENTS.md**: The generated documentation file following Agent Skills specification format
- **Code Pattern**: Repeated code structures indicating conventions (naming, architectural, etc.)
- **Framework**: Detected libraries or frameworks used in the project

## Success Criteria

### Measurable Outcomes

- **SC-001**: Generated AGENTS.md file accurately reflects 95% of repository structure
- **SC-002**: Skill completes scanning and generation in under 30 seconds for 1,000-file repositories
- **SC-003**: AI agents using generated AGENTS.md reduce context-seeking questions by 70%
- **SC-004**: Generated documentation includes all major languages and frameworks used
- **SC-005**: Skill uses less than 5,000 tokens of context when loaded by AI agents

## Assumptions

- Repository has readable file system permissions
- Common build and dependency directories follow standard naming (node_modules, target, etc.)
- Code follows consistent patterns (not randomly styled)
- Git repository info is available if running in a Git repo

## Out of Scope

- Code quality analysis or linting
- Security vulnerability scanning
- Automatic code fixes or refactoring
- Generating documentation other than AGENTS.md
- Analyzing binary files or compiled code
