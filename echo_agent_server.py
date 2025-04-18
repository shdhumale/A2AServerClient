from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server

class EchoAgent(A2AServer):
    """A simple agent that echoes back messages with a prefix."""
    
    def handle_message(self, message):
        if message.content.type == "text":
            return Message(
                content=TextContent(text=f"Echo: {message.content.text}"),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
# Run the server
if __name__ == "__main__":
    agent = EchoAgent()
    run_server(agent, host="localhost", port=5000)