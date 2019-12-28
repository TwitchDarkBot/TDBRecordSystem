class client():
    def __init__(self, streamer):
        self.comment = 0
        self.streamer = streamer

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

        if self.comment == 4:
            level = 1
        elif self.comment == 9:
            level = 1
        elif self.comment == 5:
            level = 2

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
            data = {'header':{'tocken':tocken,'server':server,'region':region},'body':{'date':time.strftime('%Y-%m-%d', time.localtime(time.time())),'time':time.strftime('%H:%M:%S', time.localtime(time.time())),'level':level,'comment':self.comment,'streamer':self.streamer}}
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