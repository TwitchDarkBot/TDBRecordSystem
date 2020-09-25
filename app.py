class storage():
    def __init__(self):
        self.server = "https://www.twitchdarkbot.com/api/tdb/record/"
        self.region = "R420"
        #from upload import upload
        #self.upload = upload()
        self.record = recmain()
        self.uploadqueue = []
        pass

class dummy(): def __init__(self): pass

class record():
    def __init__(self, storage, streamer, userid):
        from requests import post
        self.storage = storage
        self.streamer = streamer
        self.userid = userid
        self.m3u8()
        self.started = post(self.storage.server+"gettime", json={"id": userid})
        pass

    def m3u8(self):
        import streamlink
        try:
            tmp = streamlink.streams("http://twitch.tv/"+self.streamer)
        except streamlink.exceptions.PluginError as e:
            print(e)
            return None
        except:
            return None
        if "1080p60" in tmp: rtn = tmp["1080p60"].url
        elif "1080p" in tmp: rtn = tmp["1080p"].url
        elif "720p60" in tmp: rtn = tmp["720p60"].url
        elif "720p" in tmp: rtn = tmp["720p"].url
        elif "480p" in tmp: rtn = tmp["480p"].url
        elif "360p" in tmp: rtn = tmp["360p"].url
        elif "160p" in tmp: rtn = tmp["160p"].url
        else: return None
        return rtn
        pass

    def record(self, name, userid, url):
        rtn = post(self.storage.server+"gettime", json={"id": userid})

        filename = name+"-"+time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))+".mp4"

class recmain():
    def __init__(self, storage):
        self.storage = storage
        self.threads = []
        pass

    def main(self):
        from threading import Thread
        rtn = self.get()
        tmp = 0
        for now in rtn:
            if now[2] != self.storage.region: break
            if now[4] == 0: 
                tmp += 1
                break
            elif now[4] == 1: 
                if now[3] != "recording":
                    q = Thread(target=record, args=(self.storage, now[1], now[0],))
                    q.start()
                    self.threads.append(q)
        
        if tmp == len(rtn): self.threads = []
        
        pass
    
    def get(self):
        from requests import get
        rtn = get("http://www.twitchdarkbot.com/api/tdb/record/server/broadlist?region="+str(self.region))
        if rtn.status_code == 200:
            return rtn.json()["list"]
        else:
            return False


    def streamlist(self):
        self.storage


if __name__ == "__main__":
    storage = storage()
    while True:
        storage.record.main()
    pass