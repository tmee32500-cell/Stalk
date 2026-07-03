import discord
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

last_state = None

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
ROBLOSECURITY = os.getenv("ROBLOSECURITY")

USER_ID = 2459564462  # CHANGE THIS

client = discord.Client(intents=discord.Intents.default())

last_state = None

async def get_presence(session):
    url = "https://presence.roblox.com/v1/presence/users"

    headers = {
        "Cookie": f".ROBLOSECURITY={ROBLOSECURITY}",
        "Content-Type": "application/json"
    }

    payload = {"userIds": [USER_ID]}

    async with session.post(url, json=payload, headers=headers) as r:
        data = await r.json()
        
        print("ROBLOX RESPONSE:", data)

        state = data["userPresences"][0]["userPresenceType"]
        print("ROBLOX STATE:", state)
        return data["userPresences"][0]



async def get_username(session):
    url = f"https://users.roblox.com/v1/users/{USER_ID}"

    async with session.get(url) as r:
        data = await r.json()

    return data["name"]



@client.event
async def on_ready():
    global last_state
    print(f"Logged in as {client.user}")
    print("ROBLOX LOOP STARTED")

    channel = client.get_channel(CHANNEL_ID)

    async with aiohttp.ClientSession() as session:
        username = await get_username(session)

    await channel.send(
    f"✅ Bot is now online and monitoring Roblox.\n👀 Watching: {username}"
)


    async with aiohttp.ClientSession() as session:
        while True:
            try:
                p = await get_presence(session)
                state = p["userPresenceType"]

                if last_state is None:
                    last_state = state

                if state != last_state:
                    if state == 0:
                        await channel.send("🔴 Offline")
                    elif state == 1:
                        await channel.send("🟢 Online")
                    elif state == 2:
                        await channel.send("🎮 In Game")
                    elif state == 3:
                        await channel.send("🛠 In Studio")

                    last_state = state

            except Exception as e:
                print("Error:", e)

            await asyncio.sleep(15)

client.run(TOKEN)
