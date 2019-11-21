import requests
import json
import os
import time
from parse import compile


def main(data):
    while True:
        gdata = ''
        commandline = ''
        res = ''
        m3u8id = ''
        quality = ''

        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Loading API')
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'TDB Sync')
        #sync
        #print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'')
        #sync end
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+"Getting "+data["username"]+"'s m3u8 data")
        res = requests.get(data["m3u8get"]+"?url=twitch.tv/"+data["username"])
        gdata = res.json()
        if gdata["success"] == True:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+data["username"]+' is streaming.')
            # parsing
            if data['quality_enable'] == 1:
                if data['quality'] in gdata['urls']:
                    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Using config.json quality: '+data['quality'])
                    m3u8id = gdata["urls"][data['quality']]
                    quality = data['quality']
                else:
                    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown quality. Program exit')
                    exit()
            else:
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
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Setting the quality to '+quality)
            fhname = data["username"]+"-"+time.strftime('%Y-%m-%d.%Hh%Mm%Ss', time.localtime(time.time()))
            commandline = "streamlink -o '"+fhname+".mp4' "+m3u8id+" best"
            os.system(commandline)
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'moving the file named "'+fhname+'".mp4')
            commandline = "mv "+fhname+".mp4 "+data["mvtarget"]+"/"+fhname+".mp4"
            os.system(commandline)
        else: 
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: '+data["username"]+' is not streaming')

        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'sleep', data["sleeptime"])
        time.sleep(data["sleeptime"])


if __name__ == "__main__":
    # do not touch this
    data = ''
    m3u8get = "https://pwn.sh/tools/streamapi.py"
    p = compile("{}.py")
    result = p.parse(os.path.basename(__file__))
    username = result[0]
    print('Starting the program named with '+username+'.py')
    # fix this
    # if you use config.json, change True
    IsConfigFileEnabled = True
    # If IsConfigFileEnabled = True, You dont have to change this
    sleeptime = 180
    quality_enable = 0
    quality = ''
    mvtarget = "../record/"+username

    # Do not fix this
    data = {"m3u8get": m3u8get, "username": username, "sleeptime": sleeptime, "quality_enable": quality_enable, "quality": quality, "mvtarget": mvtarget}

    if IsConfigFileEnabled == True:
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Reading Config File')
        fl = open('config.json','r')
        f = json.load(fl)
        data['sleeptime'] = f['sleeptime']
        if f['username_enable'] == 1:
            data['username'] = f['username']
        if f['quality_enable'] == 1:
            data['quality_enable'] = f['quality_enable']
            data['quality'] = f['quality']
        if f["mvtarget_enable"] == 1:
            data['mvtarget'] = f['mvtarget']

    # done
    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Set streamer as '+data['username'])
    main(data)