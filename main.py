# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "mcp",
#     "requests",
# ]
# ///
from contextlib import closing
from mcp.server.fastmcp import FastMCP
import sqlite3
import os
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cozyapi")

db_file = os.getenv("DATABASE_FILE", "data.db")
if db_file.startswith("~/"):
    db_file = os.path.expanduser(db_file)

logger.info(f"Use SQLite DB {db_file}")

# Pass lifespan to server
mcp = FastMCP("Cozy API")


# Add a tool to list API endpoints
@mcp.tool()
def list_endpoints() -> str:
    """List all available API endpoints from the database as a Markdown table"""
    try:
        with closing(sqlite3.connect(db_file)) as conn:
            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "select id, name, method, path, created_at, updated_at from endpoints"
                )
                rows = cursor.fetchall()

                # Create Markdown table
                table = "| Name | Method | Path |\n"
                table += "|------|--------|------|\n"

                for row in rows:
                    name = row[1] or ""
                    method = row[2] or ""
                    path = row[3] or ""
                    table += f"| {name} | {method} | {path} |\n"

                return table

    except Exception as e:
        logger.error(f"Database error executing query: {e}")
        raise


# Add a tool to request an endpoint by name
@mcp.tool()
def request_endpoint(name: str, data: str = "") -> str:
    """Request an endpoint by name. Load the endpoint from database and perform HTTP request.

    Args:
        name: The name of the endpoint to request
        data: Optional JSON data to send with the request (for POST, PUT, PATCH requests)

    Returns:
        JSON response from the endpoint
    """
    try:
        # Load endpoint from database
        with closing(sqlite3.connect(db_file)) as conn:
            conn.row_factory = sqlite3.Row
            with closing(conn.cursor()) as cursor:
                cursor.execute(
                    "select name, method, path from endpoints where name = ?", (name,)
                )
                row = cursor.fetchone()

                if not row:
                    return f"Error: Endpoint '{name}' not found in database"

                endpoint_name = row["name"]
                method = row["method"].upper()
                path = row["path"]

                # Construct full URL (assuming localhost for now)
                url = f"http://localhost:8000{path}"

                logger.info(f"Requesting {method} {url}")

                # Prepare request data
                json_data = None
                if data and method in ["POST", "PUT", "PATCH"]:
                    try:
                        json_data = json.loads(data)
                    except json.JSONDecodeError as e:
                        return f"Error: Invalid JSON data - {e}"

                # Make HTTP request
                response = requests.request(
                    method=method, url=url, json=json_data, timeout=30
                )

                # Format response
                result = {
                    "endpoint": endpoint_name,
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "headers": dict(response.headers),
                    "response": response.text,
                }

                # Try to parse response as JSON if possible
                try:
                    result["response"] = response.json()
                except (json.JSONDecodeError, requests.exceptions.JSONDecodeError):
                    pass  # Keep as text

                return json.dumps(result, indent=2)

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error: {e}")
        return f"Error: HTTP request failed - {e}"
    except Exception as e:
        logger.error(f"Error requesting endpoint: {e}")
        return f"Error: {e}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
