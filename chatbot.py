import discord, re, os
from discord.ext import commands
from googleapiclient.discovery import build
from googletrans import Translator
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from dotenv import load_dotenv

load_dotenv()
chatbot = ChatBot('Rob Obvious')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("chatterbot.corpus.english")
googleapi = os.getenv('GOOGLEAPI')
googleenginetoken = os.getenv('ENGINETOKEN')
client = commands.Bot(command_prefix='+')
resource = build("customsearch", "v1", developerKey=googleapi).cse()
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

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="+commands for help"))

@client.command()
async def commands(ctx):
    embed=discord.Embed(title="Manual",description=f"\nCommands:\n\n+translate | example: (+translate English-Spanish hello)\n\n+image | example: (+image Meme or +image 3 Meme)\n\n+search | example: (+search Meme or +search 3 Meme)\n\n+youtube | example: (+youtube Music or +youtube 3 Music)\n\nPinging the bot will make it respond using a neural network database. | example: (<@!791829989750210570> hey)\n\nBot's prefix is +\n\nSupport Server: https://discord.gg/DRghdsN2Bu\n\nDiscord Bot Invite Link: https://discord.com/api/oauth2/authorize?client_id=791829989750210570&permissions=8&scope=bot",type="rich",colour=0xFF0000)
    await ctx.send(embed=embed)

@client.command()
async def search(ctx, count, *, args=None):
    try:
        try:
            int(count)
            args = fr'{args}'
            result = resource.list(q=fr'{args}', cx=googleenginetoken, start=1).execute()
            try:
                for item in result['items']:
                    if item == result['items'][int(count)]:
                        break
                    search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}\n{item['snippet']}")
                    await ctx.send(embed=search.embed)
            except:
                for item in result['items']:
                    if item == result['items'][int(count)]:
                        break
                    search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}")
                    await ctx.send(embed=search.embed)
        except:
            if args != None:
                count = fr'{count}'
                args = fr'{args}'
                result = resource.list(q=fr"{count} {args}", cx=googleenginetoken, start=1).execute()
                try:
                    for item in result['items']:
                        if item == result['items'][1]:
                            break
                        search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}\n{item['snippet']}")
                        await ctx.send(embed=search.embed)
                except:
                    for item in result['items']:
                        search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}")
                        await ctx.send(embed=search.embed)
                        if item == result['items'][1]:
                            break
            else:
                count = fr'{count}'
                result = resource.list(q=fr"{count}", cx=googleenginetoken, start=1).execute()
                try:
                    for item in result['items']:
                        if item == result['items'][1]:
                            break                    
                        search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}\n{item['snippet']}")
                        await ctx.send(embed=search.embed)
                except:
                    for item in result['items']:
                        if item == result['items'][1]:
                            break                    
                        search = Search(name=item['title'],description=f"Google Search\nLink: {item['link']}")
                        await ctx.send(embed=search.embed)
    except:
        await ctx.send("There were no results.")

@client.command()
async def image(ctx, count, *, args=None):
    try:
        try:
            int(count)
            args = fr'{args}'
            result = resource.list(q=fr"{args}", cx=googleenginetoken, start=1, searchType='image').execute()
            for item in result['items']:
                if item == result['items'][int(count)-1]:
                    break            
                image = Image(name=item['title'],image=item['link'],description="Image")
                await ctx.send(embed=image.embed)
        except:
            if args != None:
                count = fr'{count}'
                args = fr'{args}'
                result = resource.list(q=fr"{str(count)} {args}", cx=googleenginetoken, start=1, searchType='image').execute()
                for item in result['items']:
                    if item == result['items'][1]:
                        break
                    image = Image(name=item['title'],image=item['link'],description="Image")
                    await ctx.send(embed=image.embed)
            else:
                count = fr'{count}'
                result = resource.list(q=fr"{str(count)}", cx=googleenginetoken, start=1, searchType='image').execute()
                for item in result['items']:
                    if item == result['items'][1]:
                        break
                    image = Image(name=item['title'],image=item['link'],description="Image")
                    await ctx.send(embed=image.embed)
    except:
        await ctx.send("There were no results.")

@client.command()
async def youtube(ctx, count, *, args=None, starting=None):
    if starting == None:
        try:
            try:
                int(count)
                args = fr'{args}'
                starting = fr'{starting}'
                result = resource.list(q=fr"www.youtube.com {args}", cx=googleenginetoken, start=1).execute()
                for item in result['items']:
                    if item == result['items'][int(count)-1]:
                        break                
                    await ctx.send(f"{item['title']} - {item['link']}")
            except:
                if args != None:
                    count = fr'{count}'
                    args = fr'{args}'
                    starting = fr'{starting}'
                    result = resource.list(q=fr"www.youtube.com {str(count)} {args}", cx=googleenginetoken, start=1).execute()
                    for item in result['items']:
                        if item == result['items'][1]:
                            break
                        await ctx.send(f"{item['title']} - {item['link']}")
                else:
                    count = fr'{count}'
                    result = resource.list(q=fr"www.youtube.com {str(count)}", cx=googleenginetoken, start=1).execute()
                    for item in result['items']:
                        if item == result['items'][1]:
                            break
                        await ctx.send(f"{item['title']} - {item['link']}")
        except:
            await ctx.send("There were no results")
    else:
        try:
            try:
                int(starting)
                int(count)
                args = fr'{args}'
                result = resource.list(q=fr"www.youtube.com {args}", cx=googleenginetoken, start=starting).execute()
                for item in result['items']:
                    if item == result['items'][int(count)-1]:
                        break                
                    await ctx.send(f"{item['title']} - {item['link']}")
            except:
                if args != None and starting != None:
                    count = fr'{count}'
                    args = fr'{args}'
                    result = resource.list(q=fr"www.youtube.com {str(count)} {args}", cx=googleenginetoken, start=starting).execute()
                    for item in result['items']:
                        if item == result['items'][1]:
                            break
                        await ctx.send(f"{item['title']} - {item['link']}")
                else:
                    count = fr'{count}'
                    result = resource.list(q=fr"www.youtube.com {str(count)}", cx=googleenginetoken, start=1).execute()
                    for item in result['items']:
                        if item == result['items'][1]:
                            break
                        await ctx.send(f"{item['title']} - {item['link']}")
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

@client.event
async def on_message(message):
    mention = fr'<@!{client.user.id}>'
    try:
        if message.author != client.user and message.content.startswith("+") == False and mention in message.content:
            message.content = fr'{message.content}'
            request = re.sub(mention,'',message.content)
            response = chatbot.get_response(request)
            await message.channel.send(fr"{response}")
        await client.process_commands(message)
    except:
        await message.channel.send("There was an error in processing your request.")

client.run(os.getenv('DISCORDTOKEN'))