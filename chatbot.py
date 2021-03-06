import discord, re, os
from discord.ext import commands
from googlesearch import search
from googletrans import Translator
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import urllib.request
from bs4 import BeautifulSoup
from keepalive import keepalive

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
chatbot = ChatBot('Rob Obvious')
trainer = ChatterBotCorpusTrainer(chatbot.storage)
trainer.train("chatterbot.corpus.english")
client = commands.Bot(command_prefix='+')
translator = Translator()

class Image():
    def __init__(self,name,image,description):
        self.name=name
        self.image=image
        self.description=description
        self.embed=(discord.Embed(title=self.name,description=self.description,type="rich",colour=0x0000FF)).set_image(url=self.image)

class Search():
    def __init__(self,name,description):
        self.name=name
        self.description=description
        self.embed=discord.Embed(title=self.name,description=self.description,type="rich",colour=0x00FF00)

languages = {
'Afrikaans':'af',
'Albanian':'sq',
'Amharic':'am',
'Arabic':'ar',
'Armenian':'hy',
'Azerbaijani':'az',
'Basque':'eu',
'Belarusian':'be',
'Bengali':'bn',
'Bosnian':'bs',
'Bulgarian':'bg',
'Catalan':'ca',
'Cebuano':'ceb',
'Chichewa':'ny',
'Chinese':'zh-cn',
'Corsican':'co',
'Croatian':'hr',
'Czech':'cs',
'Danish':'da',
'Dutch':'nl',
'English':'en',
'Esperanto':'eo',
'Estonian':'et',
'Filipino':'tl',
'Finnish':'fi',
'French':'fr',
'Frisian':'fy',
'Galician':'gl',
'Georgian':'ka',
'German':'de',
'Greek':'el',
'Gujarati':'gu',
'Haitian creole':'ht',
'Hausa':'ha',
'Hawaiian':'haw',
'Hebrew':'iw',
'Hebrew':'he',
'Hindi':'hi',
'Hmong':'hmn',
'Hungarian':'hu',
'Icelandic':'is',
'Igbo':'ig',
'Indonesian':'id',
'Irish':'ga',
'Italian':'it',
'Japanese':'ja',
'Javanese':'jw',
'Kannada':'kn',
'Kazakh':'kk',
'Khmer':'km',
'Korean':'ko',
'Kyrgyz':'ky',
'Lao':'lo',
'Latin':'la',
'Latvian':'lv',
'Lithuanian':'lt',
'Luxembourgish':'lb',
'Macedonian':'mk',
'Malagasy':'mg',
'Malay':'ms',
'Malayalam':'ml',
'Maltese':'mt',
'Maori':'mi',
'Marathi':'mr',
'Mongolian':'mn',
'Myanmar':'my',
'Nepali':'ne',
'Norwegian':'no',
'Odia':'or',
'Pashto':'ps',
'Persian':'fa',
'Polish':'pl',
'Portuguese':'pt',
'Punjabi':'pa',
'Romanian':'ro',
'Russian':'ru',
'Samoan':'sm',
'Scots gaelic':'gd',
'Serbian':'sr',
'Sesotho':'st',
'Shona':'sn',
'Sindhi':'sd',
'Sinhala':'si',
'Slovak':'sk',
'Slovenian':'sl',
'Somali':'so',
'Spanish':'es',
'Sundanese':'su',
'Swahili':'sw',
'Swedish':'sv',
'Tajik':'tg',
'Tamil':'ta',
'Telugu':'te',
'Thai':'th',
'Turkish':'tr',
'Ukrainian':'uk',
'Urdu':'ur',
'Uyghur':'ug',
'Uzbek':'uz',
'Vietnamese':'vi',
'Welsh':'cy',
'Xhosa':'xh',
'Yiddish':'yi',
'Yoruba':'yo',
'Zulu':'zu'
}

google = search

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="+commands for help"))

