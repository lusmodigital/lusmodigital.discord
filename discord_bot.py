import os
import discord
import requests
from discord.ext import commands

# Environment variables - replace with your actual values!
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN") # your bot token
GITHUB_REPO = os.getenv("GITHUB_REPO") # Your github repo like owner/reponame
GH_PAT = os.getenv("GH_PAT") # your github personal access token
WORKFLOW_ID = os.getenv("WORKFLOW_ID") # name of the workflow file inside .github/workflows folder


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.command(name="run_poller", help="Runs the discord poller")
async def run_poller(ctx):
    await ctx.send("Starting the poller...")
    try:
        headers = {
            "Authorization": f"Bearer {GH_PAT}",
            "Accept": "application/vnd.github+json"
        }
        url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/{WORKFLOW_ID}/dispatches"
        data = {"ref": "main"}  # Or the branch you want
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        await ctx.send("Successfully triggered the poller.")
    except Exception as e:
        await ctx.send(f"Failed to trigger the poller: {e}")
    
bot.run(DISCORD_TOKEN)