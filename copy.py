import os

if __name__ == "__main__":
    while True:
        streamer = input('STREAMER NAME: ')
        if streamer == 'exit':
            exit()
        commandline = 'cp username.py '+streamer+'.py'
        os.system(commandline)
