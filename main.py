import os, urllib3, time, requests, tqdm, math 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tqdm import *
from pySmartDL import SmartDL
from urllib.error import HTTPError
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image

# Configs
API_HASH = os.environ['API_HASH'] # Api hash
APP_ID = int(os.environ['APP_ID']) # Api id/App id
BOT_TOKEN = os.environ['BOT_TOKEN'] # Bot token
OWNER_ID = int(os.environ['OWNER_ID']) # Your telegram id
AS_DOC = os.environ['AS_DOC'] # Upload method. If True: will send as document | If False: will send as video
DEFAULT_THUMBNAIL = os.environ['DEFAULT_THUMBNAIL'] # Default thumbnail. Used if bot can't find streamtape video thumbnail

# Buttons
START_BUTTONS=[
    [
        InlineKeyboardButton("⭕ Channel ⭕", url="https://t.me/Dads_links"),
        InlineKeyboardButton("📛 Bot Channel 📛", url="https://t.me/Dads_links_bot"),
    ],
    [InlineKeyboardButton("Developer 🙎", url="https://t.me/Doctorstra_1")],
]


# Buttons
REPORT_BUTTONS=[InlineKeyboardButton("💬 Comments 💬", url="https://t.me/D1D2D3D4D5_BOT")],
               

# Helpers

