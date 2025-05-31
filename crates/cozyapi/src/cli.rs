use clap::{Parser, Subcommand};

#[derive(Parser)]
#[command(name = "cozyapi")]
#[command(about = "Let AI agents interact with your API")]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    Mcp,
}

pub async fn run() {
    let cli = Cli::parse();

    match cli.command {
        Some(Commands::Mcp) => {
            cozyapi_mcp_server::run().await;
        }
        None => {
            crate::tauri::run();
        }
    }
}
