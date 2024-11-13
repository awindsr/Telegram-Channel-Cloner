from telethon import TelegramClient
import asyncio
import time
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import datetime
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

# Channel IDs
SOURCE_CHANNEL = int(os.getenv("SOURCE_CHANNEL"))
DESTINATION_CHANNEL = int(os.getenv("DESTINATION_CHANNEL"))

# Delay between forwards (in seconds)
COOLDOWN = 2

# File to store progress
PROGRESS_FILE = 'forward_progress.json'

def save_progress(last_message_id, total_messages):
    """Save the progress to a file"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump({
            'last_message_id': last_message_id,
            'total_messages': total_messages
        }, f)

def load_progress():
    """Load the progress from file"""
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading progress file: {e}")
    return None

async def get_all_messages(client, channel):
    """Fetch all messages from the channel and return as a list"""
    messages = []
    message_count = 0
    
    print("Fetching messages from source channel...")
    async for message in client.iter_messages(channel, reverse=True):
        messages.append(message)
        message_count += 1
        if message_count % 100 == 0:
            print(f"Fetched {message_count} messages so far...")
    
    return messages

async def main():
    # Initialize the client
    client = TelegramClient('session_name', API_ID, API_HASH)
    await client.start(phone=PHONE_NUMBER)
    
    print("Client Created")
    
    try:
        # Get all messages first
        messages = await get_all_messages(client, SOURCE_CHANNEL)
        total_messages = len(messages)
        
        print(f"\nFetching completed. Total messages found: {total_messages}")
        
        # Load previous progress if exists
        progress = load_progress()
        start_index = 0
        
        if progress:
            # Find the index of the last forwarded message
            for i, msg in enumerate(messages):
                if msg.id == progress['last_message_id']:
                    start_index = i + 1
                    print(f"\nResuming from message {start_index}/{total_messages}")
                    break
        
        if start_index >= total_messages:
            print("All messages have already been forwarded!")
            return
        
        print("\nStarting forward process...")
        
        # Forward messages with progress tracking
        for index, message in enumerate(messages[start_index:], start_index + 1):
            try:
                # Forward the message
                await client.forward_messages(
                    entity=DESTINATION_CHANNEL,
                    messages=message
                )
                
                # Calculate percentage
                percentage = (index / total_messages) * 100
                
                # Print progress
                print(f"Progress: {index}/{total_messages} ({percentage:.1f}%) - Message ID: {message.id}")
                
                # Save progress after each successful forward
                save_progress(message.id, total_messages)
                
                # Wait for cooldown period
                await asyncio.sleep(COOLDOWN)
                
            except Exception as e:
                print(f"Error forwarding message {message.id}: {str(e)}")
                continue
        
        print("\nForwarding completed!")
        print(f"Successfully processed all messages")
        
        # Clean up progress file after successful completion
        if os.path.exists(PROGRESS_FILE):
            os.remove(PROGRESS_FILE)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    finally:
        await client.disconnect()

if __name__ == "__main__":
    # Run the async function
    asyncio.run(main())
