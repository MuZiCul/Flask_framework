import copy
import os
import string
import sys
import concurrent.futures
import shutil
from concurrent.futures import ThreadPoolExecutor

from flask import current_app

from SexImg import config as con
from SexImg.utils import *
from SexImg.logger_setting import logger
from config.models import FpuModel, SpuModel, JpuModel, SiuModel, FiuModel
from config.exts import db

Fore = con.Fore
localePath = ''

common_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Accept-Language': 'zh-CN,en-US;q=0.7,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

headers = {
    **common_headers,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    "host": "t66y.com",
    "Content-Type": "application/json;charset=utf-8",
    'Upgrade-Insecure-Requests': '1'
}

headers_User_Agent = {
    **common_headers,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
}

headers1 = {
    **common_headers,
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'If-None-Match': "62519b25-7c336b"
}

headers2 = {
    **common_headers,
    'Host': 'louimg.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1'
}



# 失败列表
FailImgUrlList = []
# 失败列表
SuccessImgUrlList = []
# 根目录
timeout = 15
proxies = con.proxies
value = {
    'url': '',
    'title': '',
    'quality': 0,
    'all_size': '',
    'avg_size': '',
    'img_size': '',
    'pcImg': 0,
    'phoneImg': 0,
    'dir': '',
    'publish_date': '',
    'success': 1,
    'kind': 0,
    'reason': '',
    'img_reason': '',
    'SuccessImgUrlList': [],
    'FailImgUrlList': []
}

logger_ = logger()


def DownLoadImg(url, path, SN, app_instance):
    # 修改请求头，防止被服务器屏蔽
    global headers1
    global FailImgUrlList
    # 获取图片后缀
    others = url.rsplit('.', 1)
    img_suffix = others[1]
    # 防止出现标点符号导致文件不能创建
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    out = regex.sub('', others[0].rsplit('/', 1)[1])
    # 防止文件名过长
    if len(out) > 6:
        out = out[-3:]
    # 拼接图片真实路径
    if img_suffix not in con.imgSuffix:
        img_suffix = 'png'
    out = ''.join(random.sample(string.digits, 10))
    img_Name = SN + '.' + out
    # 拼接图片真实存放地址
    rulePath = path + '/' + img_Name + '.' + img_suffix
    if 'ttps' in url and 'https' not in url:
        url = 'h' + url
    # 在每个线程开始时手动推入应用上下文
    with app_instance.app_context():
        try:
            response = getResponse(url, headers1, 0)
            with open(rulePath, 'wb') as img_file:
                img_file.write(response[2])  # 写入二进制内容
            logger_.info(
                Fore.BLUE + f"No.{str(SN).zfill(3)}:{url} ,Download Successful ," + Fore.YELLOW + f"Status Code:{response[0]}\n")
            dic = (url, value['title'], os.path.getsize(rulePath), getLocalTime())
            SuccessImgUrlList.append(dic)
            return True
        except Exception as e:
            logger_.error(Fore.RED + f'图片写入失败，故障原因：{str(e)}\n')
            value['img_reason'] = str(e)
            FailImgUrlList.append(url)
            return False


def getPostTime(html_string):
    import re
    from datetime import datetime

    # 使用正则表达式匹配并提取所需内容
    match = re.search(r'>(\d{2}-\d{2} \d{2}:\d{2})<', html_string)

    # 如果找到匹配，提取时间；否则，使用当前日期和时间
    if match:
        extracted_time = match.group(1)
    else:
        current_time = datetime.now().strftime('%m-%d %H:%M')  # 格式化当前日期和时间为MM-DD HH:MM格式
        extracted_time = current_time

    return extracted_time


