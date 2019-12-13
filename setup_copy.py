import json
import shutil
import os
import platform
import sys
import time
from requests import get
import string
import random

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
        
    # check can i write the file
    rd = ''
    lng = 1024
    string_pool = string.ascii_letters + string.digits

    for i in range(lng): 
        rd += random.choice(string_pool)
    
    f = open("firewrite", "w")
    f.write(rd)
    f.close
    f = open("firewrite", "r")
    readed = f.read()
    f.close
    os.remove("firewrite")
    if rd == readed:
        nul = 0
    else:
        print("ERROR: No Permission. Please grant permission on this directory")
        print('ERROR: Exit in 5 secounds')
        time.sleep(5)
        exit()
    
    # Check permission upper directory

    rd = ''
    lng = 1024
    string_pool = string.ascii_letters + string.digits

    for i in range(lng): 
        rd += random.choice(string_pool)
    
    f = open("../firewrite", "w")
    f.write(rd)
    f.close
    f = open("../firewrite", "r")
    readed = f.read()
    f.close
    os.remove("../firewrite")
    if rd == readed:
        upperperm = 1
    else:
        print("WARN: No Permission on upper directory.")
        upperperm = 0

    # Check setup_username.py
    if os.path.isfile('./setup_username.py'):
        nul = 0
    else:
        print('WARN: No setup_username.py')
        print('INFO: Downloading setup_username.py')
        url = "https://raw.githubusercontent.com/TwitchDarkBot/TDBRecordSystem/m3u8downloader/setup_username.py"
        f = open("setup_username.py", "wb")
        res = get(url)
        f.write(res.content)
        f.close
        
    shmake = 0
    makepm2 = 0
    now = os.getcwd()
    plat = platform.system()
    # ffmpeg scan

    if plat == 'windows':
        if os.getenv('ffmpeg') == 'None':
            if os.path.isfile('./ffmpeg.exe'):
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
                    f.close
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'Y':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'yes':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close
                    ffmpeg = "./ffmpeg.exe"
                elif q == 'Yes':
                    url = "https://github.com/TwitchDarkBot/TDBRecordSystem/raw/m3u8downloader/bin/ffmpeg.exe"
                    f = open("ffmpeg.exe", "wb")
                    res = get(url)
                    f.write(res.content)
                    f.close
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
                linff = 1
            elif q == 'Y':
                linff = 1
            elif q == 'yes':
                linff = 1
            elif q == 'Yes':
                linff = 1
            else:
                print('ERROR: You have to download ffmpeg to use TDBRecordSystem')
                print('ERROR: Exit in 5 secounds')
                time.sleep(5)
                exit()
            if  linff == 1:
                if "debian" in platform.platform():
                    lin = 1
                elif "ubuntu" in platform.platform():
                    lin = 1
                elif "CentOS" in platform.platform():
                    lin = 2
                elif "redhat" in platform.platform():
                    lin = 2
                elif "oracle" in platform.platform():
                    lin = 2
                else:
                    while True:
                        print("INFO: Select your linux build")
                        print("[1] Debian, Ubuntu (which uses apt-get)")
                        print("[2] RHEL(Redhat, Oracle linux, Centos) (which uses yum)")
                        q = int(input("[1, 2]: "))
                        if q == 1:
                            lin = 1
                            break
                        elif q == 2:
                            lin = 2
                            break
                        else:
                            print('WARN: Please write down 1, 2')
            if lin == 1:
                command = "sudo apt-get update"
                os.system(command)
                command = "sudo apt-get install ffmpeg -y"
                os.system(command)
                print('ffmpeg installation finished.')
                ffmpeg = 'ffmpeg'
            elif lin == 2:
                if os.getenv("make") == 'None':
                    command = "sudo yum -y groupinstall 'Development Tools'"
                    os.system(command)
                url = "http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2"
                f = open("ffmpeg.tar.bz2", "wb")
                res = get(url)
                f.write(res.content)
                f.close
                f = open("setup_ffmpeg.sh","w")
                f.write("tar xjvf ffmpeg-snapshot.tar.bz2\n")
                f.write("cd ffmpeg\n")
                f.write("./configure --disable-x86asm\n")
                f.write("make\n")
                f.write("make install\n")
                f.write("make distclean\n")
                f.write("cd ..\n")
                f.write("rm -rf ffmpeg/\n")
                f.close
                command = "setup_ffmpeg.sh"
                os.system(command)
        else:
            ffmpeg = 'ffmpeg'

    # Check JSON File
    f = open('config.json', 'w')
    conf_js = {"username_enable": 0, "username": "streamer", "quality_enable": 0, "quality": "best", "mvtarget_enable": 0, "mvtarget": "../Video", "sleeptime": 180}
    json.dump(conf_js, f, indent="\t")
    f.write
    f.close


    #pm2
    if plat == 'Windows':
        print('WARN: Windows cannot use pm2. SKIP.')
    elif plat == 'Linux':
        if os.path.isfile('./start_pm2.sh'):
            pm2file = './start_pm2.sh'
            search = 1
        elif os.path.isfile('../start_pm2.sh'):
            if upperperm == 1:
                pm2file = '../start_pm2.sh'
                search = 1
            else:
                search = 0
        else:
            search = 0
            makepm2 = 1

        while True:
            print('INFO: [1] Use PM2')
            print('INFO: [2] Just copy file')
            mksh = int(input('[1, 2]: '))
            if mksh == 1:
                pm2a = 0
                shmake = 1

                if search == 1:
                    while True:
                        print('INFO: [1] Delete previous file and make new file')
                        print('INFO: [2] Fix previous file')
                        question = int(input('[1, 2]: '))
                        if question == 1:
                            os.remove(pm2file)
                            search = 0
                            makepm2 = 1
                            question = ''
                            break
                        elif question == 2:
                            pm2a = 1
                            f = open(pm2file,'r')
                            lines = f.readlines()
                            f.close
                            f = open(pm2file,'w')
                            f.writelines([item for item in lines[:-1]])
                            f.close
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
                            if upperperm == 1:
                                pm2file = '../start_pm2.sh'
                                f = open(pm2file, 'a')
                                f.write('cd '+now+'\n')
                                f.close
                                pm2a = 1
                            else:
                                print("ERROR: No Permission. Please grant permission upper directory")
                                print('ERROR: Exit in 5 secounds')
                                time.sleep(5)
                                exit()
                            break
                        else:
                            print('WARN: Please write down 1, 2')
                if pm2a == 1:
                    break
            elif mksh == 2:
                shmake = 0
                if search == 1:
                    os.remove(pm2file)
                break
            else:
                print('WARN: Please write down 1, 2')
    oad = 0
    print('INFO: To exit, type exit')
    while True:
        streamer = input('STREAMER NAME: ')
        if streamer == 'exit':
            if shmake == 1:
                if oad == 1:
                    f.close
                    print('WARN: Nothing added.')
                    print('WARN: Removing the file'+pm2file)
                    os.remove(pm2file)
                else:
                    f = open(pm2file, 'a')
                    f.write('exit')
                    f.close
                    print('INFO: Closing File OK')
                    os.system('chmod 775 '+pm2file)
            print('INFO: EXIT OK')
            exit()
        elif '!' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '@' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '#' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '$' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '%' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '^' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '&' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '*' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif '(' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif ')' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        elif ' ' in streamer:
            print("WARN: Unknown username:"+streamer)
            print("WARN: Not added")
        else:
            oad = 1
            shutil.copy("setup_username.py", streamer+'.py')
            print('INFO: COPY '+streamer+' OK')
            if shmake == 1:
                f = open(pm2file, 'a')
                f.write('pm2 start -x --interpreter /bin/python3 '+streamer+'.py\n')
                print('INFO: PM2 Write OK')
                f.close
