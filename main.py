import os
import json
from datetime import datetime
from anthropic import Anthropic

class AIAssistant:
    """
    A Claude-like AI Assistant that maintains conversation context
    and provides intelligent responses across various tasks.
    """
    
    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.model = model
        self.conversation_history = []
        self.system_prompt = """You are Claude, a helpful, harmless, and honest AI assistant created by Anthropic. 
You are intelligent, curious, and thoughtful. You provide clear, accurate, and nuanced responses.
You think step-by-step about complex problems and explain your reasoning.
You are willing to admit uncertainty and ask clarifying questions when needed."""
    
    def chat(self, user_message: str) -> str:
        """
        Send a message to the AI and get a response while maintaining conversation context.
        
        Args:
            user_message: The user's input message
            
        Returns:
            The AI's response
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Claude
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )
        
        # Extract response text
        assistant_message = response.content[0].text
        
        # Add assistant response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> list:
        """Get the current conversation history."""
        return self.conversation_history
    
    def save_conversation(self, filename: str):
        """Save the conversation to a JSON file."""
        with open(filename, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "model": self.model,
                "conversation": self.conversation_history
            }, f, indent=2)
    
    def load_conversation(self, filename: str):
        """Load a conversation from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
            self.conversation_history = data.get("conversation", [])
            self.model = data.get("model", self.model)


def main():
    """Main function to run the interactive AI assistant."""
    print("=" * 60)
    print("Welcome to Claude AI Assistant")
    print("=" * 60)
    print("\nType your messages below. Commands:")
    print("  /clear  - Clear conversation history")
    print("  /save   - Save conversation to file")
    print("  /load   - Load conversation from file")
    print("  /exit   - Exit the program")
    print("\n" + "=" * 60 + "\n")
    
    assistant = AIAssistant()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() == "/exit":
                print("Goodbye!")
                break
            elif user_input.lower() == "/clear":
                assistant.clear_history()
                print("Conversation history cleared.\n")
                continue
            elif user_input.lower() == "/save":
                filename = f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                assistant.save_conversation(filename)
                print(f"Conversation saved to {filename}\n")
                continue
            elif user_input.lower() == "/load":
                filename = input("Enter filename to load: ").strip()
                try:
                    assistant.load_conversation(filename)
                    print(f"Conversation loaded from {filename}\n")
                except FileNotFoundError:
                    print(f"File {filename} not found.\n")
                continue
            
            # Get AI response
            print("\nClaude: ", end="", flush=True)
            response = assistant.chat(user_input)
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