def createFolder(urls,urls1, url_list_len, tittle, postDate):
    tittle = tittle.replace('］', ']').replace('［', '[')
    sets = ['/', '-', ',', ' ', '.', '，', '&', '^', '$', '~', '·', '`', '￥', '……', '@', '！', '!', '*', '+', '。', '\\',
            ':', '*', '?', '"', '<', '>', '|', '\t', '\n', '\r', '&nbsp;', 'nbsp;']
    tittle = tittle.translate(str.maketrans('', '', ''.join(sets)))
    pnum = re.findall('\[(.*?)]', tittle, re.S)
    if len(pnum) > 1:
        pnum.reverse()
    title = tittle
    for i in pnum:
        title = title.replace(i, '')
    title = title.replace(']', '').replace('[', '')
    if pnum:
        tittle = tittle.replace(f'[{pnum[0]}]', '')
    if '[' not in tittle and ']' not in tittle:
        tittle = '[自拍]' + tittle
    if pnum:
        if 'P' in pnum[0]:
            tittle = f'{tittle}[{pnum[0]}]'
    if '洲]' in tittle:
        value['kind'] = 0
    elif '真]' in tittle:
        value['kind'] = 1
    elif '拍]' in tittle:
        value['kind'] = 2

    paths = localePath + '/' + tittle
    value['title'] = title
    value['publish_date'] = getPostTime(postDate)
    logger_.info(Fore.BLUE + f'目标文件夹位置：{paths}，开始测试图片链接：')
    if not checkNet(urls,urls1, url_list_len, headers1):
        value['reason'] = '网络异常'
        return False
    else:
        logger_.info(Fore.BLUE + f'图片链接成功！受测链接：{urls}')
    # 获取目录下文件夹
    dir_list = []
    for root, dirs, files in os.walk(localePath):
        dir_list = dirs
        break
    logger_.info(Fore.GREEN + '本篇发布时间：' + Fore.YELLOW + value['publish_date'])
    for dir_one in dir_list:
        if tittle in dir_one:
            logger_.warning(Fore.YELLOW + f'相似文件夹{dir_one}已存在，图片将存到本目录下！')
            paths = localePath + '/' + dir_one
            break
    else:
        if not os.path.exists(paths):
            os.makedirs(paths)
            logger_.info(Fore.GREEN + f'创建文件夹-->{paths}<--成功！')
        else:
            logger_.warning(Fore.YELLOW + f'文件夹已存在，图片将存到本目录下！')

    return paths


def analWebData(html):
    # 正则匹配图片链接和主题名和发布时间
    urlLists = getUrlList('ess-data=\'(.*?)\'', html)
    logger_.info(Fore.BLUE + f'图片列表获取成功，共获取到：{len(urlLists)}张图片！')
    title = getUrlList('class="f16">(.*?)</h4>', html)[0]
    for i in urlLists:
        logger_.info(Fore.BLUE + f'{title}：{i}')
    postDate = getUrlList('TOP</a></span>\r\n(.*?)\r\n\r\n<span class="s3">樓主', html)
    if len(urlLists) < 1:
        logger_.error(Fore.RED + '图片列表获取失败，请检查Url！')
        value['reason'] = '图片列表获取失败，请检查Url！'
        return False, False
    else:
        if con.jumpList[0] in urlLists[0]:
            value['img_reason'] = con.jumpList[0]
            value['success'] = -1
            value['SuccessImgUrlList'] = []
            value['FailImgUrlList'] = []
            logger_.warning(Fore.YELLOW + f'图片无法下载，原因：{con.jumpList[0]}')
            return -1, -1
        global headers1
        if 's3.xoimg.com' in urlLists[0]:
            headers1 = headers1
        elif 'louimg.com' in urlLists[0]:
            headers1 = headers2
        else:
            headers1 = headers_User_Agent
        # 判断网络连接并创建目录文件夹
        logger_.info(Fore.BLUE + '开始分析图片链接真实性并创建下载目录：')
        realPath = createFolder(urlLists[0],urlLists[1], len(urlLists), title, postDate[0])
        if realPath:
            return urlLists, realPath
        else:
            return False, False


