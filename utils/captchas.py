import datetime
import os
import time

from captcha.image import ImageCaptcha
import random
import string

from flask import session

from config.exts import redis_client


def getCaptchaPic(coding):
    srcPath = session.get('oldSrc')
    if srcPath is not None:
        if '.jpg' in srcPath:
            os.remove(srcPath)
    characters = '02345689xyzabc'
    width, height, n_len, n_class = 170, 80, 4, len(characters)
    generator = ImageCaptcha(width=width, height=height)
    random_str = ''.join([random.choice(characters) for j in range(4)])
    if not coding:
        coding = ''.join([random.choice(characters) for j in range(6)])
        session[coding] = 0
    random_random = ''.join([random.choice(characters) for j in range(6)])
    img = generator.generate_image(random_str)
    session['coding'] = coding
    file_name = 'static/captcha/' + random_random + '.jpg'
    session['oldSrc'] = file_name
    redis_client.set(random_str.lower(), 'captcha_img_code', 300)
    redis_client.set(random_random + '.jpg', 'captcha_img', 300)
    img.save(file_name)
    return file_name, coding


def delCaptcha():
    try:
        filePath = 'static/captcha/'
        lists = os.listdir(filePath)
        for i in lists:
            if not redis_client.keys(i):
                os.remove(filePath + '/' + i)
    except Exception as e:
        print('delCaptcha',e)
