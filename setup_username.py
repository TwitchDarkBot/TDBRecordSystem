import requests
import json
import os
import time
from parse import compile
import subprocess
import platform
import tdbclient


def main(data, cont):
    streamer = data["username"]
    tdblogger = tdbclient.client(streamer)
    tdblogger.comment = 1
    tdblogger.send()
    # Repeat while KeyboardInterrupt
    while True:
        # Reset data
        gdata = ''
        commandline = ''
        res = ''
        m3u8id = ''
        quality = ''
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Loading API')
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'TDB Sync mode is AUTO')
        tdblogger.comment = 2
        tdblogger.send()
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+"Getting "+data["username"]+"'s m3u8 data")
        streamer = data["username"]
        res = tdblogger.status(streamer)
        if res["status"] == True: # If streamer is streaming
            res = requests.get(data["m3u8get"]+"?url=twitch.tv/"+data["username"]) # request streamer is streaming, m3u8 id
            gdata = res.json() # save json
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+data["username"]+' is streaming.')
            # json parsing
            if data['quality_enable'] == 1:
                tdblogger.comment = 3
                tdblogger.send()
                if data['quality'] in gdata['urls']:
                    if cont == False:
                        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Using config.json quality: '+data['quality'])
                    m3u8id = gdata["urls"][data['quality']]
                    quality = data['quality']
                elif data['quailty'] == "best":
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
                else:
                    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown quality. Program exit in 5 secounds.')
                    time.sleep(5)
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
            while True:
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Setting the quality to '+quality)
                fhname = data["username"]+"-"+time.strftime('%Y-%m-%d.%Hh%Mm%Ss', time.localtime(time.time()))
                commandline = ffmpeg+' -err_detect ignore_err -i "'+m3u8id+'" -c copy '+fhname+'.mp4'
                #subprocess.run([commandline])
                os.system(commandline) # streamlink start
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'moving the file named "'+fhname+'".mp4')
                if platform.system() == 'Windows':
                    commandline = "move "+fhname+".mp4 "+data["mvtarget"]+"\\"+fhname+".mp4"
                elif platform.system() == 'Linux':
                    commandline = "mv "+fhname+".mp4 "+data["mvtarget"]+"/"+fhname+".mp4"
                os.system(commandline)
                # Re-Check Streamer is streaming
                res = tdblogger.status(streamer)
                if res['status'] == True:
                    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: '+'Restarting the record')
                else:
                    tdblogger.comment = 6
                    tdblogger.send()
                    break
        else: # Streamer is not streaming
            tdblogger.comment = 4   
            tdblogger.send()
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: '+data["username"]+' is not streaming')
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'sleep', data["sleeptime"])
        tdblogger.comment = 8
        tdblogger.send()
        time.sleep(data["sleeptime"])

if __name__ == "__main__":
    if platform.system() == 'Windows':
        nul = 0
    elif platform.system() == 'Linux':
        nul = 0
    else:
        print('ERROR: You cannot use this program on '+platform.system()+'.')
        print('ERROR: Program will exit in 5 secounds')
        time.sleep(5)
        exit()
    # do not touch this
    data = ''
    m3u8get = "https://pwn.sh/tools/streamapi.py"
    p = compile("{}.py")
    result = p.parse(os.path.basename(__file__))
    username = result[0]
    # ============================== fix =================================
    # if you use config.json, change True
    IsConfigFileEnabled = True
    ConfigFile = "config.json"

    # If IsConfigFileEnabled = True, You dont have to change this
    sleeptime = 180
    quality_enable = 0 # If 0, automatically best
    quality = 'best'
    mvtarget = "../record/"+username

    # =========================== fix end =================================
    ffmpeg = "ffmpeg"
    if platform.system() == 'Windows':
        if os.getenv('ffmpeg') == None:
            if os.path.isfile('ffmpeg.exe'):
                ffmpeg = 'ffmpeg.exe'
            elif os.path.isfile('bin/ffmpeg.exe'):
                ffmpeg = 'bin\\ffmpeg.exe'
            else:
                url = "https://raw.githubusercontent.com/TwitchDarkBot/TDBRecordSystem/master/bin/ffmpeg.exe"
                f = open("ffmpeg.exe", "wb")
                res = requests.get(url)
                f.write(res.content)
                f.close
                ffmpeg = "ffmpeg.exe"
        else:
            ffmpeg = "ffmpeg"

    # Do not fix this
    data = {"m3u8get": m3u8get, "username": username, "sleeptime": sleeptime, "quality_enable": quality_enable, "quality": quality, "mvtarget": mvtarget, "ffmpeg": "ffmpeg"}


    if IsConfigFileEnabled == True:
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Reading Config File')
        fl = open(ConfigFile,'r')
        f = json.load(fl)
        data['sleeptime'] = f['sleeptime']
        if f['username_enable'] == 1:
            data['username'] = f['username']
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Starting the program named with '+f['username'])
        elif f['username_enable'] == 0:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Starting the program named with '+username+'.py')
        else:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown username_enabled')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Please fill in with 0, 1')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Program will exit in 5 secounds')
            time.sleep(5)
            exit()


        if f['quality_enable'] == 1:
            data['quality_enable'] = f['quality_enable']
            data['quality'] = f['quality']
        elif f['quality_enable'] == 0:
            nul = 0
        else:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown quality_enable')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Please fill in with 0, 1')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Program will exit in 5 secounds')
            time.sleep(5)
            exit()


        if f["mvtarget_enable"] == 1:
            data['mvtarget'] = f['mvtarget']
        elif f['mvtarget_enable'] == 0:
            nul = 0
        else:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown mvtaget_enable')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Please fill in with 0, 1')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Program will exit in 5 secounds')
            time.sleep(5)
            exit()
    
    if os.path.isdir(mvtarget):
        nul = 0
    else:
        commandline = 'mkdir '+mvtarget
        os.system(commandline)

    # done
    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Set streamer as '+data['username'])
    cont = False
    main(data, cont)
