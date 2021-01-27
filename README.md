# Nooi
Not Only Onedrive Index 不只是索引，更是管理器。

![Nooi logo](https://cdn.jsdelivr.net/gh/Micraow/pics@master/nooi.png)

Github 地址:[Nooi](https://github.com/Micraow/nooi)

Nooi是一个Onedrive 资源管理器，是一个命令行工具，不只列出Onedrive 文件，更可上传，下载，删除等，争取做一个完整的管理器。

## 状态

[![DeepSource](https://deepsource.io/gh/Micraow/nooi.svg/?label=active+issues&show_trend=true)](https://deepsource.io/gh/Micraow/nooi/?ref=repository-badge)

[![DeepSource](https://deepsource.io/gh/Micraow/nooi.svg/?label=resolved+issues&show_trend=true)](https://deepsource.io/gh/Micraow/nooi/?ref=repository-badge)

## 警告
由于微软政策的改变：

>自 2020 年 11 月 9 日起，最终用户将不再能够同意未经认证的发布者新注册的多租户应用。

部分用户可能无法登陆我们预置的应用ID,我已尝试申请MPN ID，却失败了。然而我测试的过程中发现貌似没有出现这个问题，如果有人出问题的话可以在issue里提一下，我看看怎么解决

## 特点与适用场景

1.通过Microsoft Graph API 进行操作，速度有所加快。
2.可以获取下载直链，便于分享。
3.可以通过API实现官方软件与网页版没有的功能，如：获取websocket订阅，查找变化项等。
4.体积小巧，不占空间。
5.全平台支持。官方应用只有Android , IOS , Windows.
6.命令行操作，可与其它服务结合，而且 *比较酷*

## TODO

1. 多线程后台刷新令牌。
2. 列出文件。
3. 删除文件。
4. 生成下载链接。
5. ……

## 文档

文档列表:

[Microsoft Graph](https://docs.microsoft.com/zh-cn/graph/api/resources/onedrive?view=graph-rest-1.0)

[Drive Item相关](https://docs.microsoft.com/zh-cn/graph/api/resources/driveitem?view=graph-rest-1.0)

自述文件原文链接: [Micraow Blog](https://msblog.ml/nooi-readme/index.html)

## 最后

由于比较忙，可能更新慢，请大家谅解，支持，谢谢！
有问题请提issues ，我争取快回复，也欢迎pull requests.