def DownLoadImgList(urlList, path, max_workers):
    logger_.info(Fore.PURPLE + f'开始下载{len(urlList)}个文件：')
    No = len(urlList)
    app_instance = current_app._get_current_object()  # 获取当前应用实例，确保可以跨线程使用
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for url in urlList:
            executor.submit(DownLoadImg, url, path, str(len(urlList) - No + 1), app_instance)
            No -= 1
    logger_.info(Fore.PURPLE + '\n下载结束，任务信息：')
    logger_.info(Fore.PURPLE + '--获取链接：' + Fore.YELLOW + f'{len(urlList)}个')
    logger_.info(Fore.PURPLE + '--下载成功：' + Fore.YELLOW + f'{len(urlList) - len(FailImgUrlList)}个')
    logger_.info(Fore.PURPLE + '--下载失败：' + Fore.YELLOW + f'{len(FailImgUrlList)}个')
    logger_.info(Fore.PURPLE + '--缓存位置：' + Fore.YELLOW + f'{path}')
    return FailImgUrlList


def DownLoadStart(URL, downloadPath):
    value['success'] = 1
    value['SuccessImgUrlList'] = []
    value['FailImgUrlList'] = []
    global localePath, FailImgUrlList, headers
    if not downloadPath == '' and not os.path.exists(downloadPath):
        os.makedirs(downloadPath)
    if not downloadPath == '':
        localePath = downloadPath
    # 修改请求头，防止被服务器屏蔽
    # 获取下载列表
    response = getResponse(URL, headers, 0)
    if not response:
        logger_.error(Fore.RED + '网络异常，该链接已加入失败列表！')
        value['success'] = 0
        value['reason'] = '网络异常'
        return value
    else:
        logger_.info(Fore.BLUE + '下载列表获取成功，开始分析下载列表！')
    # 分析下载列表
    urlList, path = analWebData(response[1])
    if urlList == -1:
        return value
    count = 1
    while not urlList:
        if count > 1:
            logger_.warning(Fore.RED + '重新获取资源列表失败，该URL将纳入错误列表！')
            value['reason'] = '重新获取资源列表失败'
            value['success'] = 0
            return value
        logger_.info(Fore.YELLOW + '重新请求获取列表！')
        urlList, path = analWebData(response[1])
        count += 1
    if urlList:
        DownLoadImgList(urlList, path, 10)
        DownloadFailList(path)
        try:
            if SuccessImgUrlList:
                value['SuccessImgUrlList'] = copy.deepcopy(SuccessImgUrlList)
                SuccessImgUrlList.clear()
        except Exception as e:
            logger_.error(str(e))
        if FailImgUrlList:
            value['FailImgUrlList'] = copy.deepcopy(FailImgUrlList)
            FailImgUrlList.clear()
        if not Judge_picture_quality(path):
            return value
        return value
    else:
        return value


def DownloadFailList(path):
    while len(FailImgUrlList) > 0:
        logger_.info(Fore.BLUE + f'\n下载失败列表：')
        for failUrl in FailImgUrlList:
            logger_.info(Fore.RED + failUrl)
        failCount = 0
        while len(FailImgUrlList) > 0:
            if failCount > 4:
                return
            FailList = copy.deepcopy(FailImgUrlList)
            FailImgUrlList.clear()
            logger_.info(Fore.BLUE + f'\n开始重新下载失败列表{len(FailList)}个文件：')
            DownLoadImgList(FailList, path, len(FailList))
            failCount += 1


