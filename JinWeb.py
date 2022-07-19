# coding=utf-8

import os
import json
import sys
from fileid import fileid
import getopt
import socket

from fastapi import FastAPI, Form
from fastapi import File, UploadFile
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.templating import Jinja2Templates
import uvicorn

import ProgramLog

_PATH_ = os.path.split(__file__)[0]
__Verison__ = str(open(fr"{_PATH_}/Version", "r", encoding="utf-8").read())

if os.path.exists(fr"{_PATH_}/ProgramLog.log"):
    pass
else:
    open(fr"{_PATH_}/ProgramLog.log", "w+", encoding="utf-8")
_Log_ = ProgramLog.ProgramLog(fr"{_PATH_}/ProgramLog.log")
__Share__ = json.loads(open(fr"{_PATH_}/Share.json", "r", encoding="utf-8").read())

def AddShare(filepath, user, key):
    global __Share__
    _Log_.afferent("正常运行 / normal operation", f"添加文件 / Add file: {os.path.split(filepath)[-1]}")
    _Log_.afferent("正常运行 / normal operation", f"操作用户为 / Operation user is: {user}")
    if key:
        __Share__[os.path.split(filepath)[-1]] = {"user":user, "file":filepath, "key":key}
    else:
        __Share__[os.path.split(filepath)[-1]] = {"user":user, "file":filepath, "key":"None"}
    with open(fr"{_PATH_}/Share.json", "w+", encoding="utf-8") as fp:
        fp.write(json.dumps(__Share__))
    _Log_.afferent("正常运行 / normal operation", "添加成功！ / Successfully added!")
    _Log_.afferent("正常运行 / normal operation", f"将密钥共享为 / Share the secret key as: {key}")

def RemoveShare(filename, user):
    global __Share__
    _Log_.afferent("正常运行 / normal operation", f"删除文件 / Delete file: {filename}")
    _Log_.afferent("正常运行 / normal operation", f"操作用户为/ Operation user is: {user}")
    if filename in __Share__.keys():
        if __Share__[filename]['key'] != "None":
            key = input("请输入共享秘钥 / Please enter the shared secret key:")
        else:
            key = __Share__[filename]['key']
        if key == __Share__[filename]['key']:
            os.remove(f"{os.path.split(__file__)[0]}"+__Share__[filename]['file'])
            __Share__.pop(filename)
            with open(fr"{_PATH_}/Share.json", "w+", encoding="utf-8") as fp:
                fp.write(json.dumps(__Share__))
            _Log_.afferent("正常运行 / normal operation", "删除成功！ / Deletion succeeded!")
        else:
            _Log_.afferent("参数错误 / Parameter error", f"秘钥 {key} 错误！ / Secret key {key} error!")
    else:
        _Log_.afferent("参数错误 / Parameter error", f"未找到文件：{filename} / File not found: {filename}")

def DeleteShare(user):
    global __Share__
    _Log_.afferent("正常运行 / normal operation", "删除所有共享文件... / Delete all shared files...")
    _Log_.afferent("正常运行 / normal operation", f"操作用户为/ Operation user is: {user}")
    for key in __Share__.keys():
        _Log_.afferent("正常运行 / normal operation", "\t"+f"{os.path.split(__file__)[0]}"+os.path.split(__Share__[key]['file'])[-1])
        try:
            os.remove(f"{os.path.split(__file__)[0]}"+__Share__[key]['file'])
        except:
            _Log_.afferent("文件错误 / file error", "文件不存在或无法访问，跳过删除文件 / File does not exist or cannot be accessed, skip deleting file")
    __Share__ = {}
    with open(fr"{_PATH_}/Share.json", "w+", encoding="utf-8") as fp:
        fp.write("{}")
    _Log_.afferent("正常运行 / normal operation", "删除成功！ / Deletion succeeded!")

def SeeShare():
    global __Share__
    for key, value in __Share__.items():
        _Log_.afferent("正常运行 / normal operation", f"文件：{key} 操作用户：{value['user']} / File: {key} operation user: {value['user']}")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index(request:Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request":request,
            "Version":__Verison__
        }
    )

@app.get("/app")
async def APP(request:Request):
    return templates.TemplateResponse(
        "app.html",
        {
            'request':request
        }
    )

@app.get("/share")
async def share(request:Request):
    return templates.TemplateResponse(
        'share.html',
        {
            "request":request,
            "Files":__Share__
        }
    )

@app.get("/share_app")
async def share_app(request:Request):
    return templates.TemplateResponse(
        "share_app.html",
        {
            "request":request,
            "Files":__Share__
        }
    )

@app.get("/key_error")
async def Key_Error(request:Request):
    return templates.TemplateResponse(
        "keyerror.html",
        {
            "request":request
        }
    )


