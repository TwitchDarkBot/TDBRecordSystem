# This code is based on tutorial by slicktechies modified as needed to use oauth token from Twitch.
# You can read more details at: https://www.junian.net/2017/01/how-to-record-twitch-streams.html
# original code is from https://slicktechies.com/how-to-watchrecord-twitch-streams-using-livestreamer/

import requests
import os
import time
import json
import sys
import subprocess
import datetime
import getopt
from parse import compile
import tdbclient

class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.client_id = "jzkbprff40iqj646a697cyrvl0zt2m6" # don't change this
        # get oauth token value by typing `streamlink --twitch-oauth-authenticate` in terminal
        self.oauth_token = "agt3kgn1gb8epuccat2zfyma1y3ijk"
        self.ffmpeg_path = 'ffmpeg'
        self.refresh = 20.0
        self.root_path = "../Videos"
        
        # user configuration
        p = compile("{}.py")
        result = p.parse(os.path.basename(__file__))
        self.username = result[0]
        self.quality = "best"
        streamer = self.username
        self.tdblogger = tdbclient.client(streamer)

    def run(self):
        # path to recorded stream
        self.recorded_path = os.path.join(self.root_path, "recorded", self.username)

        # path to finished video, errors removed
        self.processed_path = os.path.join(self.root_path, "processed", self.username)

        # create directory for recordedPath and processedPath if not exist
        if(os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)
        if(os.path.isdir(self.processed_path) is False):
            os.makedirs(self.processed_path)

        # make sure the interval to check user availability is not less than 15 seconds
        if(self.refresh < 15):
            print("Check interval should not be lower than 15 seconds.")
            self.refresh = 15
            print("System set check interval to 15 seconds.")
        
        # fix videos from previous recording session
        try:
            video_list = [f for f in os.listdir(self.recorded_path) if os.path.isfile(os.path.join(self.recorded_path, f))]
            if(len(video_list) > 0):
                print('Fixing previously recorded files.')
            for f in video_list:
                recorded_filename = os.path.join(self.recorded_path, f)
                print('Fixing ' + recorded_filename + '.')
                try:
                    subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', os.path.join(self.processed_path,f)])
                    os.remove(recorded_filename)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)

        print("Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality.")
        self.loopcheck()

    def check_user(self):
        # 0: online, 
        # 1: offline, 
        # 2: not found, 
        # 3: error
        self.tdblogger.comment = 2
        self.tdblogger.send()
        
        url = 'https://api.twitch.tv/kraken/streams/' + self.username
        info = None
        status = 3
        try:
            r = requests.get(url, headers = {"Client-ID" : self.client_id}, timeout = 15)
            r.raise_for_status()
            info = r.json()
            if info['stream'] == None:
                self.tdblogger.comment = 4
                status = 1

            else:
                self.tdblogger.comment = 3
                status = 0
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    self.tdblogger.comment = 5
                    status = 2

        self.tdblogger.send()
        return status, info

    def loopcheck(self):
        while True:
            status, info = self.check_user()
            if status == 2:
                print("Username not found. Invalid username or typo.")
                time.sleep(self.refresh)
            elif status == 3:
                print(datetime.datetime.now().strftime("%Hh%Mm%Ss")," ","unexpected error. will try again in 5 minutes.")
                time.sleep(300)
            elif status == 1:
                os.system ('mv ../Videos/processed/'+self.username+'/*.mp4 ../Total')
                time.sleep(self.refresh)
            elif status == 0:
                print(self.username, "online. Stream recording in session.")
                filename = self.username + " - " + datetime.datetime.now().strftime("%Y-%m-%d %Hh%Mm%Ss") + " - " + (info['stream']).get("channel").get("status") + ".mp4"
                
                # clean filename from unecessary characters
                filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])
                
                recorded_filename = os.path.join(self.recorded_path, filename)
                
                # start streamlink process
                subprocess.call(["streamlink", "--twitch-disable-hosting", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality, "-o", recorded_filename])
                print("Recording stream is done. Fixing video file.")
                self.tdblogger.comment = 6
                self.tdblogger.send()
                if(os.path.exists(recorded_filename) is True):
                    try:
                        self.tdblogger.comment = 7
                        self.tdblogger.send()

                        subprocess.call([self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy', os.path.join(self.processed_path, filename)])
                        os.remove(recorded_filename)
                    except Exception as e:
                        print(e)
                else:
                    self.tdblogger.comment = 9
                    self.tdblogger.send()
                    print("Skip fixing. File not found.")
                    
                print("Fixing is done. Going back to checking..")
                self.tdblogger.comment = 8
                self.tdblogger.send()
                time.sleep(self.refresh)

def main(argv):
    twitch_recorder = TwitchRecorder()

    twitch_recorder.tdblogger.comment = 1
    twitch_recorder.tdblogger.send()

    twitch_recorder.run()

if __name__ == "__main__":
    main(sys.argv[1:])