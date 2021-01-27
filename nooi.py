import APIhandler
'''这里是主逻辑，主应用程序.'''

API = APIhandler.APIs()
def launcher(): 
    '''应用启动器.'''
    print("欢迎来到Nooi,") # TO-DO 后面应该加用户名的

def bootstrap():  
    '''# 启动时运行的代码.'''
    API.check_token()
    launcher()
    
bootstrap()