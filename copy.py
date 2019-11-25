import shutil
import os
import platform

if __name__ == "__main__":
    shmake = 0
    now = os.getcwd()
    plat = platform.system()
    if plat == 'Windows':
        print('Windows cannot use pm2. SKIP.')
    elif plat == 'Linux':
        while True:
            print('[1] Use PM2          [2] Just copy file')
            mksh = input('[1, 2]: ')
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
                        print('[1] Delete previous file and make new file')
                        print('[2] Fox previous file')
                        question = input('[1, 2]: ')
                        if question == 1:
                            os.system('rm '+pm2file)
                            search = 0
                            makepm2 = 1
                            question = ''
                            break
                        elif question == 2:
                            pm2a = 1
                            break
                        else:
                            print('Please write down 1, 2')
                if makepm2 == 1:
                    while True:
                        print('[1] Create script file on this directory')
                        print('[2] Create script file upper directory')
                        question = input('[1, 2]: ')
                        if question == 1:
                            os.system('touch ./start_pm2.sh')
                            pm2file = './start_pm2.sh'
                            f = open(pm2file, 'a')
                            f.write('cd '+now)
                            f.close
                            pm2a = 1
                            break
                        elif question == 2:
                            os.system('touch ../start_pm2.sh')
                            pm2file = '../start_pm2.sh'
                            f = open(pm2file, 'a')
                            f.write('cd '+now)
                            f.close
                            pm2a = 1
                            break
                        else:
                            print('Please write down 1, 2')
                if pm2a == 1:
                    break
            elif mksh == 2:
                shmake = 0
                break
            else:
                print('Please wrute down 1, 2')


    while True:
        streamer = input('STREAMER NAME: ')
        if streamer == 'exit':
            if shmake == 1:
                f = open(pm2file, 'a')
                f.write('exit')
                f.close
            exit()
        shutil.copy("username.py", streamer+'.py')
        if shmake == 1:
            f = open(pm2file, 'a')
            f.write('pm2 start -x --interpreter /bin/python3 '+streamer+'.py')
            f.close