def Start():
    while True:
        URL = input(Fore.GREEN + '请输入贴吧链接（输入”0“停止运行）：')
        if URL == '0':
            logger_.info(Fore.RED + '\n程序退出运行！')
            sys.exit()
        tic = time.time()
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(regex, URL) is not None:
            if 't66y' in URL:
                if 'localhost' in URL or 't66y' not in URL:
                    logger_.info(Fore.RED + "仅支持”草榴社区“中帖子Url，请检查Url后重新输入。\n")
                    continue
                if not 199 < getResponse(URL, headers, 0)[0] < 300:
                    logger_.warning(Fore.RED + "请求获取失败，请检查Url后重新输入。\n")
                    continue
                if judgeUrlDownloadSuccess(URL[17:]):
                    continue
                else:
                    result = FpuModel.query.filter_by(url=URL[17:]).all()
                    if len(result) > 0:
                        tagger = input(Fore.YELLOW + '该文件存在下载失败记录，是否重新下载？0/1')
                        if tagger == '1':
                            DownLoadStart(URL, '')
                            if value['success'] == 1:
                                value['url'] = URL[17:]
                                SpuModelData = (
                                    value['url'], value['title'], value['kind'], value['quality'], value['all_size'],
                                    value['avg_size'], value['publish_date'],
                                    value['img_size'], value['pcImg'], value['phoneImg'], value['dir'])
                                spu = SpuModel(
                                    url=SpuModelData[0],
                                    title=SpuModelData[1],
                                    kind=SpuModelData[2],
                                    quality=SpuModelData[3],
                                    all_size=SpuModelData[4],
                                    avg_size=SpuModelData[5],
                                    publish_date=SpuModelData[6],
                                    img_size=SpuModelData[7],
                                    pcImg=SpuModelData[8],
                                    phoneImg=SpuModelData[9],
                                    dir=SpuModelData[10]
                                )
                                db.session.add(spu)
                                db.session.commit()
                                if len(result) == 1:
                                    fpu = FpuModel.query.filter_by(id=result[0][0]).first()
                                    db.session.delete(fpu)
                                    db.session.commit()
                                else:
                                    for res in result:
                                        fpu = FpuModel.query.filter_by(id=res[0]).first()
                                        db.session.delete(fpu)
                                        db.session.commit()
                            elif value['success'] == 0:
                                logger_.error(Fore.RED + '下载失败，纳入错误下载列表，退出下载！\n')
                                fpu = FpuModel(
                                    url=value['url'],
                                    title=value['title'],
                                    publish_date=value['publish_date'],
                                    reason=value['reason']
                                )
                                db.session.add(fpu)
                                db.session.commit()
                                continue
                            elif value['success'] == -1:
                                logger_.warning(Fore.RED + f"该链接触发跳过关键词：{value['img_reason']}，下载跳过！")
                                result = JpuModel.query.filter_by(url=URL).all()
                                if value['img_reason'] in con.jumpList and not result:
                                    JpuModelData = (URL, value['title'], value['img_reason'], value['publish_date'],
                                            getLocalTime())
                                    jpu = JpuModel(
                                        url=JpuModelData[0],
                                        title=JpuModelData[1],
                                        reason=JpuModelData[2],
                                        publish_date=JpuModelData[3]
                                    )
                                    db.session.add(jpu)
                                    db.session.commit()
                                else:
                                    logger_.warning(Fore.RED + f"该链接已存在于跳过下载列表！")
                                failResult = FpuModel.query.filter_by(url=URL[17:]).all()
                                if failResult:
                                    logger_.warning(Fore.RED + f"该链接存在于下载失败列表，将从失败列表删除该链接！")
                                    for i in failResult:
                                        fpu = FpuModel.query.filter_by(id=i.id).first()
                                        db.session.delete(fpu)
                                        db.session.commit()
                        else:
                            continue
                    else:
                        DownLoadStart(URL, '')
                        if value['success'] == -1:
                            logger_.warning(Fore.RED + f"该链接触发跳过关键词：{value['img_reason']}，下载跳过！")

                            result = JpuModel.query.filter_by(url=URL).all()
                            if value['img_reason'] in con.jumpList and not result:
                                JpuModelData = (URL, value['title'], value['img_reason'], value['publish_date'],
                                        getLocalTime())
                                jpu = JpuModel(
                                    url=JpuModelData[0],
                                    title=JpuModelData[1],
                                    reason=JpuModelData[2],
                                    publish_date=JpuModelData[3]
                                )
                                db.session.add(jpu)
                                db.session.commit()
                            else:
                                logger_.warning(Fore.RED + f"该链接已存在于跳过下载列表！")
                            failResult = FpuModel.query.filter_by(url=URL[17:]).all()
                            if failResult:
                                logger_.warning(Fore.RED + f"该链接存在于下载失败列表，将从失败列表删除该链接！")
                                for i in failResult:
                                    fpu = FpuModel.query.filter_by(id=i.id).first()
                                    db.session.delete(fpu)
                                    db.session.commit()
                        else:
                            if value['success'] == 1:
                                SpuModelData = (URL[17:], value['title'], value['kind'], value['quality'],
                                        value['all_size'],
                                        value['avg_size'], value['publish_date'],
                                        value['img_size'], value['pcImg'], value['phoneImg'],
                                        value['dir'])
                                spu = SpuModel(
                                    url=SpuModelData[0],
                                    title=SpuModelData[1],
                                    kind=SpuModelData[2],
                                    quality=SpuModelData[3],
                                    all_size=SpuModelData[4],
                                    avg_size=SpuModelData[5],
                                    publish_date=SpuModelData[6],
                                    img_size=SpuModelData[7],
                                    pcImg=SpuModelData[8],
                                    phoneImg=SpuModelData[9],
                                    dir=SpuModelData[10]
                                )
                                db.session.add(spu)
                                db.session.commit()

                            else:
                                fpu = FpuModel(
                                    url=URL[17:],
                                    title=value['title'],
                                    publish_date=value['publish_date'],
                                    reason=value['reason']
                                )
                                db.session.add(fpu)
                                db.session.commit()
                            try:
                                if SuccessImgUrlList:
                                    nowUrl = SpuModel.query.filter_by(url=value['url']).all()
                                    for i in SuccessImgUrlList:
                                        urlTuple = i[:0] + (nowUrl[0],) + i[0:]
                                        siu = SiuModel(
                                            page_id=urlTuple[0],
                                            url=urlTuple[1],
                                            title=urlTuple[2],
                                            size=urlTuple[3]
                                        )
                                        db.session.add(siu)
                                        db.session.commit()
                                    SuccessImgUrlList.clear()
                            except Exception as e:
                                logger_.error(str(e))
                            if FailImgUrlList:
                                nowUrl = SpuModel.query.filter_by(url=value['url']).all()
                                for url in FailImgUrlList:
                                    FiuModelData = (nowUrl[0], url, value['title'], value['img_reason'], getLocalTime())
                                    fiu = FiuModel(
                                        page_id=FiuModelData[0],
                                        url=FiuModelData[1],
                                        title=FiuModelData[2],
                                        reason=FiuModelData[3]
                                    )
                                    db.session.add(fiu)
                                    db.session.commit()
                                FailImgUrlList.clear()
            elif 'yalayi' in URL:
                pass
            else:
                logger_.warning(Fore.RED + "Url无法识别，请重新输入。\n")
                continue
            toc = time.time()
            logger_.info(Fore.PURPLE + f'\n本次用时：{round(toc - tic, 2)}秒\n')
        else:
            logger_.error(Fore.RED + "Url有误，请检查Url后重新输入。\n")
            continue


