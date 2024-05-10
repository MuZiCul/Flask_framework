import sys
import time
from datetime import datetime

from sqlalchemy.exc import NoResultFound

from SexImg import DownLoadImg
from config.decorators import throttle
from config.models import AgainpageModel, SpuModel, JpuModel, ReFiuModel, SiuModel, FiuModel, FpuModel, ConfigModel, \
    LogModel
from SexImg import config
from SexImg import utils as ut
from SexImg.logger_setting import logger
from config.exts import db

Fore = config.Fore
logger = logger()


def start():
    logger.info(Fore.GREEN + '开始检查网络：')
    baidu_code, google_code = ut.NetConnect().check_connect_return()
    if baidu_code + google_code == 2:
        logger.info(Fore.GREEN + '开始检查重下列表：')
        reDownload()
        logger.info(Fore.GREEN + '开始运行爬取程序：')

        URLlist = []
        for fid in [8, 16]:
            for page in [1, 2]:
                url = f'http://t66y.com/thread0806.php?fid={fid}&search=&page={page}'
                URLlist.append(url)

        successCount = 0
        failCount = 0
        UrlType = '洲]'
        UrlType1 = '真]'
        for URL in URLlist:
            logger.info(Fore.BLUE + f'检查URL：{URL}')
            response = ut.getResponse(URL, DownLoadImg.headers, 0)
            if not response:
                continue
            # 正则匹配图片链接和主题名
            result = ut.getUrlList(
                '<td class="tal" id=""> \r\n\r\n\t\r\n\r\n\t(.*?)\r\n\r\n\t<h3><a href="(.*?)" target="_blank" id="(.*?)">(.*?)</a></h3>',
                str(response[1]))
            for res in result:
                url = res[1]
                title = str(res[3])
                if '</' in title:
                    title = ut.getUrlList('>(.*?)</', title)[0]
                if len(str(res[0])) < 5:
                    title = str(res[0]) + title
                else:
                    title = '[自拍]' + title
                if 'read.php' in url:
                    continue
                if 'fid=8' in URL:
                    if UrlType in res[0] or UrlType1 in res[0]:
                        logger.info(Fore.BLUE + f'\n开始下载：{title}，Url：[{url}]')
                        successCount, failCount, s = download(title, url, successCount, failCount, config.localePath)
                elif 'fid=16' in URL:
                    logger.info(Fore.BLUE + f'\n开始下载：{title}，Url：[{url}]')
                    successCount, failCount, s = download(title, url, successCount, failCount, config.localePathSelf)

        logger.info(Fore.BLUE + f'\n本轮统计：\n成功{successCount}个，失败{failCount}个。')


def go_check():
    logger.info(Fore.GREEN + '开始检查网络：')
    baidu_code, google_code = ut.NetConnect().check_connect_return()
    if baidu_code + google_code == 2:
        state_msg = '正在运行'
    else:
        state_msg = '未运行'
    if baidu_code > 0:
        config_model = ConfigModel.query.filter_by(id=7).first()
        if config_model:
            config_model.value = 1
            db.session.commit()
        else:
            config_model = ConfigModel(id=7, value=1, key='state')
            db.session.add(config_model)
            db.session.commit()
        ut.send_to_wecom(
            '爬虫开始运行，网络自检情况：\n国内状态码：' + str(baidu_code) + '\n国外状态码：' + str(
                google_code) + '\n爬虫状态：' + state_msg)
    if baidu_code + google_code < 2:
        sys.exit(0)


