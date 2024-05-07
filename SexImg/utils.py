import json

from SexImg import config
import requests
import re
# 安装时安装pillow
from PIL import Image
import random
import time

from SexImg.logger_setting import logger
from config.models import SpuModel, LogModel

timeout = config.timeout
Fore = config.Fore
User_Agents = config.User_Agents
imgSuffix = config.imgSuffix
returnType = config.ReturnType
log = config.log


logger_util = logger()


def getResponse(URL, headers, ReturnType):
    URL = str(URL).replace('[img]', '')
    # net = NetConnect()
    # if not net.check_connect(1):
    #     logger_util.error(Fore.RED + '网络或代理异常！')
    #     return False
    timeSleep = 2
    failCount = 1
    if ReturnType == 0:
        timeSleep = 3
    elif ReturnType == 1:
        timeSleep = 1
    while True:
        if failCount > 1:
            logger_util.warning(Fore.RED + f'连接[{URL}]失败，请求次数过1，请求已终止！')
            break
        try:
            headers["User-Agent"] = random.choice(User_Agents)
            response = requests.get(url=URL, headers=headers, timeout=timeout, verify=True)
            # 判断状态码不是200，自动引发HTTPError
            response.raise_for_status()
            status_code = response.status_code
            text = response.text
            content = response.content
            response.close()
            if 199 < status_code < 300:
                logger_util.info(Fore.BLUE + f'连接[{URL}]成功，状态码：' + Fore.YELLOW + f'{status_code}\n')
                return status_code, text, content
        except requests.exceptions.ConnectTimeout:
            logger_util.error(f'连接超时，{timeSleep}秒后重新开始！')
            time.sleep(timeSleep)
        except requests.exceptions.ProxyError:
            logger_util.error(f'代理异常')
            return False
        except requests.exceptions.ConnectionError:
            logger_util.error(f'网络异常')
            return False
        except requests.HTTPError:
            logger_util.error(f'HTTP错误异常')
            return False
        except requests.URLRequired:
            logger_util.error(f'URL缺失异常')
            return False
        except requests.TooManyRedirects:
            logger_util.error(f'超过最大重定向次数，产生重定向异常')
        except Exception as e:
            logger_util.warning(Fore.YELLOW + f'连接[{URL}]出现未知异常，错误信息：{e}')
            return False
        finally:
            failCount += 1
    return False


def getLocalTime():
    c_time = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())
    return str(c_time)


def getFormatData():
    return '[' + getLocalTime() + ']'


def getUrlList(regular, text):
    return re.findall(regular, text, re.S)


def getImgResolution(filename):
    try:
        img = Image.open(filename)
        imgSize = img.size
        img.close()
        if imgSize[0] >= imgSize[1]:
            return True
        else:
            return False
    except Exception as e:
        logger_util.warning(Fore.RED + '识别长宽出错：' + str(e))
        return False


def judgeUrlDownloadSuccess(imgUrl):
    result = SpuModel.query.filter_by(url=imgUrl).all()
    if result:
        logger_util.warning(Fore.RED + f"此Url：[{imgUrl}]已下载成功，无需重复下载！\n")
        return True
    else:
        return False


class NetConnect:

    def __init__(self):
        self.baiduHost = 'https://www.baidu.com/'
        self.youtubeHost = 'https://www.google.com/'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}

    def check_connect(self, value):
        if 0 == value:
            logger_util.info(Fore.YELLOW + '开始检查网络连接！')
        try:
            google_code, baidu_code = self.check_connect_return()
            if google_code + baidu_code == 2:
                return True
            else:
                return False
        except Exception as e:
            logger_util.error(Fore.red + '网络异常，错误信息：' + str(e))
        return False

    def check_connect_return(self):
        google_code = 0
        baidu_code = 0
        try:
            Google = requests.get(url=self.youtubeHost, headers=self.headers, timeout=1)
            if 199 < Google.status_code < 300:
                logger_util.info(Fore.green + '国外（Google）正常！')
                google_code = 1
            else:
                logger_util.warning(Fore.red + '国外（Google）异常！')
            Baidu = requests.get(url=self.baiduHost, headers=self.headers, timeout=1)
            if 199 < Baidu.status_code < 300:
                baidu_code = 1
                logger_util.info(Fore.green + '国内（Baidu）正常！')
            else:
                logger_util.info(Fore.red + '国内（Baidu）异常')

            return baidu_code, google_code
        except Exception as e:
            logger_util.error(Fore.red + '网络异常，错误信息：' + str(e))
        return baidu_code, google_code