def Judge_picture_quality(start_path):
    total_size = 0
    total = 0
    quality = ''
    gif = 0
    DocumentQuality = con.DQ
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            if '.gif' in f or '.GIF' in f:
                gif = 1
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total += 1
                total_size += os.path.getsize(fp)
    if total == 0:
        shutil.rmtree(start_path)
        return False
    totalMb = round(total_size / 1048576, 2)
    filesize = round(totalMb / total, 2)
    qualityCode = -1
    if gif == 1:
        qualityCode = 9
        quality = DocumentQuality[9]
    elif filesize < 0.11:
        qualityCode = 0
        quality = DocumentQuality[0]
    elif 0.1 < filesize < 0.6:
        qualityCode = 1
        quality = DocumentQuality[1]
    elif 0.5 < filesize < 1.6:
        qualityCode = 2
        quality = DocumentQuality[2]
    elif 1.5 < filesize < 2.1:
        qualityCode = 3
        quality = DocumentQuality[3]
    elif 2 < filesize < 5.1:
        qualityCode = 4
        quality = DocumentQuality[4]
    elif 5 < filesize < 10.1:
        qualityCode = 5
        quality = DocumentQuality[5]
    elif 10 < filesize < 15.1:
        qualityCode = 6
        quality = DocumentQuality[6]
    elif 15 < filesize < 20.1:
        qualityCode = 7
        quality = DocumentQuality[7]
    elif 20 < filesize:
        qualityCode = 8
        quality = DocumentQuality[8]
    start_path_rsplit = start_path.rsplit('/', 1)
    dir_path = start_path_rsplit[1]
    # 获取年月日时分秒
    datatime = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())))
    # 对文件尺寸小数补零
    filesizeLZ = f"{filesize:.2f}".rstrip('0').rstrip('.') if filesize.is_integer() else f"{filesize:.2f}"
    # 拼接序列号，质量代码+年月日时分秒+文件尺寸
    new_path = '['+str(qualityCode) + datatime + str(filesizeLZ)+']'
    # 删除序列号中的小数点
    new_path = new_path.replace(".", "")

    # pattern = r'\[(.*?)\](.*?)\[\d+P\]'
    # match = re.search(pattern, dir_path)
    # if match:
    #     # group(2) 用于获取第2个括号内匹配的内容，即我们想要提取的部分
    #     dir_path = match.group(2).strip()  # 使用strip()去除可能的前后空白
    #
    # if len(dir_path) > 20:
    #     dir_path = dir_path[:20]

    if '质量' in start_path and 'AVG' in start_path:
        file_name = ''
        for dir_ in range(30, len(dir_path)):
            file_name += dir_path[dir_]
        new_path += file_name
    else:
        new_path += dir_path

    new_path = start_path_rsplit[0] + '/' + new_path
    os.rename(start_path, new_path)
    if not Inductive(new_path, filesize, gif):
        return False
    logger_.info(Fore.PURPLE + '\n图片综合质量评价：')
    logger_.info(Fore.PURPLE + '--图片总数：' + Fore.YELLOW + f'{total}个')
    value['img_size'] = str(total)
    logger_.info(Fore.PURPLE + '--整体质量：' + Fore.YELLOW + f'{totalMb}MB')
    value['all_size'] = str(totalMb)
    logger_.info(Fore.PURPLE + '--平均质量：' + Fore.YELLOW + f'{filesize}MB')
    value['avg_size'] = str(filesize)
    logger_.info(Fore.PURPLE + '--综合评价：' + Fore.YELLOW + f'{quality}')
    value['quality'] = qualityCode
    return True


