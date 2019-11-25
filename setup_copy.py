import shutil
import os
import platform
import sys

if __name__ == "__main__":
    shmake = 0
    makepm2 = 0
    now = os.getcwd()
    plat = platform.system()
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
                            f = open("start_pm2.sh")
                            lines = f.readlines()
                            f.close()
                            f = open("start_pm2.sh",'w')
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
                            os.system('touch ./start_pm2.sh')
                            pm2file = './start_pm2.sh'
                            f = open(pm2file, 'a')
                            f.write('cd '+now+'\n')
                            f.close
                            pm2a = 1
                            break
                        elif question == 2:
                            os.system('touch ../start_pm2.sh')
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
                print('WARN: Please wrute down 1, 2')

    print('INFO: To exit, type exit')
    while True:
        streamer = input('STREAMER NAME: ')
        if streamer == 'exit':
            if shmake == 1:
                f = open(pm2file, 'a')
                f.write('exit')
                f.close
                print('INFO: Closing File OK')
            print('INFO: EXIT OK')
            exit()
        shutil.copy("setup_username.py", streamer+'.py')
        print('INFO: COPY '+streamer+' OK')
        if shmake == 1:
            f = open(pm2file, 'a')
            f.write('pm2 start -x --interpreter /bin/python3 '+streamer+'.py\n')
            print('INFO: PM2 Write OK')
            f.close
