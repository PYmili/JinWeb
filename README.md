# JinWeb
![JinWeb](https://www.kuko.icu/API/JinWeb/icon.png)
Jin-Web 基于fastapi实现的局域网文件共享

# 作者 PYmili
![PYmili](https://www.kuko.icu/PYmili/img/PYmili_400x400.jpg)
### 官网网址：[kuko.icu](https://www.kuko.icu) 个人博客：[csdn-pymili](https://blog.csdn.net/qq_53280175?spm=1000.2115.3001.5343)

# 使用架构
### 程序使用fastapi框架制作后端, html及css,JavaScript制作前端部分
### 前端的所有样式都在程序文件夹中，可自行更改样式

# 使用方式
### 程序使用命令行方式运行程序，为了方便快捷共享文件

# 正常系统
### windows 10 经过测试运行正常
### linux Ubuntu 正常运行
### linux CentOs 正在测试

# 命令行文档 

~~~
Jin-Web | Version:0.1.1
        可用命令 / Available commands:
                -f/--file=         要共享的文件路径 / File path to share
                -u/--user=         共享文件的用户名，默认为：admin / The user name of the shared file. The default is admin
                -k/--key=          为要共享的文件添加加密秘钥，可不添加 / Add an encryption key to the file to be shared, but do not add it
                -R/--Remove=       要删除的共享文件名字(参数等于 all 时删除所有共享文件)(参数等于log时清除程序日志) / Name of the shared file to be deleted (delete all shared files when the parameter is equal to all)  (clear the program log when the parameter is equal to log)
                -s/--see           查看已共享的所有文件 / View all shared files
                -r/--run           启动共享 / Start sharing
~~~
