# 本地代理服务器地址
proxies = {'http': 'http://127.0.0.1:11223', 'https': 'http://127.0.0.1:11223'}
# 草榴新时代的我们全站存放地址
localePath = 'G:\\测试\\全站\\缓存'
# 草榴自拍图存放地址
localePathSelf = 'G:\\测试\\自拍\\缓存'
# 草榴失败重下存放地址
localeFailPathSelf = 'G:\\测试\\失败重下'
# wall图存放地址
wallImgPath = 'G:\\测试\\img'
# 请求超时时间
timeout = 200
# 图片质量
DocumentQuality = ['垃圾质量(AVG：小于0.1M)', '劣质质量(AVG：0.1M-0.6M)', '一般质量(AVG：0.5M-1.6M)',
                   '清晰质量(AVG：1.5M-2.1M)', '标清质量(AVG：2M-5.1M)', '高清质量(AVG：5M-10.1M)',
                   '超高质量(AVG：10M-15.1M)', '顶级质量(AVG：15M-20.1M)', '巨顶质量(AVG：大于20M)',
                   '含有动图GIF']
# 图片质量
DQ = ['垃圾质量', '劣质质量', '一般质量', '清晰质量', '标清质量', '高清质量',
      '超高质量', '顶级质量', '巨顶质量', '含有动图']
# 图片后缀
imgSuffix = ['.BMP', '.DIB', '.EMF', '.GIF', '.ICB', '.ICO', '.JPG', '.JPEG', '.PBM', '.PCD', '.PCX', '.PGM', '.PNG',
             '.PPM', '.PSD', '.PSP', '.RLE', '.SGI', '.TGA', '.TIF',
             '.bmp', '.dib', '.emf', '.gif', '.icb', '.ico', '.jpg', '.jpeg', '.pbm', '.pcd', '.pcx', '.pgm', '.png',
             '.ppm', '.psd', '.psp', '.rle', '.sgi', '.tga', '.tif']
# 请求头
User_Agents = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 "
]

# 返回类型
ReturnType = ['URL', 'IMG']
# 输出颜色配置
printColour = 1
# 日志开关
log = 1

PrintColourList = ['\033[95m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[95m', '\033[94m', '\033[92m',
              '\033[93m', '\033[91m', '\033[0m', '\033[1m', '\033[4m', '\n', '\r']

jumpList = ['xsspic', 'imgxx.xyz']


# 输出颜色属性配置
class Fore:
    if printColour:
        PURPLE = '\033[95m'  # pink
        BLUE = '\033[94m'  # blue
        GREEN = '\033[92m'  # green
        YELLOW = '\033[93m'  # yellow
        RED = '\033[91m'  # red

        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

        purple = '\033[95m'  # pink
        blue = '\033[94m'  # blue
        green = '\033[92m'  # green
        yellow = '\033[93m'  # yellow
        red = '\033[91m'  # red

        header = '\033[95m'
        okblue = '\033[94m'
        okgreen = '\033[92m'
        warning = '\033[93m'
        fail = '\033[91m'
        endc = '\033[0m'
        bold = '\033[1m'
        underline = '\033[4m'
    else:
        PURPLE = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''

        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''

        purple = ''
        blue = ''
        green = ''
        yellow = ''
        red = ''

        header = ''
        okblue = ''
        okgreen = ''
        warning = ''
        fail = ''
        endc = ''
        bold = ''
        underline = ''


#企业微信配置
WECOM_CID = 'wwec2f4545241fa36d'  # 企业id
WECOM_AID = '1000004'  # 应用id
WECOM_SECRET = 'qCRWc1_PhhhYSjZr9oPENxBHPPQFYgA60Hzs-PxC_z8'  # 应用secret
WECOM_TOUID = '@all'
