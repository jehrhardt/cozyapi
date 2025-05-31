use rmcp::{ServerHandler, model::*, schemars, tool};
use serde::Deserialize;

#[derive(Clone)]
pub(crate) struct Server {}

#[derive(Debug, Deserialize, schemars::JsonSchema)]
struct SumRequest {
    a: i32,
    b: i32,
}

#[tool(tool_box)]
impl Server {
    pub(crate) fn new() -> Self {
        Self {}
    }

    #[tool(description = "Calculate the sum of two numbers")]
    async fn add(&self, #[tool(aggr)] SumRequest { a, b }: SumRequest) -> String {
        (a + b).to_string()
    }
}

#[tool(tool_box)]
impl ServerHandler for Server {
    fn get_info(&self) -> ServerInfo {
        ServerInfo {
            server_info: Implementation {
                name: "Cozy API".to_string(),
                version: "0.1.0".to_string(),
            },
            instructions: Some("Let AI agents interact with your API".into()),
            capabilities: ServerCapabilities::builder()
                .enable_logging()
                .enable_tools()
                .build(),
            ..Default::default()
        }
    }
}
