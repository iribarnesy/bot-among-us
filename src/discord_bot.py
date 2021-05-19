import time
import os
from dotenv import load_dotenv
import asyncio
import discord
from discord.ext import commands
from gtts import gTTS
from playsound import playsound

from src.utils import KillableThread

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("GUILD")
CHANNEL = os.getenv("CHANNEL")
TEXT_CHANNEL_ID = os.getenv("TEXT_CHANNEL_ID")
VOICE_CHANNEL_ID = os.getenv("VOICE_CHANNEL_ID")

ffmpeg_options = {
    'options': '-vn'
}

client = discord.Client()

class DiscordBot(commands.Bot):
    def __init__(self):
        commands.Bot.__init__(self, command_prefix='!', self_bot=False)
        self.guild = None
        self.voice_channel = None
        self.text_channel = None
        self.voice_client = None
        self.add_commands()
        self.loop = asyncio.get_event_loop()

    async def on_ready(self):
        self.guild = discord.utils.get(self.guilds, name=GUILD)
        self.voice_channel = discord.utils.get(self.guild.channels, id=int(VOICE_CHANNEL_ID))
        self.text_channel = discord.utils.get(self.guild.channels, id=int(TEXT_CHANNEL_ID))
        print('{} is ready !'.format(self.user.name))

    def _wait_for_function(self, func):
        future = asyncio.run_coroutine_threadsafe(
            func, 
            self.loop)
        # wait for the coroutine to finish
        return future.result()

    def write(self, message):
        self._wait_for_function(self.text_channel.send(message))

    def play(self, audio_path="tmp.mp3"):
        if self.voice_client is None or not self.voice_client.is_connected():
            self.join_voice_channel()
        audio_source = discord.FFmpegPCMAudio(audio_path)
        if not self.voice_client.is_playing():
            self.voice_client.play(
                audio_source, 
                after=lambda error: print('done', error))

    def say(self, message, language="en"):
        audio = gTTS(text=message, lang=language, slow=False)
        audio_path = "tmp.mp3"
        audio.save(audio_path)
        self.play(audio_path)

    def join_voice_channel(self):
        self._wait_for_function(self.voice_channel.connect())
        self.voice_client = self.guild.voice_client
    
    def leave_voice_channel(self):
        voice_client = self.guild.voice_client
        if voice_client is not None and voice_client.is_connected():
            self._wait_for_function(voice_client.disconnect())
        else:
            print("The bot is not connected to a voice channel")

    def start_listening(self):
        self.discord_thread = KillableThread(name="discord_thread", target=self.run, args=(DISCORD_TOKEN,))
        self.discord_thread.start()
        print("Wait 4s for the discord bot initialization... 🤖")
        time.sleep(4)

    def stop_listening(self):
        self.leave_voice_channel()
        if self.discord_thread is not None:
            self.discord_thread.kill()
            print("Terminate :", self.discord_thread)
            try:
                # Try a command to make it crash
                self.join_voice_channel()
            except:
                print("Well closed !")
        

    """ Kept for some debugging in the discord interface
    """
    def add_commands(self):
        @commands.command(name="status", pass_context=True)
        async def status(ctx):
            print(ctx)
            await ctx.channel.send(ctx)
        
        @commands.command(name='join', help='Tells the bot to join the voice channel')
        async def join(ctx):
            if not ctx.message.author.voice:
                await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
                return
            else:
                channel = ctx.message.author.voice.channel
            await channel.connect()
            print(self.user)

        @commands.command(name='leave', help='To make the bot leave the voice channel')
        async def leave(ctx):
            voice_client = ctx.message.guild.voice_client
            if voice_client.is_connected():
                await voice_client.disconnect()
            else:
                await ctx.send("The bot is not connected to a voice channel.")

        @commands.command()
        async def play(ctx, audio_path: str):
            voice_client: discord.VoiceClient = ctx.voice_client
            # vc = ctx.message.guild.voice_client
            if voice_client is None:
                voice_client = await discord.utils.get(ctx.guild.channels, name='among').connect()
            audio_source = discord.FFmpegPCMAudio(audio_path)
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: print('done', e))

        self.add_command(status)
        self.add_command(join)
        self.add_command(leave)
        self.add_command(play)
        