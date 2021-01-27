import tokens
import threading
"""这里是主逻辑，主应用程序"""

access_token = ""
refresh_token = ""
token = tokens.AUTH("66f884d4-0c48-48eb-8753-43524e18830f",
                    "7vSsDNnV6i2snIp~2BDQ_-cc.jb-IPR2O4")  # 此时会自动检查有无登陆。


def check_token():  # 载入自动刷新token的线程
    global token
    TokenreFresher = threading.Timer(
        3585, token.refresh_acc_tk)  # 每过3599秒，access token会过期
    TokenreFresher.start()


def bootstrap():  # 启动时运行的代码
    pass