def checkNet(urls,urls1, url_list_len, headers1):
    # net = NetConnect()
    # if not net.check_connect(0):
    #     return False
    logger_util.info(Fore.YELLOW + '开始检查网络连通性并测试链接：')
    start = 0
    end = 0
    try:
        start = time.time()
        response = getResponse(urls, headers1, 0)
        end = time.time()
        if response:
            logger_util.info(Fore.GREEN + f'网络连通性检查完成！\n链接列表测试完成，开始下载{url_list_len}个链接！\n')
            logger_util.info(
                Fore.GREEN + f'状态码：{response[0]}\n预计下载时间：{round(url_list_len * (end - start) / 2, 2)}s')
            return True
        else:
            start = time.time()
            response = getResponse(urls1, headers1, 0)
            end = time.time()
            if response:
                logger_util.info(Fore.GREEN + f'网络连通性检查完成！\n链接列表测试完成，开始下载{url_list_len}个链接！\n')
                logger_util.info(
                    Fore.GREEN + f'状态码：{response[0]}\n预计下载时间：{round(url_list_len * (end - start) / 2, 2)}s')
                return True
            else:
                return False

    except Exception as es:
        if 'proxy' in str(es) or 'Proxy' in str(es):
            logger_util.warning(Fore.RED + f'网络异常，请检查代理！\n检查用时{end - start}s\n故障详情：{es}')
            return False
        else:
            logger_util.error(Fore.RED + f'网络异常！错误信息：{str(es)}')
            return False


def inductive(filesize, gif):
    DocumentQuality = config.DocumentQuality
    Inductive_Catalog = ''
    if filesize < 0.11:
        Inductive_Catalog = DocumentQuality[0]
    elif 0.1 < filesize < 0.6:
        Inductive_Catalog = DocumentQuality[1]
    elif 0.5 < filesize < 1.6:
        Inductive_Catalog = DocumentQuality[2]
    elif 1.5 < filesize < 2.1:
        Inductive_Catalog = DocumentQuality[3]
    elif 2 < filesize < 5.1:
        Inductive_Catalog = DocumentQuality[4]
    elif 5 < filesize < 10.1:
        Inductive_Catalog = DocumentQuality[5]
    elif 10 < filesize < 15.1:
        Inductive_Catalog = DocumentQuality[6]
    elif 15 < filesize < 20.1:
        Inductive_Catalog = DocumentQuality[7]
    elif 20 < filesize:
        Inductive_Catalog = DocumentQuality[8]
    if gif == 1:
        Inductive_Catalog = DocumentQuality[9]
    return Inductive_Catalog


def del_log_file():
    import os

    folder_path = "./logs"  # 文件夹路径
    target_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    # 遍历文件夹中的所有文件
    count = 0
    for filename in os.listdir(folder_path):
        # 判断文件名是否包含目标字符串
        if target_str not in filename:
            # 构造文件的绝对路径
            file_path = os.path.join(folder_path, filename)
            # 删除文件
            count += 1
            os.remove(file_path)
    logger_util.error(Fore.green + f'历史日志清理完毕，共清理：{count}个文件；')


def send_to_wecom(msg):
    net = NetConnect()
    wecom_cid = config.WECOM_CID
    wecom_aid = config.WECOM_AID
    wecom_secret = config.WECOM_SECRET
    wecom_touid = config.WECOM_TOUID
    get_token_url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={wecom_cid}&corpsecret={wecom_secret}"
    response = requests.get(get_token_url).content
    access_token = json.loads(response).get('access_token')
    if access_token and len(access_token) > 0:
        send_msg_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'
        data = {
            "touser": wecom_touid,
            "agentid": wecom_aid,
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "duplicate_check_interval": 600
        }
        response = requests.post(url=send_msg_url, data=json.dumps(data)).content
        return response
    else:
        return 0