@app.post("/verification/{filename}")
async def verification(request:Request, filename, PassWord:str = Form(...)):
    global __Share__
    if str(PassWord) == __Share__[filename]['key']:
        return templates.TemplateResponse(
            "file.html",
            {
                "request":request,
                "file":__Share__[filename]['file']
            }
        )
    else:
        await Key_Error(request)

@app.get("/download_app/{filename}")
async def DownLoadApp(request:Request, filename):
    return templates.TemplateResponse(
        "download_app.html",
        {
            "request":request,
            "filename":filename
        }
    )


@app.get("/download/{filename}")
async def DownLoadFile(request:Request, filename):
    return templates.TemplateResponse(
        "download.html",
        {
            "request":request,
            "filename":filename
        }
    )


def run(Port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    IP = s.getsockname()[0]
    _Log_.afferent("正常运行 / normal operation", f"http://{IP}:8989/")
    _Log_.afferent("正常运行 / normal operation", f"共享文件地址：http://{IP}:8989/share/ | Shared file address: http://{IP}: 8989/share/")
    uvicorn.run(app, host="0.0.0.0", port=Port)

if __name__ == '__main__':
    FILEPATH = "None"
    USERNAME = "admin"
    KEY = False
    PORT = 8989

    try:
        options, args = getopt.getopt(sys.argv[1:], "hf:u:k:R:p:srv", ["help", "file=", "user=", "key=", "Remove=", "prot=", "see", "run", "version"])
    except getopt.GetoptError:
        sys.exit()
    for key, value in options:
        if key in ['-u', '--user']:
            USERNAME = value
        elif key in ['-k', "--key"]:
            KEY = value
        elif key in ['-f', '--file']:
            if os.path.isfile(value):
                Openfile = open(value, "rb")
                FILERD = Openfile.read()
                Openfile.close()
                with open(fr"{_PATH_}/static/file/{os.path.split(value)[-1]}", "wb") as fp:
                    fp.write(FILERD)
                if os.path.exists(fr"{_PATH_}/static/file/{os.path.split(value)[-1]}"):
                    FILEPATH = fr"/static/file/{os.path.split(value)[-1]}"
                else:
                    _Log_.afferent("文件错误 / file error", f"无法添加文件：{value}  / Cannot add file: {value}")
            else:
                _Log_.afferent("文件错误 / file error", f"文件 {value} 不存在！ / The file {value} does not exist!")
        elif key in ['-R', '--Remove']:
            if value == "all":
                DeleteShare(USERNAME)
            elif value == "log":
                open(fr"{_PATH_}/ProgramLog.log", "w+", encoding="utf-8")
                print(fr"已清空日志！ / The log has been cleared!{_PATH_}/ProgramLog.log")
            elif value in __Share__.keys():
                RemoveShare(value, USERNAME)
            else:
                _Log_.afferent("文件错误 / file error", f"未找到共享文件：{value} / Shared file not found: {value}")
        elif key in ['-p', '--prot']:
            try:
                PORT = int(value)
            except ValueError:
                print("请输入端口！ / Please enter the port!")
        elif key in ['-s', '--see']:
            SeeShare()
        elif key in ['-r', '--run']:
            _Log_.afferent("正常运行 / normal operation", "已共享文件 / Shared files")
            for filename in __Share__.keys():
                print("\t", filename)
            print("\n")
            run(PORT)
        elif key in ['-v', '--version']:
            print("JinWeb Version and ", __Verison__)
        elif key in ["-h", "--help"]:
            print(f"\nJin-Web | Version:{__Verison__}")
            print("\t可用命令 / Available commands:")
            print("\t\t-f/--file=         要共享的文件路径 / File path to share")
            print("\t\t-u/--user=         共享文件的用户名，默认为：admin / The user name of the shared file. The default is admin")
            print("\t\t-k/--key=          为要共享的文件添加加密秘钥，可不添加 / Add an encryption key to the file to be shared, but do not add it")
            print("\t\t-R/--Remove=       要删除的共享文件名字(参数等于 all 时删除所有共享文件)(参数等于log时清除程序日志) /",
                  "Name of the shared file to be deleted (delete all shared files when the parameter is equal to all) ",
                  "(clear the program log when the parameter is equal to log)")
            print("\t\t-s/--see           查看已共享的所有文件 / View all shared files")
            print("\t\t-r/--run           启动共享 / Start sharing")

    if os.path.exists(f"{os.path.split(__file__)[0]}"+FILEPATH):
        AddShare(FILEPATH, USERNAME, KEY)
        print("请使用--run命令运行 / Please use the --run command to run")