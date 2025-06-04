use clap::Parser;

#[derive(Parser)]
#[command(name = "cozyapi")]
#[command(about = "Let AI agents interact with your API")]
struct Cli {}

pub async fn run() {
    let _cli = Cli::parse();
    crate::tauri::run();
}
