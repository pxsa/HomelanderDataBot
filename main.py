import asyncio
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from bale import Bot

# =========================================================
# Initialize the bot with your token
# =========================================================
load_dotenv('.env') 
BOT_TOKEN = os.getenv('BOT_TOKEN')


# =========================================================
# Create a bot instance
# =========================================================
homelander = Bot(BOT_TOKEN, ssl=False)




# =========================================================
# Run the bot
# =========================================================
@homelander.event
async def on_ready():
    print(f'Logged in as {homelander.user}')








# =========================================================
# Run the bot
# =========================================================
homelander.run()



