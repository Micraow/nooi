import APIhandler
from rich.console import Console
'''这里是主逻辑，主应用程序.'''

console = Console()

API = APIhandler.APIs()

def launcher():
    '''应用启动器.'''
    console.print("欢迎来到Nooi,"+API.get_profile(),style='blue',justify='center')  # TO-DO 后面应该加用户名的
    console.print(API.analyze(API.list_file()))

def bootstrap():
    '''# 启动时运行的代码.'''
    API.check_token()
    launcher()

bootstrap()

class render:
    """通过rich库来渲染界面."""

    def __init__(self):
        pass
