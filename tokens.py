from urllib.parse import parse_qsl, urlsplit, quote
import requests
import json


class AUTH:
    """获取令牌,并刷新.
    :param acc_tk: access token
    :param ref_tk: refresh token
    """

    def __init__(
            self,
            appid,
            appsc,
            scope="offline_access Files.Read.All Files.Read.All Files.ReadWrite Files.ReadWrite.All profile openid"):
        self.cliend_id = appid
        self.client_secret = appsc
        self.scope = scope
        try:
            with open('token.json', mode='r') as ori_token:
                all_date = json.load(ori_token)
                self.acc_tk = all_date["access_token"]
                self.ref_tk = all_date["refresh_token"]
        except FileNotFoundError:
            fd = open("token.json", mode="w", encoding="utf-8")
            fd.close()
            print('未登录！\n')
            self.get_code()
            self.qsl_code()
            self.access_token()
            self.save_tokens()
            self.load_tokens()

    def get_code(self):
        """获取长地址."""
        scopes = quote(self.scope)
        self.backsite = input(
            "打开此链接:  https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=" +
            self.cliend_id +
            "&response_type=code&redirect_uri=http://localhost&response_mode=query&scope=" +
            scopes +
            "&state=200  然后将localhost开头的地址栏中地址粘贴到这里:")

    def access_token(self):
        """发送请求."""
        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': self.cliend_id,
            'scope': self.scope,
            'code': self.code,
            'redirect_uri': 'http://localhost',
            'grant_type': 'authorization_code',
            'client_secret': self.client_secret
        }
        self.r = requests.post(url, data=data, headers=headers)

    def qsl_code(self):
        """提取code."""
        self.code = dict(parse_qsl(urlsplit(self.backsite).query)).get('code')

    def save_tokens(self):
        """将access_token和refresh_token写入文件."""
        with open('token.json', mode='w') as token_recorder:
            data2 = json.loads(self.r.text)
            self.acc_tk = data2["access_token"]
            self.ref_tk = data2["refresh_token"]
            data3 = json.dumps(data2, sort_keys=True,
                               indent=4, separators=(',', ':'))
            token_recorder.write(data3)

    def load_tokens(self):
        """加载获取的access_token和refresh_token."""
        with open('token.json', mode='r') as ori_token:
            all_date = json.load(ori_token)
            self.acc_tk = all_date["access_token"]
            self.ref_tk = all_date["refresh_token"]

    def refresh_acc_tk(self):
        """刷新访问令牌."""
        url = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        try:
            data = {
                'client_id': self.cliend_id,
                'scope': self.scope,
                'refresh_token': self.ref_tk,
                'redirect_uri': 'http://localhost',
                'grant_type': 'refresh_token',
                'client_secret': self.client_secret
            }
            self.r = requests.post(url, data=data, headers=headers)
            self.save_tokens()
        except AttributeError:
            self.load_tokens()
            self.refresh_acc_tk()
