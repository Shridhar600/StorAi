import argparse
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Import Memory explicitly for the test mode
from memory.models import Memory
from memory.storage import MemoryStore
from generation.tweet_generator import TweetGenerator, TweetGenerationError
from generation.llm_clients import OpenRouterClient
# Only import TwitterClient if we're actually tweeting
from twitter.api_client import TwitterClient


def setup_argument_parser():
    """Set up command line arguments"""
    parser = argparse.ArgumentParser(description='AI Intern Twitter Bot')
    parser.add_argument(
        '--dry-run', 
        action='store_true',
        help='Generate tweet but do not post to Twitter'
    )
    parser.add_argument(
        '--add-milestone', 
        action='store_true',
        help='Add current tweet as an important milestone'
    )
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Run in test mode without requiring Twitter credentials'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='Clear all memories and start fresh'
    )
    parser.add_argument(
        '--view-memories',
        action='store_true',
        help='View all stored memories without generating new tweet'
    )
    parser.add_argument(
        '--memory-file',
        type=str,
        help='Path to the memory file (optional)'
    )
    return parser


def run_bot(dry_run=False, is_milestone=False, test_mode=False, memory_file=None, twitter_client=None) -> str: 
    """Run the main bot process"""
    # Initialize components
    memory_store = MemoryStore(file_path=memory_file)
    llm_client = OpenRouterClient() #Change this according to your LLM client
    tweet_generator = TweetGenerator(memory_store, llm_client) #my tweet generator obj

    # Generating tweet now
    try:
        tweet = tweet_generator.generate_tweet()
        print(f"\n----------- Generated Tweet -----------")
        print(f"{tweet}")
        print(f"--------------------------------------\n")

        # Character count check
        print(f"Character count: {len(tweet)}/280")

        # If this is a milestone, update the importance
        if is_milestone:
            # Create memory with higher importance
            memory = Memory(
                text=tweet,
                timestamp=datetime.now(),
                importance=3.0,  # Milestone importance
                category="milestone"
            )
            memory_store.save_memory(memory)
            print("Saved as milestone memory")
        else:
            # Store normal memory
            memory = Memory(
                text=tweet,
                timestamp=datetime.now(),
                importance=1.0,
                category="daily"
            )
            memory_store.save_memory(memory)
            print("Saved as normal memory")

        # Post to Twitter if not a dry run or test mode
        if not dry_run and not test_mode:
            if twitter_client is None:
                twitter_client = TwitterClient()
            tweet_id = twitter_client.post_tweet(tweet)
            if tweet_id:
                print(f"Successfully posted to Twitter with ID: {tweet_id}")
            else:
                print("Failed to post to Twitter")
        else:
            print("Not posting to Twitter - running in dry run or test mode")

        return tweet
    except TweetGenerationError as e:
        print(f"Error: {e}")
        # Handle the error, possibly exiting or returning a default value
        return None

#use with caution
def reset_memories():
    """Clear all memories and start fresh"""
    from config.settings import MEMORY_FILE

    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
        print(f"Memory file deleted: {MEMORY_FILE}")
    else:
        print(f"No memory file found at {MEMORY_FILE}")

    # Create empty memories file
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, 'w') as f:
        json.dump([], f)
    print("Created new empty memories file")


def view_memories():
    """View all stored memories"""
    memory_store = MemoryStore()
    memories = sorted(memory_store.memories, key=lambda x: x.timestamp)

    if not memories:
        print("No memories stored yet.")
        return

    print(f"\n===== All Memories ({len(memories)}) =====")
    for i, memory in enumerate(memories):
        print(f"\n[{i+1}] {memory.timestamp.strftime('%Y-%m-%d %H:%M')} - Importance: {memory.importance}")
        print(f"Category: {memory.category}")
        print(f"Text: {memory.text}")
    print("\n===================================")



if __name__ == "__main__":
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    if args.reset:
        reset_memories()
        print("All memories have been reset.")
        exit(0)

    # Handle view memories if requested
    if args.view_memories:
        view_memories()
        exit(0)

    # Run the bot
    tweet = run_bot(
        dry_run=args.dry_run,
        is_milestone=args.add_milestone,
        test_mode=args.test_mode,
        memory_file=args.memory_file
    )
