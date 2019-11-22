import os

if __file__ == "__main__":
    while True:
        copyfile = input('STREAMER NAME: ')
        if copyfile == 'exit':
            exit()
        commandline = 'cp username.py '+copyfile+'.py'
        os.system(commandline)
        