import requests
import json
from typing import Optional, Dict
from datetime import datetime

class JokeGenerator:
    """
    A random joke generator using the JokeAPI (https://jokeapi.dev/)
    Supports multiple joke types and can filter jokes by category.
    """
    
    BASE_URL = "https://v2.jokeapi.dev/joke"
    
    CATEGORIES = {
        "general": "General",
        "knock-knock": "Knock-knock",
        "programming": "Programming",
        "misc": "Miscellaneous"
    }
    
    JOKE_TYPES = ["single", "twopart"]
    
    def __init__(self):
        self.session = requests.Session()
        self.joke_history = []
    
    def get_random_joke(self, category: str = "any", joke_type: str = "any") -> Optional[Dict]:
        """
        Fetch a random joke from the API.
        
        Args:
            category: Joke category (general, knock-knock, programming, misc, any)
            joke_type: Type of joke (single, twopart, any)
            
        Returns:
            Dictionary containing joke data or None if request fails
        """
        try:
            # Validate inputs
            if category.lower() not in list(self.CATEGORIES.keys()) + ["any"]:
                print(f"Invalid category. Use: {', '.join(self.CATEGORIES.keys())}, or 'any'")
                return None
            
            if joke_type.lower() not in self.JOKE_TYPES + ["any"]:
                print(f"Invalid type. Use: {', '.join(self.JOKE_TYPES)}, or 'any'")
                return None
            
            # Build URL
            if category.lower() == "any":
                url = f"{self.BASE_URL}/Any"
            else:
                url = f"{self.BASE_URL}/{category}"
            
            # Add type parameter if specified
            if joke_type.lower() != "any":
                url += f"?type={joke_type}"
            
            # Fetch joke
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            joke_data = response.json()
            
            # Check if joke was found
            if joke_data.get("error"):
                print("No jokes found matching your criteria.")
                return None
            
            # Add metadata
            joke_data["fetched_at"] = datetime.now().isoformat()
            
            # Store in history
            self.joke_history.append(joke_data)
            
            return joke_data
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching joke: {e}")
            return None
        except json.JSONDecodeError:
            print("Error parsing joke response.")
            return None
    
    def format_joke(self, joke_data: Dict) -> str:
        """
        Format joke data for display.
        
        Args:
            joke_data: Dictionary containing joke information
            
        Returns:
            Formatted joke string
        """
        if not joke_data:
            return "No joke to display."
        
        output = []
        output.append(f"📖 Category: {joke_data.get('category', 'Unknown')}")
        
        if joke_data.get("type") == "single":
            output.append(f"\n{joke_data.get('joke', 'No joke found.')}")
        
        elif joke_data.get("type") == "twopart":
            output.append(f"\n🎭 Setup: {joke_data.get('setup', '')}")
            output.append(f"\n😂 Delivery: {joke_data.get('delivery', '')}")
        
        if joke_data.get("flags"):
            flags = [flag for flag, value in joke_data["flags"].items() if value]
            if flags:
                output.append(f"\n⚠️  Content warning(s): {', '.join(flags)}")
        
        return "\n".join(output)
    
    def get_joke_history(self) -> list:
        """Get all fetched jokes."""
        return self.joke_history
    
    def clear_history(self):
        """Clear the joke history."""
        self.joke_history = []
    
    def save_history(self, filename: str):
        """Save joke history to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.joke_history, f, indent=2)
        print(f"Joke history saved to {filename}")
    
    def get_multiple_jokes(self, count: int = 5, category: str = "any") -> list:
        """
        Fetch multiple jokes at once.
        
        Args:
            count: Number of jokes to fetch
            category: Joke category
            
        Returns:
            List of joke dictionaries
        """
        jokes = []
        for i in range(count):
            joke = self.get_random_joke(category)
            if joke:
                jokes.append(joke)
            if i < count - 1:
                # Small delay to avoid rate limiting
                import time
                time.sleep(0.5)
        return jokes


def main():
    """Main function to run the interactive joke generator."""
    print("=" * 60)
    print("🎭 Welcome to the Random Joke Generator! 🎭")
    print("=" * 60)
    print("\nCommands:")
    print("  /joke         - Get a random joke")
    print("  /joke <cat>   - Get a joke from category")
    print("  /categories   - Show available categories")
    print("  /types        - Show available joke types")
    print("  /multi <n>    - Get n random jokes")
    print("  /history      - Show all fetched jokes")
    print("  /save         - Save history to file")
    print("  /clear        - Clear history")
    print("  /exit         - Exit the program")
    print("\n" + "=" * 60 + "\n")
    
    generator = JokeGenerator()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split()
            command = parts[0].lower()
            
            if command == "/exit":
                print("Thanks for the laughs! 👋")
                break
            
            elif command == "/categories":
                print("\nAvailable categories:")
                for key, value in generator.CATEGORIES.items():
                    print(f"  - {key}: {value}")
                print()
            
            elif command == "/types":
                print("\nAvailable joke types:")
                for jtype in generator.JOKE_TYPES:
                    print(f"  - {jtype}")
                print()
            
            elif command == "/joke":
                category = parts[1].lower() if len(parts) > 1 else "any"
                joke = generator.get_random_joke(category)
                if joke:
                    print("\n" + generator.format_joke(joke) + "\n")
            
            elif command == "/multi":
                count = int(parts[1]) if len(parts) > 1 else 5
                print(f"\nFetching {count} jokes...\n")
                jokes = generator.get_multiple_jokes(count)
                for i, joke in enumerate(jokes, 1):
                    print(f"--- Joke {i} ---")
                    print(generator.format_joke(joke) + "\n")
            
            elif command == "/history":
                if not generator.joke_history:
                    print("\nNo jokes in history yet.\n")
                else:
                    print(f"\nShowing {len(generator.joke_history)} jokes in history:\n")
                    for i, joke in enumerate(generator.joke_history, 1):
                        print(f"--- Joke {i} ---")
                        print(generator.format_joke(joke) + "\n")
            
            elif command == "/save":
                filename = f"jokes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                generator.save_history(filename)
                print()
            
            elif command == "/clear":
                generator.clear_history()
                print("History cleared.\n")
            
            else:
                print("Unknown command. Type /exit to quit.\n")
        
        except ValueError:
            print("Invalid input. Please try again.\n")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
