# --- Modified AddAgent Server Code ---
from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AddAgent(A2AServer):
    """
    An agent that expects a single text message containing two numbers
    separated by a comma (e.g., "5,2") and returns their sum.
    """

    # MODIFIED: handle_message now accepts ONE message argument
    def handle_message(self, message: Message):
        logging.info(f"Received message: {message}")

        # Check if it's a text message
        if not (hasattr(message, 'content') and message.content.type == "text"):
            warning_msg = "Error: Input must be a text message."
            logging.warning(warning_msg)
            return Message(
                content=TextContent(text=warning_msg),
                role=MessageRole.AGENT,
                parent_message_id=getattr(message, 'message_id', None),
                conversation_id=getattr(message, 'conversation_id', None)
            )

        # Get the text and try to parse it
        text_input = message.content.text
        logging.info(f"Attempting to parse text: '{text_input}'")

        try:
            # Split the text by a comma (or another delimiter you choose)
            parts = text_input.split(',')
            if len(parts) != 2:
                raise ValueError("Input text must contain exactly two numbers separated by a comma.")

            # Attempt conversion to float
            num1 = float(parts[0].strip()) # Use strip() to remove leading/trailing whitespace
            num2 = float(parts[1].strip())

            # Perform the addition
            result = num1 + num2
            response_text = f"The sum of {num1} and {num2} is: {result}"
            logging.info(f"Calculation successful: {response_text}")

            # Return the result message
            return Message(
                content=TextContent(text=response_text),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )

        except ValueError as e:
            # Handle cases where splitting fails or text cannot be converted
            error_msg = f"Error processing input '{text_input}': {e}"
            logging.error(error_msg)
            return Message(
                content=TextContent(text=error_msg),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        except Exception as e:
             error_msg = f"An unexpected error occurred: {e}"
             logging.exception(error_msg) # Log full traceback
             return Message(
                 content=TextContent(text="An internal server error occurred."),
                 role=MessageRole.AGENT,
                 parent_message_id=message.message_id,
                 conversation_id=message.conversation_id
             )

# Run the server (no changes needed here)
if __name__ == "__main__":
    agent = AddAgent()
    print("Starting AddAgent server...")
    # Now the handle_message signature matches what run_server expects
    run_server(agent, host="localhost", port=5000)