# 按图片质量归类
def Inductive(PrFilePath, filesize, gif):
    fileList = []
    oldPathRsplit = PrFilePath.rsplit('/', 2)
    Inductive_Catalog = inductive(filesize, gif)
    targetPath = oldPathRsplit[0] + '/' + Inductive_Catalog
    targetDir = targetPath + '/' + PrFilePath.rsplit('/', 1)[1]
    count = 1
    while os.path.exists(targetDir):
        targetDir = targetPath + '/' + PrFilePath.rsplit('/', 1)[1] + str(count)
        count += 1
        if not os.path.exists(targetDir):
            os.rename(targetPath + '/' + PrFilePath.rsplit('/', 1)[1], targetDir)
            logger_.warning(Fore.RED + '归档已存在，旧档更名为：' + Fore.YELLOW + targetDir)
            break
    targetDir = targetPath + '/' + PrFilePath.rsplit('/', 1)[1]
    if os.path.exists(targetPath):
        shutil.move(PrFilePath, targetPath)
    else:
        os.makedirs(targetPath)
        shutil.move(PrFilePath, targetPath)

    if not os.path.exists(targetDir + '/手机壁纸'):
        os.makedirs(targetDir + '/手机壁纸')
    if not os.path.exists(targetDir + '/电脑壁纸'):
        os.makedirs(targetDir + '/电脑壁纸')
    for root, dirs, files in os.walk(targetDir):
        fileList = files
        break
    PCCount = 0
    PhoneCount = 0
    for file in fileList:
        if getImgResolution(targetDir + '/' + file):
            PCCount += 1
            shutil.move(targetDir + '/' + file, targetDir + '/电脑壁纸')
        else:
            PhoneCount += 1
            shutil.move(targetDir + '/' + file, targetDir + '/手机壁纸')
    icloudPath = convert_path(targetDir)
    copy_folder(targetDir, icloudPath)
    logger_.info(Fore.PURPLE + f'\nicloud Done ,{icloudPath}')
    logger_.info(Fore.PURPLE + '\n归档结束，任务信息：')
    logger_.info(Fore.PURPLE + '--电脑壁纸：' + Fore.YELLOW + f'{PCCount}个')
    value['pcImg'] = PCCount
    logger_.info(Fore.PURPLE + '--手机壁纸：' + Fore.YELLOW + f'{PhoneCount}个')
    value['phoneImg'] = PhoneCount
    logger_.info(Fore.PURPLE + '--存放位置：' + Fore.YELLOW + f'{targetDir}')
    value['dir'] = targetDir
    return True


