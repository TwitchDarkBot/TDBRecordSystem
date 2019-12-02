import json
import shutil
import os
import platform
import sys
import time
from requests import get

if __name__ == "__main__":
    # Check setup_username.py
    if os.path.isfile('./setup_username.py'):
        nul = 0
    else:
        print('ERROR: No setup_username.py')
        print('ERROR: Program will be exit in 5 secounds')
        time.sleep(5)
        exit()
        
    shmake = 0
    makepm2 = 0
    now = os.getcwd()
    plat = platform.system()
    # ffmpeg scan

    if plat == 'windows':
        if os.getenv('ffmpeg') == 'None':
            if os.path.isfile('./ffmpeg.exe'):
                ffmpeg = './ffmpeg.exe'
            elif os.path.isfile('../ffmpeg.exe'):
                ffmpeg = './ffmpeg.exe'
            elif os.path.isfile('./bin/ffmpeg.exe'):
                ffmpeg = './bin/ffmpeg.exe'
            else:
                print('WARN: Cannot find ffmpeg. Do you want to download it?')
                q = 'y'
                q = input('(Default Y [Y, n]): ')

                if q == 'y':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close()
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'Y':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close()
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'yes':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close()
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'Yes':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close()
                    ffmpeg = "./ffmpeg.exe"
                else:
                    print('ERROR: You have to download ffmpeg to use TDBRecordSystem')
                    print('ERROR: Exit in 5 secounds')
                    time.sleep(5)
                    exit()
        else:
            ffmpeg = 'ffmpeg'
    elif plat == 'Linux':
        if os.getenv('ffmpeg') == 'None':
            print('WARN: Cannot find ffmpeg. Do you want to install it?')
            q = 'y'
            q = input("(Default Y[Y,n]): ")
            if q == 'y':
                while True:
                    print("INFO: Select your linux build")
                    print("[1] Debian, Ubuntu")
                    print("[2] RHEL(Redhat, Oracle linux, Centos)")
                    q = 'no'
                    q = int(input("[1, 2]: "))
                    if q == 1:
                        lin = 1
                        break
                    elif q == 2:
                        lin = 2
                        break
                    else:
                        nul = 0
            elif q == 'Y':
                while True:
                    print("INFO: Select your linux build")
                    print("[1] Debian, Ubuntu")
                    print("[2] RHEL(Redhat, Oracle linux, Centos)")
                    q = 'no'
                    q = int(input("[1, 2]: "))
                    if q == 1:
                        lin = 1
                        break
                    elif q == 2:
                        lin = 2
                        break
                    else:
                        nul = 0
            elif q == 'yes':
                while True:
                    print("INFO: Select your linux build")
                    print("[1] Debian, Ubuntu")
                    print("[2] RHEL(Redhat, Oracle linux, Centos)")
                    q = 'no'
                    q = int(input("[1, 2]: "))
                    if q == 1:
                        lin = 1
                        break
                    elif q == 2:
                        lin = 2
                        break
                    else:
                        nul = 0
            elif q == 'Yes':
                while True:
                    print("INFO: Select your linux build")
                    print("[1] Debian, Ubuntu")
                    print("[2] RHEL(Redhat, Oracle linux, Centos)")
                    q = 'no'
                    q = int(input("[1, 2]: "))
                    if q == 1:
                        lin = 1
                        break
                    elif q == 2:
                        lin = 2
                        break
                    else:
                        nul = 0
            else:
                print('ERROR: You have to download ffmpeg to use TDBRecordSystem')
                print('ERROR: Exit in 5 secounds')
                time.sleep(5)
                exit()

            if lin == 1:
                command = "sudo apt-get update"
                os.system(command)
                command = "sudo apt-get install ffmpeg -y"
                os.system(command)
                print('ffmpeg installation finished.')
                ffmpeg = 'ffmpeg'
            elif lin == 2:
                if os.getenv("git") == 'None':
                    command = "sudo yum -y install git"
                    os.system(command)
                if os.getenv("make") == 'None':
                    command = "sudo yum -y groupinstall 'Development Tools'"
                    os.system(command)
                command = "git clone https://github.com/FFmpeg/FFmpeg.git"
                os.system(command)
        else:
            ffmpeg = 'ffmpeg'

    # Check JSON File
    f = open('config.json', 'w')
    conf_js = {"username_enable": 0, "username": "streamer", "quality_enable": 0, "quality": "best", "mvtarget_enable": 0, "mvtarget": "../Video", "sleeptime": 180, "ffmpeg": ffmpeg}
    json.dump(conf_js, f, indent="\t")
    f.write
    f.close


    #pm2
    if plat == 'Windows':
        print('WARN: Windows cannot use pm2. SKIP.')
    elif plat == 'Linux':
        while True:
            print('INFO: [1] Use PM2')
            print('INFO: [2] Just copy file')
            mksh = int(input('[1, 2]: '))
            if mksh == 1:
                pm2a = 0
                shmake = 1
                if os.path.isfile('./start_pm2.sh'):
                    pm2file = './start_pm2.sh'
                    search = 1
                elif os.path.isfile('../start_pm2.sh'):
                    pm2file = '../start_pm2.sh'
                    search = 1
                else:
                    search = 0
                    makepm2 = 1

                if search == 1:
                    while True:
                        print('INFO: [1] Delete previous file and make new file')
                        print('INFO: [2] Fix previous file')
                        question = int(input('[1, 2]: '))
                        if question == 1:
                            os.system('rm '+pm2file)
                            search = 0
                            makepm2 = 1
                            question = ''
                            break
                        elif question == 2:
                            pm2a = 1
                            f = open(pm2file,'r')
                            lines = f.readlines()
                            f.close()
                            f = open(pm2file,'w')
                            f.writelines([item for item in lines[:-1]])
                            f.close()
                            break
                        else:
                            print('WARN: Please write down 1, 2')
                if makepm2 == 1:
                    while True:
                        print('INFO: [1] Create script file on this directory')
                        print('INFO: [2] Create script file upper directory')
                        question = int(input('[1, 2]: '))
                        if question == 1:
                            pm2file = './start_pm2.sh'
                            f = open(pm2file, 'a')
                            f.write('cd '+now+'\n')
                            f.close
                            pm2a = 1
                            break
                        elif question == 2:
                            pm2file = '../start_pm2.sh'
                            f = open(pm2file, 'a')
                            f.write('cd '+now+'\n')
                            f.close
                            pm2a = 1
                            break
                        else:
                            print('WARN: Please write down 1, 2')
                if pm2a == 1:
                    break
            elif mksh == 2:
                shmake = 0
                break
            else:
                print('WARN: Please write down 1, 2')

    print('INFO: To exit, type exit')
    while True:
        streamer = input('STREAMER NAME: ')
        if streamer == 'exit':
            if shmake == 1:
                f = open(pm2file, 'a')
                f.write('exit')
                f.close
                print('INFO: Closing File OK')
            os.system('chmod 775 '+pm2file)
            print('INFO: EXIT OK')
            exit()
        shutil.copy("setup_username.py", streamer+'.py')
        print('INFO: COPY '+streamer+' OK')
        if shmake == 1:
            f = open(pm2file, 'a')
            f.write('pm2 start -x --interpreter /bin/python3 '+streamer+'.py\n')
            print('INFO: PM2 Write OK')
            f.close
