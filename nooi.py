import APIhandler
from rich.console import Console
from rich.table import Table

# 这里是主逻辑，主应用程序

console = Console()

console.print("即将刷新token，请稍候", style="bright_black")
API = APIhandler.APIs()
path = APIhandler.PATH()
DriveType = API.get_drive()["driveType"]


def launcher():
    """应用启动器."""
    console.print(
        "欢迎来到Nooi," +
        API.get_profile(),  # 用户名
        style='blue',
        justify='center')
    console.print("您使用的是" + DriveType + "类型的Onedrive", style='blue')

    while True:
        Render.main_loop()  # Render是实例，render是类
    # console.print(API.analyze(API.list_file()))


def bootstrap():
    """启动时运行的代码."""
    API.check_token()
    launcher()


class render:
    """通过rich库来渲染界面."""

    def __init__(self):
        self.origin_data = dict()

    def main_loop(self):
        """主循环，不断执行，流程如下.
        1.打印出文件列表.
        2.打印出在当前目录可进行的操作（上传）.
        3.用户选中项目，检查它是文件还是文件夹，并展示对应操作。
        4.操作完成，返回，再次打印列表.
        """
        self.print_files()
        self.base_action()

    def print_files(self):
        """将文件列表打印出来."""
        global all_file
        if path.path == "":
            now_path = "/"
        else:
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
                type_of_object = "文件"
            else:
                type_of_object = "文件夹"
            size = self.hum_convert(resp['size'])
            files_table.add_row(str(num), type_of_object, name, size)
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
            if value <= 1024:
                return str(value) + "B"
            value = value / size

    def base_action(self):
        """在一个文件夹内，即使不选中文件也能执行的操作"""
        global all_file

        def deeper(name):
            """说明是向下移动的."""
            if self.origin_data[name].get('file'):
                path.goinfolder("/" + name)
                self.FileActions(name)
                path.upfolder()
            else:
                path.goinfolder("/" + name)

        print("[a]进入一个项目页")
        print("[b]新建文件夹")
        if path.path != "":
            print("[c]返回上一级目录。")
        print("请填写选项字母:")
        choice = input().lower()
        if choice == "a":
            print("请填入项目序号")
            try:
                num = int(input())
                file_num = num - 1
                name = all_file[file_num]
                deeper(name)
            except IndexError:
                print("您输入的数字超范围了。")
                self.base_action()
            except ValueError:
                print("请输入一个数字。")
                self.base_action()
        elif choice == "c":
            path.upfolder()
        elif choice == "b":
            foldername = input("请键入文件夹名（若已存在自动改名）")
            parent_item_id = self.origin_data[all_file[0]
                                              ]["parentReference"]["id"]
            # print(API.new_folder(foldername, parent_item_id))
            console.print("已创建为" + API.new_folder(foldername,
                                                  parent_item_id)["name"], style="blue")

        else:
            print("请检查填写格式是否有误，或者填错了。")
            self.base_action()

    def FileActions(self, name):
        """文件的相关操作"""
        resp = self.origin_data[name]
        id = self.origin_data[name]["id"]
        console.print(name, justify="center")
        console.print("在线链接" + resp["webUrl"], style="blue")
        console.print("大小：" + self.hum_convert(resp['size']), style="blue")
        console.print("由 "+resp["createdBy"]["user"]
                      ["displayName"]+"创建", style="blue")

        print("[a]获取下载链接")
        print("[b]获取原响应")
        print("[c]删除")
        print("[d]返回")
        print("请选择功能")
        choice = input().lower()
        if choice == "a":
            console.print(
                "下载链接是:" +
                self.origin_data[name]["@microsoft.graph.downloadUrl"],
                style="blue")
            print("1.尝试转换为pdf")
            print("2.完成")
            choice = input()
            if choice == "1":
                resp = API.convert_download(id)
                if resp.status_code == 200:
                    print("已转化")
                    console.print("链接是:" + resp.url, style="blue")
                else:
                    print("不支持转换，可转换格式请见https://docs.microsoft.com/zh-cn/graph/api/driveitem-get-content-format?view=graph-rest-1.0&tabs=http")
            elif choice == "2":
                pass
            else:
                print("无此选项")
        elif choice == "b":
            console.print(self.origin_data[name])
        elif choice == "d":
            pass
        elif choice == "c":
            code = API.delete(id)
            if code == 204:
                console.print("删除成功!", style="red")
            else:
                print("遇到错误")
        else:
            print("请检查填写格式是否有误，或者填错")


Render = render()
bootstrap()