def download(title, url, successCount, failCount, path):
    state = False
    Sresult = SpuModel.query.filter_by(url=url).all()
    Jresult = JpuModel.query.filter_by(url=url).all()
    if len(Sresult) > 0 or len(Jresult) > 0:
        logger.info(Fore.GREEN + f'该{url}已下载成功，跳过下载！')
        return successCount, failCount, state

    value = DownLoadImg.DownLoadStart(f'http://t66y.com/{url}', path)
    if value['success'] == 1:
        logger.info(Fore.GREEN + f'{url}下载成功！')
        successCount += 1
        result = SpuModel.query.filter_by(url=url).first()
        if not result or len(result) < 1:
            spu = SpuModel(
                url=url,
                title=value['title'],
                kind=value['kind'],
                quality=value['quality'],
                all_size=value['all_size'],
                avg_size=value['avg_size'],
                publish_date=value['publish_date'],
                img_size=value['img_size'],
                pcImg=value['pcImg'],
                phoneImg=value['phoneImg'],
                dir=value['dir'])
            db.session.add(spu)
            db.session.commit()
            logger.info(Fore.GREEN + f'{url}下载结果写入数据库成功！\n开始写入图片数据库！')
            nowUrl = SpuModel.query.filter_by(url=url).first()
            for i in value['SuccessImgUrlList']:
                urlTuple = i[:0] + (nowUrl.id,) + i[0:]
                siu = SiuModel(
                    page_id=urlTuple[0],
                    url=urlTuple[1],
                    title=urlTuple[2],
                    size=urlTuple[3]
                )
                db.session.add(siu)
                db.session.commit()
            logger.info(Fore.GREEN + f'开始查询失败图片数据库！')
            for furl in value['FailImgUrlList']:
                result = JpuModel.query.filter_by(url=url).all()
                if value['img_reason'] == config.jumpList and len(result) < 1:
                    JpuModelData = (
                        url, value['title'], value['img_reason'], value['publish_date'], ut.getLocalTime())
                    jpu = JpuModel(
                        url=JpuModelData[0],
                        title=JpuModelData[1],
                        reason=JpuModelData[2],
                        publish_date=JpuModelData[3]
                    )
                    db.session.add(jpu)
                    db.session.commit()
                FiuModelData = (nowUrl.id, furl, value['title'], value['img_reason'], ut.getLocalTime())
                fiu = FiuModel(
                    page_id=FiuModelData[0],
                    url=FiuModelData[1],
                    title=FiuModelData[2],
                    reason=FiuModelData[3]
                )
                db.session.add(fiu)
                db.session.commit()
        selectFailPageUrl = FpuModel.query.filter_by(url=url).all()
        for i in selectFailPageUrl:
            fpu = FpuModel.query.filter_by(id=i.id).first()
            db.session.delete(fpu)
        logger.info(Fore.BLUE + '该链接存在于失败数据库，现已下载成功，遂从失败列表删除！')
        state = True
    elif value['success'] == -1:
        logger.warning(Fore.RED + f"该链接触发跳过关键词：{value['img_reason']}，下载跳过！")
        result = JpuModel.query.filter_by(url=url).all()
        if value['img_reason'] == config.jumpList and not result:
            JpuModelData = (url, value['title'], value['img_reason'], value['publish_date'],
                            ut.getLocalTime())
            jpu = JpuModel(
                url=JpuModelData[0],
                title=JpuModelData[1],
                reason=JpuModelData[2],
                publish_date=JpuModelData[3]
            )
            db.session.add(jpu)
            db.session.commit()
        else:
            logger.warning(Fore.RED + f"该链接已存在于跳过下载列表！")
        selectFailPageUrl = FpuModel.query.filter_by(url=url).all()
        for i in selectFailPageUrl:
            fpu = FpuModel.query.filter_by(id=i.id).first()
            db.session.delete(fpu)
            db.session.commit()
    else:
        logger.info(Fore.GREEN + f'{url}下载失败！原因：{value["reason"]}')
        selectFailPageUrl = FpuModel.query.filter_by(url=url).all()
        if not selectFailPageUrl:
            fpu = FpuModel(
                url=url,
                title=title,
                publish_date=value['publish_date'],
                reason=value['reason']
            )
            db.session.add(fpu)
            db.session.commit()
        failCount += 1
    return successCount, failCount, state


def reDownload():
    successCount = 0
    failCount = 0
    relist = AgainpageModel.query.filter_by(state=0).all()
    logger.info(Fore.BLUE + f'\n重下链接统计：检测到{len(relist)}个。')
    for i in relist:
        for j in SpuModel.query.filter_by(url=i.url).all():
            spu = SpuModel.query.filter_by(id=j.id).first()
            db.session.delete(spu)
        logger.info(Fore.BLUE + f'\n开始下载：[{i.url}]')
        successCount, failCount, state = download(i.title, i.url, successCount, failCount, config.localePath)
        if state:
            againpage = AgainpageModel.query.filter_by(id=i.id).first()
            againpage.state = 1
            againpage.count = int(i.count) + 1
            db.session.commit()
    logger.info(Fore.BLUE + f'\n重下链接统计：\n共{len(relist)}个，成功{successCount}个，失败{failCount}个。')

    relist = ReFiuModel.query.filter_by(state=0).all()
    FailList = [i.url for i in relist]
    FailImgUrlList = DownLoadImg.DownLoadImgList(FailList, config.localeFailPathSelf, len(FailList)) if FailList else []
    FailList = [i for i in FailList if i not in FailImgUrlList]
    relist_ = [i for i in relist if i.url in FailList]
    for i in relist_:
        count = int(i[4]) + 1
        re_fiu = ReFiuModel.query.filter_by(id=i.id).first()
        re_fiu.state = 1
        re_fiu.count = count
        db.session.commit()


