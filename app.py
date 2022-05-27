import discord
from discord.ext import commands
from discord import PCMAudio
import os
import random
from dotenv import load_dotenv, find_dotenv
from os import listdir
from os.path import isfile, join
import sys

if find_dotenv():
    load_dotenv()

BOT_PROFILE = sys.argv[1] # First argument should be an identifier for the bot. 
# This will be used to pull the discord token, the voice channel name, and the music folder
MUSIC_FOLDER = BOT_PROFILE
VOICE_CHANNEL = BOT_PROFILE
DISCORD_TOKEN = os.getenv(BOT_PROFILE)

# Create bot
client = commands.Bot(command_prefix='!')

# Startup Information
@client.event
async def on_ready():
    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))
 
def create_audio_source():
    
    all_tracks = [f for f in listdir(MUSIC_FOLDER) if (isfile(join(MUSIC_FOLDER, f)) and ".mp3" in  f)]
    selected_track = random.choice(all_tracks)
    print("Selected " + selected_track)
    audio_source = discord.FFmpegPCMAudio(source=os.path.join(MUSIC_FOLDER,selected_track),executable='ffmpeg')
    return audio_source

@client.command(aliases=['next','paly', 'p', 'P', 'pap', 'pn', 'play_next', 'playnext'])
async def play(ctx):
    guild = ctx.guild
    voice_client: discord.VoiceClient = guild.voice_client
    if voice_client is None: voice_client = await discord.utils.get(guild.voice_channels, name=VOICE_CHANNEL).connect()

    def after_play(error):
        if not voice_client.is_playing():
            voice_client.play(create_audio_source(), after = after_play)

    if not voice_client.is_playing():
        # If not playing, then play
        voice_client.play(create_audio_source(), after = after_play)
    else:
        # If playing, then stop and call after_play()
        voice_client.stop()
    
@client.command(aliases=['disconnect', 'dismiss', 'dc'])
async def leave(ctx, empty_queue=False):
    guild = ctx.guild
    voice_client: discord.VoiceClient = guild.voice_client
    if voice_client:
        await voice_client.disconnect()

if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
