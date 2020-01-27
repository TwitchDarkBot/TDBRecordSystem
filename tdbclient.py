class client():
    def __init__(self, streamer):
        self.comment = ''
        self.level = 0
        self.streamer = streamer
        self.levelp = 0

    def send(self):
        import requests
        import json
        import time
        import os
        import platform

        if os.path.isfile('info.json'):
            f = open('info.json', 'r')
        elif platform.system() == 'Windows':
            if os.path.isfile('C:\\srv\\info.json'):
                f = open('C:\\srv\\info.json','r')
            else:
                exit()
        elif platform.system() == 'Linux':
            if os.path.isfile('/srv/info.json'):
                f = open('/srv/info.json','r')
            else:
                exit()
        srvinfo = json.load(f)
        f.close

        server = srvinfo["server"]
        region = srvinfo["region"]
        tocken = srvinfo["key"]
        ip = srvinfo["logserver"]
        resendit = srvinfo["resend"]
        if srvinfo["port"] == "default":
            port = ''
        else:
            port = ':'+srvinfo["port"]

        if srvinfo["ssl"] == "True":
            url = 'https://'+ip+port+'/logging'
        else:    
            url = 'http://'+ip+port+'/logging'

        resend = 0
        while resend < resendit:
            retry = True
            rtn = 1
            if self.level == 10:
                if self.comment == '':
                    return -1
                elif self.levelp == 0:
                    return -1
                else:
                    data = {'header':{'tocken':tocken,'server':server,'region':region},'body':{'date':time.strftime('%Y-%m-%d', time.localtime(time.time())),'time':time.strftime('%H:%M:%S', time.localtime(time.time())),'level':self.level,'comment':self.comment,'streamer':self.streamer,'levelp':self.levelp}}
            else:
                data = {'header':{'tocken':tocken,'server':server,'region':region},'body':{'date':time.strftime('%Y-%m-%d', time.localtime(time.time())),'time':time.strftime('%H:%M:%S', time.localtime(time.time())),'level':self.level,'streamer':self.streamer}}
            res = requests.post(url, json=json.dumps(data))

            if res.text == '0':
                retry = False
                rtn = res
            elif res.text == '1':
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: Auth failed')
                retry = False
                rtn = res
            elif res.text == '2':
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: TDB Client ERROR')
                retry = False
                rtn = res
            elif res.text == '3':
                print(time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'ERROR: International Server Error')
                retry = False
                rtn = res
            elif resend == 3:
                print (time.strftime('[%Y-%m-%d | %H:%M:%S] ', time.localtime(time.time()))+'WARN: CANNOT connect to logging server. Skip')
                retry = False
                rtn = 1
            else:
                resend = resend + 1
                time.sleep(2)
                retry = True
            
            if retry == True:
                retry = True
            else:
                self.comment = 0
                self.level = 0
                return rtn

    def status(self, streamer):
        import requests
        import json

        res = requests.post('http://api.twitchdarkbot.com/status', json=json.dumps({'username': streamer}))

        return res.json()

    def ipc(self):
        import socket
        requests.post('http://api.twitchdarkbot.com/ips', json=json.dumps({'server':'TDB','comment':socket.gethostbyname(socket.gethostname())}))