import os.path
from os import listdir, getenv, walk
import discord
import asyncio
from discord.ext import commands


class Voice(commands.Cog):
    """
    Voice Cog for playing local audio files.


    :param client: Discord Client
    """
    def __init__(self, client):
        self.client = client
        self.audio_path = getenv("AUDIO_PATH")

        """
        { 
        guildid: {
            file_name: str (file name without the file type)
            volume: int (volume of file)
            loop: int (amount of times to loop)
            count: int (loop count we are on)
            }
        }
        """
        self.audio_play = {}

        """
        {
        guildid: {
            file_names: list ( file names that need to be played in a row )
            volume: int (volume of file)
            loop: int (amount of times to loop)
            count: int (loop count we are on)
            index: the index of the list we are on.
            max_index: max index the file names list can have.
            }
        }
        """
        self.dic_play = {}

    @commands.command(aliases=["bruh"])
    async def play(self, ctx, file_name="bruh", volume=100, loop=1):
        """
        Play/Bruh an audio file.

        :param file_name: File name to play
        :param volume: Volume to play to the file at
        :param loop: amount of times to loop
        """
        if not await self.join(ctx):
            return

        voice_client = self.get_voice_client(ctx)
        if not voice_client:
            return await ctx.send("Could not get voice client.")

        audio_info = {
            "file_name": file_name,
            "volume": volume,
            "loop": loop,
            "count": 0
        }
        self.audio_play[ctx.guild.id] = audio_info
        try:
            self.voice_client_play(voice_client, file_name, volume, loop)
        except:
            pass

    @commands.command()
    async def dic(self, ctx, volume=100, loop=1, *, file_names):
        """
        Play files right after each other.

        :param volume: Volume to play the files at
        :param loop: Amount of times to loop this message.
        :param file_names: A list of file names separated by spaces.
        """
        file_names: list = file_names.split(" ")

        dic = {
            "file_names": file_names,
            "volume": volume,
            "loop": loop,
            "count": 0,
            "index": 0,
            "max_index": len(file_names) - 1
        }

        if not await self.join(ctx):
            return

        voice_client = self.get_voice_client(ctx)
        if not voice_client:
            return await ctx.send("Could not get voice client.")

        self.dic_play[ctx.guild.id] = dic
        try:
            self.voice_client_play(voice_client, file_names[0], volume)
        except:
            pass

    @commands.command(aliases=["disconnect"])
    async def leave(self, ctx, message=False):
        """
        Leave the voice channel in this guild.

        :param ctx: Context object
        :param message: Whether to send a message to the text channel.
        """
        if await self.disconnect_from_vc(ctx=ctx):
            if not message:
                return True
            return await ctx.send("I left your voice channel.")
        if message:
            return await ctx.send("I could not find a voice channel to leave.")

    @commands.command()
    async def join(self, ctx, message=False):
        """
        Join the voice channel of the user.

        :param ctx: Context object
        :param message: Whether to send a message to the text channel if it connected.
        """
        if await self.connect_to_vc(ctx):
            if not message:
                return True
            return await ctx.send("I connected to your voice channel.")
        await ctx.send("I could not find your voice channel.")

    @commands.command(aliases=["files"])
    async def audio(self, ctx, sub_directory=None):
        """List all of the audio files that are able to be played.

        :param sub_directory: The directory you want to audio files from.
        """

        sub_directories = []
        files_in_folder = []

        sub_directory = None if not sub_directory else sub_directory.replace(".", "/")
        accurate_audio_path = f"{self.audio_path}{sub_directory}/" if sub_directory else self.audio_path
        try:
            files = listdir(accurate_audio_path)
        except:
            return await ctx.send("That is not a sub-folder.")

        for file in files:
            file_path = f"{accurate_audio_path}{file}"
            if os.path.isdir(file_path):
                sub_directories.append(file)
            elif os.path.isfile(file_path):
                files_in_folder.append(file)

        audio_files = []
        for file in files_in_folder:
            if ".mp3" in file:
                audio_files.append(file.replace(".mp3", ""))

        dirs_in_folder_msg = f"**Sub-Folders in this folder:** {', '.join(sub_directories)}"
        audio_in_folder_msg = f"**Audio files in this folder:** {', '.join(audio_files)}"

        final_message = f"{dirs_in_folder_msg}\n{audio_in_folder_msg}"

        await ctx.send(final_message)

    @commands.command()
    async def ping(self, ctx):
        """Test if the bot is online."""
        await ctx.send("Pong")

    async def connect_to_vc(self, ctx):
        """
        Connect to the voice channel a user is connected to.

        :param ctx: Context Object
        """
        voice = ctx.author.voice
        if not voice:
            return False
        voice_channel = voice.channel
        if not voice_channel:
            return False
        try:
            await voice_channel.connect()
        except discord.ClientException:
            voice_client = self.get_voice_client(ctx)
            if voice_client:
                if voice_client.channel == voice_channel:
                    return True
            if await self.disconnect_from_vc(ctx=ctx):
                await voice_channel.connect()
        return True

    async def disconnect_from_vc(self, ctx=None, voice_client=None):
        """
        Disconnect from a voice channel

        :param [OPTIONAL] ctx: Context Object
        :param [OPTIONAL] voice_client: bot voice client to disconnect from
        :return:
        """
        try:
            if ctx:
                voice_client = self.get_voice_client(ctx)
            if not voice_client:
                return
            await asyncio.sleep(3)
            if not voice_client.is_playing():
                await voice_client.disconnect()
                return True
        except:
            pass

    def get_voice_client(self, ctx):
        """
        Get the voice client associated with the Context.

        :param ctx: Context Object
        :return: Voice client or NoneType
        """
        for voice_client in self.client.voice_clients:
            if voice_client.guild == ctx.guild:
                return voice_client

    @staticmethod
    def fetch_audio_source(file_name, volume=100):
        """
        Create and get the audio source.

        :param file_name: The file name without file type.
        :param volume: volume to play the file name at
        """
        ffmpeg_options = {
            'options': '-vn'
        }
        return AudioSource(discord.FFmpegPCMAudio(file_name, **ffmpeg_options), volume=volume/100)

    def voice_client_play(self, voice_client, file_name, volume, loop=1, count=0):
        """
        Play an audio source.

        :param voice_client: Voice client connected to VC
        :param file_name: file name to play
        :param volume: volume to play the file at
        :param loop: amount of times to loop.
        :param count: the loop iteration we are on
        """
        if count == loop or loop < 1:
            dc_from_vc = self.disconnect_from_vc(voice_client=voice_client)
            run_coro = asyncio.run_coroutine_threadsafe(dc_from_vc, self.client.loop)
            run_coro.result()

            if self.dic_play.get(voice_client.guild.id):
                self.dic_play.pop(voice_client.guild.id)

            if self.audio_play.get(voice_client.guild.id):
                self.audio_play.pop(voice_client.guild.id)
            return
        file_name = file_name.replace(".", "/")

        # we do not want users to try messing around with files across other directories, so we will do hard checks
        # and create a fallback for the audio not being found.
        # we will also use dot notation to prevent users from attempting to go to different directories.
        can_play = False

        full_file_path = f"{self.audio_path}{file_name}.mp3"
        for root, _, files in walk(self.audio_path):
            for file in files:
                current_path = f"{root}/{file}"
                if current_path == full_file_path:
                    can_play = True
        if not can_play:
            full_file_path = f"{self.audio_path}mujy/that_audio_file_does_not_exist.mp3"

        voice_client.play(self.fetch_audio_source(full_file_path, volume=volume),
                          after=self.next_play)

    def next_play(self, error):
        """
        The method called after a song ends or errors.

        :param error: Discord Error
        """
        for voice_client in self.client.voice_clients:
            if voice_client.is_playing() or voice_client.is_paused():
                continue
            audio_info: dict = self.audio_play.get(voice_client.guild.id)
            if not audio_info:
                dic: dict = self.dic_play.get(voice_client.guild.id)
                if not dic:
                    return
                audio_names: list = dic.get("file_names")

                if dic["index"] >= dic["max_index"]:
                    dic["index"] = 0
                else:
                    dic["index"] += 1

                if dic["index"] == 0:
                    # only update the count after going through the entire list.
                    dic["count"] += 1

                if audio_names:
                    self.voice_client_play(voice_client, audio_names[dic["index"]], volume=dic["volume"],
                                           loop=dic["loop"], count=dic["count"])
                return
            audio_info["count"] += 1
            self.voice_client_play(voice_client, audio_info["file_name"], audio_info["volume"], audio_info["loop"],
                                   audio_info["count"])


class AudioSource(discord.PCMVolumeTransformer):
    """Source for the Audio Files being played."""
    def __init__(self, source, *, volume=1):
        super().__init__(source, volume)
