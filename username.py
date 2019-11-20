import requests
import json
import os
import time
from parse import compile


def main(data):
    while True:
        dt = ''
        tm = ''
        gdata = ''
        commandline = ''
        res = ''
        m3u8id = ''
        quality = ''
        contzdata = ''

        dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        tm = time.strftime('%Hh%Mm%Ss', time.localtime(time.time()))
        tzdata = dt+"."+tm
        contzdata = "["+dt+" | "+tm+"] "
        res = requests.get(data["m3u8get"]+"?url=twitch.tv/"+data["username"])
        gdata = res.json()
        if gdata["success"] == True:
            print(contzdata+data["username"]+' is streaming.')
            # parsing
            if "1080p60" in gdata["urls"]:    
                m3u8id = gdata["urls"]["1080p60"]
                quality = '1080p60'
            elif "1080p" in gdata["urls"]:
                m3u8id = gdata["urls"]["1080p"]
                quality = '1080p'
            elif "720p60" in gdata["urls"]:
                m3u8id = gdata["urls"]["720p60"]
                quality = '720p60'
            elif "720p" in gdata["urls"]:
                m3u8id = gdata["urls"]["720p"]
                quality = '720p'
            elif "480p" in gdata["urls"]:
                m3u8id = gdata["urls"]["480p"]
                quality = '480p'
            elif "360p" in gdata["urls"]:
                m3u8id = gdata["urls"]["480p"]
                quality = '480p'
            elif "160p" in gdata["urls"]:
                m3u8id = gdata["urls"]["160p"]
                quality = '160p'
            # parsing end
            print(contzdata+'Setting the quality to '+quality)
            commandline = "streamlink -o '"+data["username"]+"-"+tzdata+".mp4' "+m3u8id+" best"
            os.system(commandline)
            commandline = "mv "+data["username"]+"-"+tzdata+".mp4 ../record/"+data["username"]+"/"+data["username"]+"-"+tzdata+".mp4"
            os.system(commandline)
        else: 
            print(data["username"]+'is not streaming')

        print('sleep', data["sleeptime"])
        time.sleep(data["sleeptime"])


if __name__ == "__main__":
    # do not touch this
    data = ''
    m3u8get = "https://pwn.sh/tools/streamapi.py"
    p = compile("{}.py")
    result = p.parse(os.path.basename(__file__))
    username = result[0]
    
    # fix this


    sleeptime = 120

    # done
    print('Starting the program')
    print('Set streamer as '+username)
    data = {"m3u8get": m3u8get, "username": username, "sleeptime": sleeptime}
    main(data)