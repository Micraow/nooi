import tokens
import requests
import json
import threading
import time

token = tokens.AUTH("66f884d4-0c48-48eb-8753-43524e18830f",
                    "7vSsDNnV6i2snIp~2BDQ_-cc.jb-IPR2O4")  # 此时会自动检查有无登陆。

endpoint = "https://graph.microsoft.com/v1.0"


class APIs:
    """本程序的核心，与Microsoft Graph交互，获取API端点上的json数据."""

    def __init__(self):
        token.refresh_acc_tk()
        self.headers = {
            'Authorization': 'Bearer ' + token.acc_tk,
            'Content-Type': 'application/json'
        }
        self.origin_resp = ""

    def check_token(self):
        """载入自动刷新token的线程."""
        # 每过3599秒，access token会过期,所以获取令牌后3585秒就刷新
        TokenreFresher = threading.Thread(
            target=self.refresh_timer, daemon=True)
        TokenreFresher.start()

    @staticmethod
    def refresh_timer():
        """刷新token的函数，被check_token作为多线程target调用."""
        while True:
            token.refresh_acc_tk()
            time.sleep(3585)

    def list_file(self, path=""):
        """用于列出目录下的子项."""
        if path == "":
            url = endpoint + "/me/drive/root/children"
        else:
            url = endpoint + "/me/drive/root:" + path + ":/children"
        # print(url)
        self.origin_resp = requests.get(url, headers=self.headers)
        # print(self.origin_resp.text)
        return self.origin_resp.text

    def get_profile(self):
        """获取配置文件，主要是用户名."""
        url = endpoint + "/me"
        resp = requests.get(url, headers=self.headers).text
        resp2 = json.loads(resp)
        try:
            return resp2['displayName']
        except BaseException:
            print(str(resp2))

    @staticmethod
    def analyze(origin_resp):
        """将响应中的数据解析出来，以便后续使用."""
        listOffiles = {}
        json_resp = json.loads(origin_resp)
        for item in json_resp['value']:
            listOffiles[item["name"]] = item
        return listOffiles

    def get_drive(self):
        """用于获取驱动器项目，主要是判断Onedrive类型"""
        url = endpoint + "/me/drive"
        resp = requests.get(url, headers=self.headers).text
        resp2 = json.loads(resp)
        return resp2

    def new_folder(self, foldername, parent_item_id=''):
        """用于新建文件夹，需要提供父文件夹的id"""
        if parent_item_id == '':  # 在根目录可不提供
            url = endpoint + "/me/drive/root/children"
        else:
            url = endpoint + "/me/drive/items/" + parent_item_id + "/children"
        data = {
            "name": foldername,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename",
        }
        data = json.dumps(data, ensure_ascii=False)
        resp = requests.post(url=url, headers=self.headers, data=data).text
        resp2 = json.loads(resp)
        return resp2

    def convert_download(self, id):
        """部分文件可转换为PDF再下载，详见https://developer.microsoft.com/zh-cn/graph/graph-explorer ."""
        url = endpoint + "/me/drive/items/" + id + "/content?format=pdf"
        resp = requests.get(
            url=url,
            headers=self.headers,
            allow_redirects=False)
        # print(resp.text)
        # print(resp.status_code)
        return resp

    def delete(self, id):
        """删除选定文件."""
        url = endpoint + "/me/drive/items/" + id
        resp = requests.delete(url=url, headers=self.headers)
        return resp.status_code

    def rename(self, id, newname):
        """重命名文件或文件夹"""
        url = endpoint + "/me/drive/items/" + id
        data = {
            "name": newname
            }
        resp = requests.patch(url=url, headers=self.headers, json=data)
        return resp

class PATH:
    """处理路径，提供当前路径，上一级，并可在进入子目录时将文件夹名添加到路径."""

    def __init__(self):
        self.path = ""

    def upfolder(self):
        """向上一级."""
        cut_path = self.path.split("/")
        path_list = cut_path[:-1]
        strTocut = "/"
        self.path = strTocut.join(path_list)

    def goinfolder(self, name):
        """在路径后加上name(加上的路径就好了)但有格式要求:folder/folder2,即在最后一级的名称后不加斜杠，可跳多级."""
        self.path = self.path + name
