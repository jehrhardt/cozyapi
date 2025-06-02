# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

**Development:**
- `mise run dev:app` - Start the Tauri application in development mode
- `mise run dev:mcp` - Start the MCP server with inspector
- `mise setup` or `npm install` - Install dependencies

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
  - `cozyapi_mcp_server` - Model Context Protocol server implementation
- Uses SQLite database via tauri-plugin-sql
- CLI supports both GUI mode (default) and MCP server mode (`cargo run -- mcp`)

**Key Integration Points:**
- Main entry point routes between Tauri GUI and MCP server via CLI subcommands
- MCP server uses rmcp library for Model Context Protocol implementation
- Database operations handled through Tauri's SQL plugin
- Frontend communicates with Rust backend via Tauri's IPC layer

**Development Setup:**
- Uses mise for tool management (Rust toolchain, Node.js)
- Cargo workspace manages multiple Rust crates
- Vite handles frontend bundling and HMR