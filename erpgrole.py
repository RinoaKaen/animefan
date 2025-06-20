import discord
import re

# ====== SETUP ======
TOKEN = 'TOKEN'  # Replace with your bot token
GUILD_ID = 1149713429561622609  # Replace with your server ID
# ====================

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)

def parse_amount(text):
    return int(text.replace(',', ''))

def shorten_number(n):
    if n >= 1_000_000_000_000_000:
        return f"{n / 1_000_000_000_000_000:.1f}Q"
    elif n >= 1_000_000_000_000:
        return f"{n / 1_000_000_000_000:.1f}T"
    elif n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f}B"
    elif n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    else:
        return str(n)

@client.event
async def on_ready():
    pass

@client.event
async def on_message(message):
    if message.author.id != 555955826880413696:
        return

    if not message.embeds:
        return

    embed = message.embeds[0]

    if not embed.author or '— profile' not in embed.author.name:
        return

    username = embed.author.name.split(' — ')[0]
    coins, bank = 0, 0

    for field in embed.fields:
        if field.name.strip().lower() == 'money':
            match_coins = re.search(r'\*\*Coins\*\*: ([\d,]+)', field.value)
            if match_coins:
                coins = parse_amount(match_coins.group(1))

            match_bank = re.search(r'\*\*Bank\*\*: ([\d,]+)', field.value)
            if match_bank:
                bank = parse_amount(match_bank.group(1))

    if coins == 0 and bank == 0:
        return

    total = coins + bank
    short = shorten_number(total)

    guild = client.get_guild(GUILD_ID)
    if not guild:
        return

    await guild.chunk()

    member = discord.utils.find(lambda m: m.name == username, guild.members)
    if not member:
        return

    new_nick = f"{member.display_name} | {short}"
    try:
        await member.edit(nick=new_nick[:32])
    except:
        pass

client.run(TOKEN)