import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from tqdm import *

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
