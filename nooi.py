import APIhandler
from rich.console import Console
'''这里是主逻辑，主应用程序.'''

console = Console()

API = APIhandler.APIs()
functs = {
    "1": API.list_file
}

def launcher():
    '''应用启动器.'''
    console.print("欢迎来到Nooi,"+API.get_profile(),style='blue',justify='center')  # TO-DO 后面应该加用户名的
    print("""1.列出文件""")
    choice = input("""请选择(不带".")：""")
    func = functs[choice]
    print(func())


def bootstrap():
    '''# 启动时运行的代码.'''
    API.check_token()
    launcher()

bootstrap()