@client.command()
async def commands(ctx):
    embed=discord.Embed(title="Manual",description="\nCommands:\n\n+translate | example: (+translate English-Spanish hello)\n\n+image | example: (+image Meme or +image 3 Meme)\n\n+search | example: (+search Meme or +search 3 Meme)\n\n+youtube | example: (+youtube Music or +youtube 3 Music)\n\n+chat | example: (+chat hey)\n\nBot's prefix is +\n\nSupport Server: https://discord.gg/6Fu2399thq\n\nDiscord Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=791829989750210570&permissions=8&scope=bot",type="rich",colour=0xFF0000)
    await ctx.send(embed=embed)

@client.command()
async def search(ctx, count, *, args=None):
    global google
    try:
        count=int(count)
        if count <= 3:
            for url in google(fr'{args}', stop=count):
                try:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}\n{meta[len(meta)-1]}")
                    await ctx.send(embed=search.embed)
                except:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}")
                    await ctx.send(embed=search.embed)
        elif count > 3:
            await ctx.send("You can't have more than three searches per command.")
    except:
        if args != None:
            for url in google(fr"{count} {args}", stop=1):
                try:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}\n{meta[len(meta)-1]}")
                    await ctx.send(embed=search.embed)
                except:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}")
                    await ctx.send(embed=search.embed)
        else:
            for url in google(fr"{count}", stop=1):
                try:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}\n{meta[len(meta)-1]}")
                    await ctx.send(embed=search.embed)
                except:
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    metas=soup.find_all('meta')
                    meta=[ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                    search = Search(name=title,description=f"Google Search\nLink: {url}")
                    await ctx.send(embed=search.embed)

@client.command()
async def image(ctx, count, *, args=None):
    global google
    try:
        try:
            count=int(count)
            if count <= 3:
                for url in google(fr'PNG Image File {args}', stop=count):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    image = Image(name=title,description=f"Image\nLink: {url}",image=url)
                    await ctx.send(embed=image.embed)
            elif count > 3:
                await ctx.send("You can't have more than three searches per command.")
        except:
            if args != None:
                for url in google(fr'PNG Image File {count} {args}', stop=1):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    image = Image(name=title,description=f"Image\nLink: {url}",image=url)
                    await ctx.send(embed=image.embed)
            else:
                for url in google(fr'PNG Image File {count} {args}', stop=1):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    image = Image(name=title,description=f"Image\nLink: {url}",image=url)
                    await ctx.send(embed=image.embed)
    except:
        await ctx.send("There were no results.")

@client.command()
async def youtube(ctx, count, *, args=None):
    global google
    try:
        try:
            count=int(count)
            if count <= 3:
                for url in google(fr'youtube {args}', stop=count):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    await ctx.send(f"{title} - {url}")
            elif count > 3:
                await ctx.send("You can't have more than three searches per command.")
        except:
            if args != None:
                for url in google(fr"youtube {count} {args}", stop=1):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    await ctx.send(f"{title} - {url}")
            else:
                for url in google(fr"youtube {count}", stop=1):
                    soup = BeautifulSoup(opener.open(url),"html.parser")
                    title=soup.title.string
                    await ctx.send(f"{title} - {url}")
    except:
        await ctx.send("There were no results.")

@client.command()
async def translate(ctx, language, *, args=None):
    language = fr'{language}'
    args = fr'{args}'
    match = re.search("-",fr"{language}")
    try:
        if match:
            language = language.split("-")
            language[0] = (language[0]).capitalize()
            language[1] = (language[1]).capitalize()
            if len(language) == 2 and args != None:
                language1 = languages[language[0]]
                language2 = languages[language[1]]
                translation = translator.translate(text=fr"{args}", src=language1, dest=language2)
                embed=discord.Embed(title="Translation",description=f"{language[0]}: {args}\n\n{language[1]}: {translation.text}",type="rich",colour=0xFF0000)
                await ctx.send(embed=embed)
        else:
            await ctx.send("There was an error in processing your request.")
    except:
        await ctx.send("There was an error in processing your request.")

@client.command()
async def chat(ctx, *, args):
    args = fr'{args}'
    request = args
    response = chatbot.get_response(request)
    await ctx.send(fr"{response}")

keepalive()
client.run(os.getenv('DISCORDTOKEN'))
