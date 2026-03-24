from telethon import TelegramClient, events # pip install telethon
import csv
from collections import Counter

# These keys come from your Day 1 identity anchor (my.telegram.org)
api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

async def map_relationships(group_username):
    async with TelegramClient('persona_session', api_id, api_hash) as client:
        print(f"[+] Monitoring Group: {group_username}")
        interactions = []
        
        # Scrape last 500 messages
        async for message in client.iter_messages(group_username, limit=500):
            if message.reply_to:
                reply = await message.get_reply_message()
                if reply:
                    # Record: Sender -> Recipient
                    interactions.append((message.sender_id, reply.sender_id))
        
        # Count who is the most "replied to" (The likely authority)
        stats = Counter(interactions)
        print(colored("\n--- TOP SYNDICATE NODES (BY REPLIES) ---", "yellow"))
        for (src, dest), count in stats.most_common(5):
            print(f"User ID {dest} received {count} replies from User ID {src}")

# Note: This is an async function and requires an event loop to run.