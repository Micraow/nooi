import tokens
import requests
import json
import threading
import time

token = tokens.AUTH("66f884d4-0c48-48eb-8753-43524e18830f",
                    "7vSsDNnV6i2snIp~2BDQ_-cc.jb-IPR2O4")  # 此时会自动检查有无登陆。


class APIs:
    '''本程序的核心，与Microsoft Graph交互，获取API端点上的json数据.'''

    def __init__(self):
        self.headers = {
            'Authorization': 'Bearer ' + token.acc_tk
        }

    def check_token(self):
        '''  载入自动刷新token的线程.'''
        token.refresh_acc_tk()
        TokenreFresher = threading.Thread(target=self.refresh_timer,daemon=True)  # 每过3599秒，access token会过期,所以获取令牌后3585秒就刷新
        TokenreFresher.start()

    @staticmethod
    def refresh_timer():
        while True:
            token.refresh_acc_tk()
            time.sleep(3585)

