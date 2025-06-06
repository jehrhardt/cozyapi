# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

**Development:**
- `mise run dev:app` - Start the Tauri application in development mode
- `mise run dev:mcp` - Start the MCP server with inspector
- `mise install && npm install && uv sync` - Install all dependencies

**Build and Test:**
- `npm run build` - Build the frontend
- `cargo build` - Build the Rust workspace
- `cargo tauri build` - Build the complete Tauri application

## Architecture Overview

This is a hybrid Tauri desktop application that combines:

**Frontend (SolidJS + Vite):**
- SolidJS framework with TypeScript
- Tailwind CSS for styling
- Vite dev server on port 1420

**Backend (Rust):**
- Workspace with two main crates:
  - `cozyapi` - Main Tauri application and CLI
  - `config` - Configuration utilities
- Uses SQLite database via tauri-plugin-sql
- CLI supports GUI mode via Tauri

**Backend (Python MCP Server):**
- Simple MCP server implementation in `main.py` using FastMCP
- Provides tools for basic operations (addition example)
- Supports dynamic greeting resources
- Run with `mise run dev:mcp`

**Key Integration Points:**
- Database operations handled through Tauri's SQL plugin
- Frontend communicates with Rust backend via Tauri's IPC layer

**Development Setup:**
- Uses mise for tool management (Rust toolchain, Node.js)
- Cargo workspace manages multiple Rust crates
- Vite handles frontend bundling and HMR

## Code Conventions

**SQL:**
- Use lowercase for all SQL keywords and identifiers

**Python Dependencies:**
- Use `uv add <package>` to add Python libraries as dependencies to the project