use clap::{Parser, Subcommand};
use cozyapi_config::Config;

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
            let config = Config {
                db_dir: "".to_string(),
                db_name: "".to_string(),
            };
            cozyapi_mcp_server::run(config).await;
        }
        None => {
            let config = Config {
                db_dir: "".to_string(),
                db_name: "".to_string(),
            };
            crate::tauri::run(config);
        }
    }
}
