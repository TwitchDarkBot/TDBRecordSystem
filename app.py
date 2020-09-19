class storage():
    def __init__(self):
        pass

class record():
    def __init__(self):
        pass

    def m3u8(self, streamer):
        import streamlink
        try:
            tmp = streamlink.streams("http://twitch.tv/nocopyrightsounds")
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

    def record(self, name, url):
        filename=


