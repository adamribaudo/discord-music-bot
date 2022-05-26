import discord
from discord.ext import commands
from discord import PCMAudio
import os
import random
from dotenv import load_dotenv, find_dotenv
from os import listdir
from os.path import isfile, join



if find_dotenv():
    load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PORT = os.getenv("PORT")

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
 
def create_audio_source():
    all_tracks = [f for f in listdir('music') if isfile(join('music', f))]
    selected_track = random.choice(all_tracks)
    print("Selected " + selected_track)
    audio_source = PCMAudio(open(os.path.join('music',selected_track), mode='rb'))
    return audio_source

@client.command(aliases=['paly', 'p', 'P', 'pap', 'pn', 'play_next', 'playnext'])
async def play(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = guild.voice_client
    if voice_client is None: voice_client = await discord.utils.get(guild.voice_channels, name='music').connect()

    def after_play(error):
        if not voice_client.is_playing():
            voice_client.play(create_audio_source(), after = after_play)

    print("Starting voice_client.play")
    voice_client.play(create_audio_source(), after = after_play)
    
@client.command(aliases=['disconnect', 'dismiss', 'dc'])
async def leave(ctx, empty_queue=False):
    guild = ctx.guild
    voice_client: discord.VoiceClient = guild.voice_client
    if voice_client:
        await voice_client.disconnect()

if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
