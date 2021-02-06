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
        all_file = []
        files_table = Table(title="你的位置" + path.path, style="yellow underline")
        files_table.add_column("序号", justify="center", style="red bold")
        files_table.add_column("类型", justify="left", style="green")
        files_table.add_column("名称", style="cyan")
        files_table.add_column("体积", style="blue", justify="center")
        origin_data = API.analyze(API.list_file(path.path))
        for name, resp in origin_data:
            all_file.append(name)
            num = all_file.index(name) + 1
            if origin_data[name].get('file'):
                type_of_file = "文件"
            else:
                type_of_file = "文件夹"
            size = hum_convert(resp['size'])

    def hum_convert(value):
        """加上尺寸单位，使人类可读，输入以字节为单位."""
        units = ["B", "KB", "MB", "GB", "TB", "PB"]
        size = 1024.0
        for i in range(len(units)):
            if (value / size) < 1024.0 and (value / size) >= 1:
                value = value / size
                return value + units[i]
