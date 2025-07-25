# !important
# most code is credited to: https://github.com/pawel02/music_bot/tree/main

import discord
from discord.ext import commands

import asyncio
import yt_dlp as YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio/best'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None
        self.ytdl = YoutubeDL.YoutubeDL(self.YDL_OPTIONS)
    

    def search_yt(self, item):
        with YoutubeDL.YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        return {'source': info['url'], 'title': info['title']}
    

    async def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False


    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            #try to connect to voice channel if you are not already connected
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                #in case we fail to connect
                if self.vc == None:
                    await ctx.respond("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(m_url, download=False))
            song = data['url']
            self.vc.play(discord.FFmpegPCMAudio(song, executable= "C:/Program Files (x86)/ffmpeg/bin/ffmpeg.exe", **self.FFMPEG_OPTIONS), after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(), self.bot.loop))
        else:
            self.is_playing = False


    @commands.slash_command(name="play", description="play a song!")
    async def play(self, ctx, query):
        await ctx.response.defer()
        #find voice channel
        try:
            voice_channel = ctx.author.voice.channel
        except:
            await ctx.respond("You need to connect to a voice channel first!")
            return
        
        #check if paused
        if self.is_paused:
            self.vc.resume()
        else:
            #find song
            song = self.search_yt(query)

            if type(song) == type(True):
                await ctx.respond("Couldn't download the song :(")
            else:
                #play song
                await ctx.respond(f"{song['title']} added to the queue")  
                self.music_queue.append([song, voice_channel])
                if self.is_playing == False:
                    await self.play_music(ctx)


    @commands.slash_command(name="pause", description="pause the song!")
    async def pause(self, ctx):
        if self.is_playing:
            await ctx.respond("paused the song!")
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        else:
            await ctx.respond("it is already paused!")
    

    @commands.slash_command(name="resume", description="resume the song!")
    async def resume(self, ctx):
        if self.is_paused:
            await ctx.respond("resumed the song!")
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()
        else:
            await ctx.respond("it is already playing!")


    @commands.slash_command(name="skip", description="skip the song!")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            await ctx.respond("skipped the song!")
            self.vc.stop()
            
            await self.play_next(ctx)
        else:
            await ctx.respond("failed to skip song!")
    

    @commands.slash_command(name="queue", description="shows the current queue!")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += f"#{i+1} -" + self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.respond(f"queue:\n{retval}")
        else:
            await ctx.respond("No music in queue")

    @commands.slash_command(name="clear", description="clear the queue!")
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.respond("Music queue cleared")
    

    @commands.slash_command(name="stop", description="stop the song!")
    async def stop(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
        await ctx.respond("stoped the songs!")


    @commands.slash_command(name="remove", description="removes the last song in the queue!")
    async def remove(self, ctx):
        self.music_queue.pop()
        await ctx.respond("last song removed")