def convert_path(path):
    # 定义替换规则
    old_prefix = '/Volumes/disk1_18793270297/T66Y/'
    new_prefix = '/Users/mac/Library/Mobile Documents/com~apple~CloudDocs/Mac/mac_t66y/'

    # 替换路径前缀
    new_path = path.replace(old_prefix, new_prefix)

    return new_path

# def Crawlall(SN, UrlType):
#     # 修改请求头，防止被服务器屏蔽
#     global headers
#     # 爬取网页内容
#     URL = f'http://t66y.com/thread0806.php?fid=16&search=&page={SN}'
#     response = getResponse(URL, headers, 0)
#     if not response:
#         return False
#     # 正则匹配图片链接和主题名
#     result = getUrlList('<td class="tal" id=""> \r\n\r\n\t\r\n\r\n\t(.*?)\r\n\r\n\t<h3><a href="(.*?)" target="_blank" id="">(.*?)</a></h3>', str(response[1]))
#     count = 1
#     for res in result:
#         logger_.info(f'下载第{SN}页，第{count}条')
#         count += 1
#         if UrlType in res[0]:
#             if not selectSuccessPageUrl(res[1]) and not selectFailPageUrl(res[1]):
#                 if not DownLoadStart(f'http://t66y.com/{res[1]}', ''):
#                     insertFailPageUrl(res[1])
#                 else:
#                     insertSuccessPageUrl(res[1])


if __name__ == '__main__':
    net = NetConnect()
    if net.check_connect(0):
        while True:
            # tage = input(Fore.GREEN + '是否进行批量下载（0/1）：')
            # dataBase = DB.Operation_mysql(True)
            # if tage == '1':
            #     localePath = 'E:/自拍/缓存'
            #     if not os.path.exists(localePath):
            #         os.mkdir(localePath)
            #     startPage = input(Fore.YELLOW + '开始页码：')
            #     endPage = input(Fore.YELLOW + '结束页码：')
            #     for i in range(int(startPage), int(endPage)):
            #         logger_.info(Fore.BLUE + f'开始下载第{i}页：')
            #         Crawlall(i, '')
            #         logger_.info(Fore.BLUE + f'第{i}页下载完成')
            # else:
            #     localePath = 'E:/草料/临时/缓存'
            #     if not os.path.exists(localePath):
            #         os.mkdir(localePath)
            #     Start()
            # close_conn()
            localePath = 'E:/OneDrive - muzi/草料/临时/缓存'
            if not os.path.exists(localePath):
                os.makedirs(localePath)
            Start()
