import youtube_dl
youtube_dl.utils.bug_reports_message = lambda: ''
import discord

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5, playlist = None):
        super().__init__(source, volume)

        self.data = data
        self.playlist =playlist
        self.title = data.get('title')
        self.url = data.get('url')
    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    def create_playlist(self):
        if(self.playlist == None):
            playlist = []
    async def from_url_playlist(cls,url,*,loop = None, stream= False):
        if(self.playlist == None):
            self.create_playlist()
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download= not stream))
        for i in data:
            if 'entries' in i:
                 x= i['entries'][0]
            filename = x['url'] if stream else ytdl.prepare_filename()
            self.playlist.append(cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=i))
            return self.playlist
        
        