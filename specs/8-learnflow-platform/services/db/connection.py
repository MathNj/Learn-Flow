"""
Database connection pool management for LearnFlow services.

This module provides async PostgreSQL connection pooling using asyncpg.
"""

import os
from typing import AsyncGenerator, Optional

import asyncpg
from structlog import get_logger

logger = get_logger(__name__)


class DatabasePool:
    """Async PostgreSQL connection pool manager."""

    _pool: Optional[asyncpg.Pool] = None

    @classmethod
    async def initialize(
        cls,
        dsn: Optional[str] = None,
        min_size: int = 10,
        max_size: int = 100,
        command_timeout: int = 60,
    ) -> asyncpg.Pool:
        """
        Initialize the database connection pool.

        Args:
            dsn: Database connection string (default: from DATABASE_URL env var)
            min_size: Minimum number of connections in the pool
            max_size: Maximum number of connections in the pool
            command_timeout: Default command timeout in seconds

        Returns:
            asyncpg.Pool: The connection pool

        Raises:
            ValueError: If DSN is not provided and DATABASE_URL is not set
            asyncpg.PostgresError: If connection fails
        """
        if cls._pool is not None:
            logger.info("Database pool already initialized")
            return cls._pool

        if dsn is None:
            dsn = os.getenv("DATABASE_URL")
            if not dsn:
                raise ValueError(
                    "Database DSN must be provided via dsn parameter or DATABASE_URL env var"
                )

        logger.info(
            "Initializing database pool",
            dsn=dsn.split("@")[-1] if "@" in dsn else "localhost",  # Log host only
            min_size=min_size,
            max_size=max_size,
        )

        try:
            cls._pool = await asyncpg.create_pool(
                dsn,
                min_size=min_size,
                max_size=max_size,
                command_timeout=command_timeout,
                # Connection settings
                server_settings={"application_name": "learnflow"},
                # Retry settings
                retry=True,
            )

            logger.info("Database pool initialized successfully")
            return cls._pool

        except asyncpg.PostgresError as e:
            logger.error("Failed to initialize database pool", error=str(e))
            raise

    @classmethod
    async def close(cls) -> None:
        """Close the database connection pool."""
        if cls._pool is None:
            logger.warning("Database pool not initialized, nothing to close")
            return

        logger.info("Closing database pool")
        await cls._pool.close()
        cls._pool = None
        logger.info("Database pool closed")

    @classmethod
    async def get_connection(cls) -> asyncpg.Connection:
        """
        Get a connection from the pool.

        Returns:
            asyncpg.Connection: A database connection

        Raises:
            RuntimeError: If pool is not initialized
        """
        if cls._pool is None:
            raise RuntimeError(
                "Database pool not initialized. Call DatabasePool.initialize() first."
            )

        return await cls._pool.acquire()

    @classmethod
    async def release_connection(cls, connection: asyncpg.Connection) -> None:
        """
        Release a connection back to the pool.

        Args:
            connection: The connection to release
        """
        if cls._pool is None:
            logger.warning("Database pool not initialized, cannot release connection")
            return

        await cls._pool.release(connection)

    @classmethod
    async def execute(
        cls, query: str, *args, timeout: Optional[float] = None
    ) -> str:
        """
        Execute a SQL query that doesn't return data (INSERT, UPDATE, DELETE).

        Args:
            query: SQL query with placeholders ($1, $2, etc.)
            *args: Query arguments
            timeout: Query timeout in seconds

        Returns:
            str: Status message from PostgreSQL
        """
        async with cls._pool.acquire() as connection:
            return await connection.execute(query, *args, timeout=timeout)

    @classmethod
    async def fetch(
        cls, query: str, *args, timeout: Optional[float] = None
    ) -> list[asyncpg.Record]:
        """
        Execute a SQL query and return all rows.

        Args:
            query: SQL query with placeholders ($1, $2, etc.)
            *args: Query arguments
            timeout: Query timeout in seconds

        Returns:
            list[asyncpg.Record]: Query results
        """
        async with cls._pool.acquire() as connection:
            return await connection.fetch(query, *args, timeout=timeout)

    @classmethod
    async def fetchone(
        cls, query: str, *args, timeout: Optional[float] = None
    ) -> Optional[asyncpg.Record]:
        """
        Execute a SQL query and return the first row or None.

        Args:
            query: SQL query with placeholders ($1, $2, etc.)
            *args: Query arguments
            timeout: Query timeout in seconds

        Returns:
            Optional[asyncpg.Record]: First row or None
        """
        async with cls._pool.acquire() as connection:
            return await connection.fetchrow(query, *args, timeout=timeout)

    @classmethod
    async def fetchval(
        cls,
        query: str,
        *args,
        column: int = 0,
        timeout: Optional[float] = None,
    ) -> Optional[Any]:
        """
        Execute a SQL query and return a single value from the first row.

        Args:
            query: SQL query with placeholders ($1, $2, etc.)
            *args: Query arguments
            column: Column index to return (default: 0)
            timeout: Query timeout in seconds

        Returns:
            Optional[Any]: Column value or None
        """
        async with cls._pool.acquire() as connection:
            return await connection.fetchval(query, *args, column=column, timeout=timeout)

    @classmethod
    async def transaction(cls) -> AsyncGenerator[asyncpg.Connection, None]:
        """
        Execute a transaction block.

        Yields:
            asyncpg.Connection: Connection within transaction context
        """
        async with cls._pool.acquire() as connection:
            async with connection.transaction():
                yield connection


async def check_database_health() -> bool:
    """
    Check if database connection is healthy.

    Returns:
        bool: True if database is reachable, False otherwise
    """
    try:
        result = await cls.fetchval("SELECT 1")
        return result == 1
    except Exception as e:
        logger.error("Database health check failed", error=str(e))
        return False
