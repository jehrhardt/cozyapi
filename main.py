# server.py
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
from mcp.server.fastmcp import FastMCP
import sqlite3
import os

db_file = os.getenv("DATABASE_FILE", "foo.db")

# Pass lifespan to server
mcp = FastMCP("Cozy API", lifespan=app_lifespan)


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a tool to list API endpoints
@mcp.tool()
def list_endpoints() -> list[dict]:
    """List all available API endpoints from the database"""
    ctx = mcp.get_context()
    db = ctx.request_context.lifespan_context["db"]
    cursor = db.cursor()
    cursor.execute(
        "select id, name, method, path, created_at, updated_at from endpoints"
    )
    rows = cursor.fetchall()

    endpoints = []
    for row in rows:
        endpoints.append(
            {
                "id": row[0],
                "name": row[1],
                "method": row[2],
                "path": row[3],
                "created_at": row[4],
                "updated_at": row[5],
            }
        )

    return endpoints


def main():
    mcp.run()


if __name__ == "__main__":
    main()