def Hard_disk_monitoring():
    # import shutil
    # gb = 1024 ** 3  # GB == gigabyte
    # total_b, used_b, free_b = shutil.disk_usage('E:')  # 查看磁盘的使用情况
    # print('总的磁盘空间: {:6.2f} GB '.format(total_b / gb))
    # print('已经使用的 : {:6.2f} GB '.format(used_b / gb))
    # print('未使用的 : {:6.2f} GB '.format(free_b / gb))
    # return total_b, used_b, free_b
    return 0, 0, 0


def update_database():
    dt = datetime.utcnow()

    # 尝试一次性查询所有需要更新的配置项，减少查询次数
    try:
        config_time = ConfigModel.query.filter_by(id=1).first()
        config_total_db = ConfigModel.query.filter_by(id=4).first()
        config_used_db = ConfigModel.query.filter_by(id=5).first()
        config_free_db = ConfigModel.query.filter_by(id=6).first()
    except NoResultFound:
        # 如果任一配置项不存在，根据需要处理异常
        print("One or more configuration entries not found.")
        return

    # 更新配置值
    if config_time:
        config_time.value = str(dt)
    else:
        config_time = ConfigModel(id=1, value=str(dt), key='last_date')
        db.session.add(config_time)
    config_total_value, config_used_value, config_free_value = Hard_disk_monitoring()
    if config_total_db:
        config_total_db.value = str(config_total_value)
        db.session.add(config_total_db)
        db.session.commit()
    else:
        config_total_db = ConfigModel(id=4, value=str(config_total_value), key='total_db')
        db.session.add(config_total_db)
        db.session.commit()

    if config_used_db:
        config_used_db.value = str(config_used_value)
        db.session.add(config_used_db)
        db.session.commit()
    else:
        config_used_db = ConfigModel(id=4, value=str(config_used_value), key='used_db')
        db.session.add(config_used_db)
        db.session.commit()

    if config_free_db:
        config_free_db.value = str(config_free_value)
        db.session.add(config_free_db)
        db.session.commit()
    else:
        config_free_db = ConfigModel(id=4, value=str(config_free_value), key='free_db')
        db.session.add(config_free_db)
        db.session.commit()


    # 提交所有更改到数据库，只需一次提交
    try:
        db.session.commit()
    except Exception as e:
        # 回滚事务以防止部分更改生效
        db.session.rollback()
        print(f"Error occurred during database update: {e}")


@throttle(interval=10)
def T66y():
    logger.info(Fore.YELLOW + '任务执行开始：')
    logger.info(Fore.RED + f'现在时间：{time.strftime("%H:%M:%S", time.localtime())}')
    go_check()
    start()
    update_database()
    logger.info(Fore.YELLOW + '开始休眠！')
    logger.info(Fore.RED + f'现在时间：{time.strftime("%H:%M:%S", time.localtime())}')


if __name__ == '__main__':

    go_check()
    start()
    update_database()
    while True:
        c_time = time.strftime("%H:%M:%S", time.localtime())
        if c_time[3:5] == '00' and c_time[6:8] == '00':
            logger.info(Fore.YELLOW + '任务执行开始：')
            a = time.time()
            logger.info(Fore.RED + f'现在时间：{c_time}')
            start()
            update_database()
            b = time.time()
            logger.info(Fore.YELLOW + '开始休眠！')
            if 3540 - int(b - a) > 0:
                time.sleep(3540 - int(b - a))
            logger.info(Fore.PURPLE + '休眠结束，程序已激活，程序将在下一个整点运行。')
