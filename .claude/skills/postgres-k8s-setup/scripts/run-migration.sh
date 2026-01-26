#!/bin/bash
# Run database schema migrations

set -e

NAMESPACE="postgres"
MIGRATIONS_DIR="./migrations"
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        --dir)
            MIGRATIONS_DIR="$2"
            shift 2
            ;;
        --file)
            MIGRATION_FILE="$2"
            shift 2
            ;;
        --rollback)
            ROLLBACK=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Get PostgreSQL connection details
DB_HOST="postgres.postgres.svc.cluster.local"
DB_PORT="5432"
DB_NAME=${DATABASE:-learnflow}
DB_USER=${POSTGRES_USER:-postgres}

# Get password from secret
PASSWORD=$(kubectl get secret postgres-credentials -n "$NAMESPACE" -o jsonpath='{.data.password}' | base64 -d 2>/dev/null || echo "")

if [ -z "$PASSWORD" ]; then
    echo "Error: Could not retrieve database password"
    echo "Ensure PostgreSQL is deployed first"
    exit 1
fi

export PGPASSWORD="$PASSWORD"

echo "Running migrations..."
echo "  Host: $DB_HOST"
echo "  Database: $DB_NAME"
echo "  Migrations directory: $MIGRATIONS_DIR"
echo ""

if [ "$ROLLBACK" = true ]; then
    echo "Rollback mode:"
    if [ -n "$MIGRATION_FILE" ]; then
        # Rollback specific migration
        BASE_NAME=$(basename "$MIGRATION_FILE" .up.sql)
        ROLLBACK_FILE="${MIGRATIONS_DIR}/${BASE_NAME}.down.sql"
        if [ -f "$ROLLBACK_FILE" ]; then
            echo "  Rolling back: $ROLLBACK_FILE"
            if [ "$DRY_RUN" = false ]; then
                psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$ROLLBACK_FILE"
            else
                echo "  [DRY RUN] Would execute: $ROLLBACK_FILE"
            fi
        else
            echo "  Error: Rollback file not found: $ROLLBACK_FILE"
            exit 1
        fi
    else
        echo "  Error: Must specify --file for rollback"
        exit 1
    fi
elif [ -n "$MIGRATION_FILE" ]; then
    echo "Running specific migration: $MIGRATION_FILE"
    if [ "$DRY_RUN" = false ]; then
        psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$MIGRATION_FILE"
    else
        echo "  [DRY RUN] Would execute: $MIGRATION_FILE"
    fi
else
    # Run all pending migrations
    echo "Running all pending migrations..."
    for migration in "$MIGRATIONS_DIR"/*.up.sql; do
        if [ -f "$migration" ]; then
            echo "  Applying: $(basename "$migration")"
            if [ "$DRY_RUN" = false ]; then
                psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$migration"
            else
                echo "  [DRY RUN] Would execute: $migration"
            fi
        fi
    done
fi

echo ""
echo "Migrations completed!"
