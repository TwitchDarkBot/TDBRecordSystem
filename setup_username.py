import requests
import json
import os
import time
from parse import compile
import subprocess

def main(data, cont):
    # Repeat while KeyboardInterrupt
    while True:
        # Reset data
        gdata = ''
        commandline = ''
        res = ''
        m3u8id = ''
        quality = ''
        if cont == False:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Loading API')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'TDB Sync')
            # TDB sync

            # TDB SYNC IS NOT READY.

            # TDB sync end
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+"Getting "+data["username"]+"'s m3u8 data")
            res = requests.get(data["m3u8get"]+"?url=twitch.tv/"+data["username"]) # request streamer is streaming, m3u8 id
            gdata = res.json() # save json
        if gdata["success"] == True: # If streamer is streaming
            if cont == False:
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+data["username"]+' is streaming.')
            # json parsing
            if data['quality_enable'] == 1:
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
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Setting the quality to '+quality)
            fhname = data["username"]+"-"+time.strftime('%Y-%m-%d.%Hh%Mm%Ss', time.localtime(time.time()))
            commandline = "streamlink "+m3u8id+" best -o '"+fhname+"-recording.mp4'"
            #subprocess.run([commandline])
            os.system(commandline) # streamlink start
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'moving the file named "'+fhname+'".mp4')
            if data['fix'] == 1: # If fix is true
                commandline = "ffmpeg -err_detect ignore_err -i "+fhname+"-recording.mp4 -c copy ./"+fhname+".mp4"
                #subprocess.run([commandline])
                os.system(commandline)
                os.remove(fhname+'recording.mp4')
                commandline = "mv "+fhname+".mp4 "+data["mvtarget"]+"/"+fhname+".mp4"
                #subprocess.run([commandline])
                os.system(commandline)

            elif data['fix'] == 0:
                commandline = "mv "+fhname+"-recording.mp4 "+data["mvtarget"]+"/"+fhname+".mp4"
                #subprocess.run([commandline])
                os.system(commandline)
            
            # Check Streamer is streaming
            res = requests.get(data["m3u8get"]+"?url=twitch.tv/"+data["username"]) # request streamer is streaming, m3u8 id
            gdata = res.json() # save json
            if gdata['success'] == True:
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: '+'Restarting the record')
                cont = True
            else:
                cont = False

        else: # Streamer is not streaming
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: '+data["username"]+' is not streaming')
            cont = False
        if cont == False:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'sleep', data["sleeptime"])
            time.sleep(data["sleeptime"])
        elif cont == True:
            cont = True



# ===================================================== MAIN


if __name__ == "__main__":
    # do not touch this
    data = ''
    m3u8get = "https://pwn.sh/tools/streamapi.py"
    p = compile("{}.py")
    result = p.parse(os.path.basename(__file__))
    username = result[0]
    # fix this

    # if you use config.json, change True
    IsConfigFileEnabled = True
    ConfigFile = "config.json"

    # If IsConfigFileEnabled = True, You dont have to change this
    sleeptime = 180
    quality_enable = 0 # If 0, automatically best
    quality = 'best'
    mvtarget = "../record/"+username
    fix = 0

    # Do not fix this
    data = {"m3u8get": m3u8get, "username": username, "sleeptime": sleeptime, "quality_enable": quality_enable, "quality": quality, "mvtarget": mvtarget, "fix": fix}

    if fix == 1:
        nul = 0
    elif fix == 0:
        nul = 0
    else:
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown fix')
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Please fill in with 0, 1')
        print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Program will exit in 5 secounds')
        time.sleep(5)
        exit()

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


        if f["fix"] == 1:
            data['fix'] = 1
        elif f['fix'] == 0:
            data['fix'] = 0
        else:
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Unknown fix')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Please fill in with 0, 1')
            print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: '+'Program will exit in 5 secounds')
            time.sleep(5)
            exit()

    # done
    print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'INFO: '+'Set streamer as '+data['username'])
    cont = 0
    main(data, cont)

