import discord
import aiohttp
import asyncio
import os
import winsound
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

attempts = 0
last_state = None

def play_alarm():
    for i in range(10):
        winsound.Beep(2500, 1000)


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
    global attempts
    global last_state
    print(f"Logged in as {client.user}")
    print("ROBLOX LOOP STARTED")

    channel = client.get_channel(CHANNEL_ID)

    async with aiohttp.ClientSession() as session:
        username = await get_username(session)
        await client.change_presence(
            activity=discord.Game(
                name=f"Love: {username} | Attempts: {attempts}"
            )
        )

    await channel.send(
    f"✅ Bot is now online and monitoring Roblox.\n👀 Watching: {username}"
)


    async with aiohttp.ClientSession() as session:
        while True:
            try:
                attempts += 1
                print(f"Attempt #{attempts}")
                p = await get_presence(session)
                state = p["userPresenceType"]

                await client.change_presence(
                    activity=discord.Game(
                name=f"Love: {username} | Attempts: {attempts}"
                    )
                )

                if last_state is None:
                    last_state = state

                if state != last_state:
                    if state == 0:
                        await channel.send(" 🔴@everyone ilovemycars went Offline.")
                    elif state == 1:
                        play_alarm()

                        for i in range(5):
                            await channel.send(" 🔵@everyone ilovemycars is Online!")
                            await asyncio.sleep(2)
                    
                    elif state == 2:
                        await channel.send( " 🟢@everyone ilovemycars joined a game!")
                    elif state == 3:
                        await channel.send(" 🛠 @everyone ilovemycars is in Studio!")

                    last_state = state

            except Exception as e:
                print("Error:", e)

            await asyncio.sleep(5)

client.run(TOKEN)
