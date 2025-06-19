import discord
import random
import asyncio

TOKEN = ("MTM3OTAzNDU1OTQ0NTg2MDQ0Mg.GON5jW.Y99bR4qgjBmvxF1Y2e2DvtYLSB1WmA2SDMecks")
GUILD_ID = 1149713429561622609  # your server ID
ROLE_ID = 1325399876024012800  # your role ID

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

def generate_random_color():
    return discord.Color(random.randint(0, 0xFFFFFF))

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')
    await asyncio.sleep(1)
    guild = client.get_guild(GUILD_ID)
    if not guild:
        print("❌ Guild not found!")
        return
    role = guild.get_role(ROLE_ID)
    if not role:
        print("❌ Role not found!")
        return
    while True:
        try:
            new_color = generate_random_color()
            await role.edit(color=new_color, reason="Random color change")
            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error: {e}")
            await asyncio.sleep(10)

client.run(TOKEN)
