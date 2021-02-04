import tokens
import requests
import json
import threading
import time

token = tokens.AUTH("66f884d4-0c48-48eb-8753-43524e18830f",
                    "7vSsDNnV6i2snIp~2BDQ_-cc.jb-IPR2O4")  # 此时会自动检查有无登陆。

endpoint = "https://graph.microsoft.com/v1.0"


class APIs:
    '''本程序的核心，与Microsoft Graph交互，获取API端点上的json数据.'''

    def __init__(self):
        self.headers = {
            'Authorization': 'Bearer ' + token.acc_tk
        }

    def check_token(self):
        '''  载入自动刷新token的线程.'''
        token.refresh_acc_tk()
        # 每过3599秒，access token会过期,所以获取令牌后3585秒就刷新
        TokenreFresher = threading.Thread(
            target=self.refresh_timer, daemon=True)
        TokenreFresher.start()

    @staticmethod
    def refresh_timer():
        while True:
            token.refresh_acc_tk()
            time.sleep(3585)

    def list_file(self, path="",callback):
        '''用于列出目录下的子项'''
        url = endpoint+"/me/drive/root:"+path+":/children"
        resp = requests.get(url, headers=self.headers)
        return resp.text
        callback(resp.text)

    def get_profile(self):
        '''获取配置文件，主要是用户名.'''
        url = endpoint+"/me"
        resp = requests.get(url, headers=self.headers).text
        resp2 = json.loads(resp)
        return resp2['displayName']

    def analyze(self, origin_resp):
        """将响应中的数据解析出来，以便后续使用"""
        self.files=[]
        self.foldernames=[]
        json_resp=json.load(origin_resp)
        for items in json_resp['value']:



class PATH:
    '''专用来处理文件路径的类.
        @direct：向上级目录或向下'''

    def __init__(self):
        self.root="/"

    
        



