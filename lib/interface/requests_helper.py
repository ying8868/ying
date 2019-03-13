import requests as req
from requests.adapters import HTTPAdapter
def get(url):
    s = req.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    return s.get(url,timeout=(5,10))
class httphelper(object):
    def get(self,url):
        s = req.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        return s.get(url,timeout=(5,10))