mod mcp;

use cozyapi_config::Config;
use mcp::Server;
use rmcp::{ServiceExt, transport::stdio};

pub async fn run(_config: Config) {
    let service = Server::new()
        .serve(stdio())
        .await
        .expect("Failed to start service");

    service.waiting().await.expect("Service failed");
}
