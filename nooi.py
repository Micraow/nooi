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
    Render.main_loop()  # Render是实例，render是类
    # console.print(API.analyze(API.list_file()))


def bootstrap():
    """启动时运行的代码."""
    API.check_token()
    launcher()


class render:
    """通过rich库来渲染界面."""

    def __init__(self):
        self.origin_data = ""

    def main_loop(self):
        """主循环，不断执行，流程如下.
        1.打印出文件列表.
        2.打印出在当前目录可进行的操作（上传）.
        3.用户选中项目，检查它是文件还是文件夹，并展示对应操作。
        4.操作完成，返回，再次打印列表.
        """
        self.print_files()

    def print_files(self):
        """将文件列表打印出来."""
        now_path = path.path
        all_file = []
        files_table = Table(title="你的位置" + now_path, style="yellow underline")
        files_table.add_column("序号", justify="center", style="red bold")
        files_table.add_column("类型", justify="left", style="green")
        files_table.add_column("名称", style="cyan")
        files_table.add_column("体积", style="blue", justify="center")
        self.origin_data = API.analyze(API.list_file(path.path))
        for name, resp in self.origin_data.items():
            all_file.append(name)
            num = all_file.index(name) + 1
            if self.origin_data[name].get('file'):
                type_of_file = "文件"
            else:
                type_of_file = "文件夹"
            size = self.hum_convert(resp['size'])
            files_table.add_row(str(num), type_of_file, name, size)
        console.print(files_table)

    @staticmethod
    def hum_convert(value):
        """加上尺寸单位，使人类可读，输入以字节为单位."""
        units = ["KB", "MB", "GB", "TB", "PB"]
        size = 1024
        for i in range(len(units)):
            if (value / size) < 1024 and (value / size) >= 1:
                value = value / size
                return str(round(value, 2)) + units[i]
            elif value <= 1024:
                return str(value) + "B"
            value = value / size


Render = render()
bootstrap()