# https://github.com/SpEcHiDe/AnyDLBot
async def progress_for_pyrogram(
    current,
    total,
    ud_type,
    message,
    start
):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \n📊 Percentage: {2}%\n".format(
            ''.join(["▓" for i in range(math.floor(percentage / 5))]),
            ''.join(["░" for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\n🌀 Speed: {2}/s\n⏳ ETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                text="{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

# https://github.com/viperadnan-git/google-drive-telegram-bot/blob/main/bot/helpers/downloader.py
def download_file(url, dl_path):
  try:
    dl = SmartDL(url, dl_path, progress_bar=False)
    dl.start()
    filename = dl.get_dest()
    if '+' in filename:
          xfile = filename.replace('+', ' ')
          filename2 = unquote(xfile)
    else:
        filename2 = unquote(filename)
    os.rename(filename, filename2)
    return True, filename2
  except HTTPError as error:
    return False, error


# Running bot
xbot = Client(
    'StreamtapeLoader',
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Start message
@xbot.on_message(filters.command('start') & filters.private)
async def start(bot, update):
    await update.reply_text(f"**Hello! 🙎 User,\n\nI'm A Powerful Streamtape Url Downloader 💯💯.\n\nPlease send me any Streamtape  link and I can upload it to telegram!\n\nClick /help for more details....\n\nYou must subscribe our channel in order to use me😇**", True, reply_markup=InlineKeyboardMarkup(START_BUTTONS))

# Help message
@xbot.on_message(filters.command('help') & filters.private)
async def help(bot, update):
    await update.reply_text(f"**DADS LINKS STREAMTAPE URL DOWNLOADER BOT 📥\n\nSend Any Streamtape url and I will upload in Telegram\n\n🛑 Warning 🛑\n\n🔹 Only Download Under 2GB\n\n🔹 Porn Will We Permanent Ban ❌\n\nNOTE: Download may take some time! So please wait for it to complete!**", True , reply_markup=InlineKeyboardMarkup(START_BUTTONS))

# About message
@xbot.on_message(filters.command('about') & filters.private)
async def about(bot, update):
    await update.reply_text(f"**⭕️My Name : DADS LINKS STREAMTAPE URL DOWNLOADER BOT 📥\n\n⭕️Creater : @Doctorstra_1\n\n⭕️Language : Python3\n\n⭕️Library : Pyrogram asyncio 0.16.1\n\n⭕️Source Code : 👉 @Doctorstra_1**", True)

# Me message
@xbot.on_message(filters.command('me') & filters.private)
async def me(bot, update):
    await update.reply_text(f"**Current plan details\n-----------------------------\n👤Telegram ID: 0123456789\n📝Plan name: 250GB Per Month\n🚸Expires on: 01/01/2030\n😎If You need Private Bot Please Ch3ck @Doctorstra_1.\n-----------------------------**", True)

# Report message
@xbot.on_message(filters.command('report') & filters.private)
async def report(bot, update):
    await update.reply_text(f"**Report Any Problem in Bot**", True , reply_markup=InlineKeyboardMarkup(REPORT_BUTTONS))

@xbot.on_message(filters.text & filters.private)
async def loader(bot, update):
    dirs = './downloads/'
    if not os.path.isdir(dirs):
        os.mkdir(dirs)
    if not 'streamtape.com' in update.text:
        return
    link = update.text
    if '/' in link:
        links = link.split('/')
        if len(links) == 6:
            if link.endswith('mp4'):
                link = link
            else:
                link = link + 'video.mp4'
        elif len(links) == 5:
            link = link + '/video.mp4'
        else:
            return
    else:
        return
    bypasser = lk21.Bypass()
    url = bypasser.bypass_url(link)
    pablo = await update.reply_text('**Downloading 📥... may take some time! So please wait ⏳', True)
    result, dl_path = download_file(url, dirs)
    if result == True:
        import requests
        r = requests.get(update.text)
        if 'poster="' in r.text:
            text = r.text.split('poster="')[1]
            thumb_url = text.split('"')[0]
            thumb = f'./downloads/thumb_{update.message_id}.jpg'
            r = requests.get(thumb_url, allow_redirects=True)
            open(thumb, 'wb').write(r.content)
        else:
            thumb_url = DEFAULT_THUMBNAIL
            thumb = f'./downloads/thumb_{update.message_id}.jpg'
            r = requests.get(thumb_url, allow_redirects=True)
            open(thumb, 'wb').write(r.content)
        if os.path.exists(thumb):
            width = 0
            height = 0
            metadata = extractMetadata(createParser(thumb))
            if metadata.has('width'):
                width = metadata.get('width')
            if metadata.has('height'):
                height = metadata.get('height')
            Image.open(thumb).convert('RGB').save(thumb)
            img = Image.open(thumb)
            # https://stackoverflow.com/a/37631799/4723940
            # img.thumbnail((90, 90))
            if AS_DOC == 'True':
                img.resize((320, height))
            elif AS_DOC == 'False':
                img.resize((90, height))
            img.save(thumb, "JPEG")
        metadata = extractMetadata(createParser(dl_path))
        if metadata is not None:
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            else:
                duration = 0
        start_dl = time.time()
        await pablo.edit_text('yeh,boy Uploading 📤...')
        if AS_DOC == 'True':
            await update.reply_document(
                document=dl_path, 
                quote=True, 
                thumb=thumb, 
                progress=progress_for_pyrogram, 
                progress_args=(
                    'yeh,boy Uploading 📤...', 
                    pablo, 
                    start_dl
                )
            )
            os.remove(dl_path)
            os.remove(thumb)
        elif AS_DOC == 'False':
            await update.reply_video(
                video=dl_path,
                quote=True,
                thumb=thumb,
                duration=duration,
                progress=progress_for_pyrogram,
                progress_args=(
                    'yeh boy Uploading 📤...',
                    pablo,
                    start_dl
                )
            )
            os.remove(dl_path)
            os.remove(thumb)
    else:
        await pablo.edit_text('Downloading failed 🛑.')
    await pablo.delete()

print("\n")
print("||\    /||")
print("|| \  / ||")
print("||  \/  ||")
print("||      ||")
print("\n")
print("XXXXXXXXXX")

vurl = input("\nVideo URL:")

x = vurl.replace('/','').replace('https:www.mxplayer.in','').replace('movie','').replace('show','').replace('music-online','')

header = {'x-av-code': '29',
'x-app-version': '1330001208',
'x-platform': 'android',
'x-resolution': '1920x1080',
'x-country': 'US'}

data = '{"path":"'+ vurl +'"}'

url = 'https://androidapi.mxplay.com/v1/deeplink/parser'

try:

    fetch = requests.post(url,data=data,headers=header,verify=False)

    resp = fetch.json()
    
    ex_link = resp['resources'][0]['chromecastPlayInfo'][0]['playUrl']
    
    update_link = ex_link.replace('/dash/h264_baseline_chromecast.mpd','').replace('/dash/h264_high_chromecast.mpd','').replace('dash/h265_main_chromecast.mpd','')

    ql = (input("\nEnter Video Quality: Ex- q720 or q480 or q360 or x265_720 or x265_480\n"))


    qstore = {"q720": "/download/h264_720_high_3000k.mp4",
"q480": "/download/h264_480_high_1750k.mp4",
"q360": "/download/h264_360_high_750k.mp4",
"x265_720": "/download/h265_720_main_3000k.mp4",
"x265_480": "/download/h265_480_main_1750k.mp4"}


    get = qstore.get(ql)

    save = update_link + get

    name = x + ".mp4"

    with requests.get(save, stream=True) as r:

        r.raise_for_status()

        with open(name, 'wb') as f:

            pbar = tqdm(total=int(r.headers['Content-Length']))

            for chunk in r.iter_content(chunk_size=8192):

                if chunk:

                    f.write(chunk)

                    pbar.update(len(chunk))

except:
    
    print("an Error accured, Please retry with valid URL")

xbot.run()
