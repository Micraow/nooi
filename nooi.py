import APIhandler
from rich.console import Console
from rich.table import Table

# 这里是主逻辑，主应用程序

console = Console()

console.print("即将刷新token，请稍候", style="bright_black")
API = APIhandler.APIs()
path = APIhandler.PATH()


def launcher():
    """应用启动器."""
    console.print(
        "欢迎来到Nooi," +
        API.get_profile(),
        style='blue',
        justify='center')  # TO-DO 后面应该加用户名的
    console.print(API.analyze(API.list_file()))


def bootstrap():
    """启动时运行的代码."""
    API.check_token()
    launcher()


bootstrap()


class render:
    """通过rich库来渲染界面."""

    def __init__(self):
        pass

    def main_loop(self):
        """主循环，会一直运行."""
        now_path = path.path
        files_table = Table(title="你的位置"+path.path)
        files_table.add_column("类型",justify="left",style="green")
        files_table.add_column("文件名")
