'''
Function:
    喜马拉雅模拟登录
Author:
    Charles
微信公众号:
    Charles的皮卡丘
更新日期:
    2020-11-26
'''
import os
import time
import base64
import warnings
import requests
import cv2 as cv
"""
pip3 install opencv-python
"""
import random
import json
import execjs
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import hashlib
from ..utils.misc import *
warnings.filterwarnings('ignore')


'''PC端登录喜马拉雅'''
class ximalayaPC():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in pc mode'
        self.session = requests.Session()
        self.web_pl_url = "https://mermaid.ximalaya.com/collector/web-pl/v1"
        self.login_headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
            'Content-Type': 'application/json',
            'Host': 'passport.ximalaya.com',
            'Origin': 'https://www.ximalaya.com',
            'Referer': 'https://www.ximalaya.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36'
        }
        self.session.headers.update(self.login_headers)
        self.sessionId = get_sessionId()
        self.nonce_url = 'https://passport.ximalaya.com/web/nonce/'
        self.login_url = 'https://passport.ximalaya.com/web/login/pwd/v1'
    
    def get_nonce(self,token):
        # 此处cookies可加可不加
        cookies={'fds_otp':token}
        # print(cookies)
        response = self.session.get(self.nonce_url+Captcha.get_time(),verify=False)
        return response.json()['nonce']
    
    def encrypt_password(self,password):
        """ rsa加密密码,并用base64编码 """
        modules = "009585A4773ABEECB949701D49762F2DFAB9599BA19DFE1E1A2FA200E32E0444F426DA528912D9EA8669515F6F1014C454E1343B97ABF7C10FE49D520A6999C66B230E0730C3F802D136A892501FF2B13D699B5C7ECBBFEF428AC36D3D83A5BD627F18746A7FDC774C12A38DE2760A3B95C653C10D7EB7F84722976251F649556B"
        rsa_public_key = RSA.construct((int(modules,16),int('10001',16)))
        cipher_rsa = PKCS1_v1_5.new(rsa_public_key)
        temp = cipher_rsa.encrypt(password.encode())
        return base64.b64encode(temp)
    
    def get_signature(self,account,nonce,password):
        """ sha1进行签名 """
        # 签名前大写upper()
        raw = f"account={account}&nonce={nonce}&password={password}&WEB-V1-PRODUCT-E7768904917C4154A925FBE1A3848BC3E84E2C7770744E56AFBC9600C267891F"
        return hashlib.sha1(raw.upper().encode()).hexdigest()
    
    def get_login_data(self,account,password,token):
        nonce = self.get_nonce(token)
        encrypted_password = self.encrypt_password(password)
        encrypted_password = str(encrypted_password,'utf-8')
        post_data = {
            'account': account,
            'password': encrypted_password,
            'nonce': nonce,
            'signature': self.get_signature(account,nonce,encrypted_password),
            'rememberMe': 'false',
        }
        return post_data
    
    def __login(self,account,password,token):
        post_data = self.get_login_data(account,password,token)
        # print(json.dumps(post_data))
        cookies={'fds_otp':token}
        # 最核心post请求cookie必须加
        response = self.session.post(self.login_url,data=json.dumps(post_data),cookies=cookies,verify=False)
        if response.status_code==200:
            return response.json()
    
    def login(self,username,password,crack_captcha_func):
        # 拿到通过验证码滑块的token
        token = crack_captcha_func(self.sessionId)
        resp_json = self.__login(username,password,token)
        
        if resp_json['ret'] == 0:
            """ 登录成功 """
            print(resp_json['msg'])
        elif resp_json['ret'] == 20007:
            """ 账号名或密码错误 """
            print(resp_json['msg'])
        else:
            print(resp_json)
            raise RuntimeError(resp_json.get('msg', 'something error'))
        infos_return = {'username': username}
        infos_return.update(resp_json)
        return infos_return, self.session


def get_sessionId():
    """ 获取sessionId """
    jstext = """ 
    function get_sessionId(){
    var t, o;
    var sessionId;
    o = +new Date,
    sessionId = "" + (t || "xm_") + o.toString(36) + Math.random().toString(36).substr(2, 6)
    return sessionId
    }
    """
    ctx = execjs.compile(jstext)
    sessionId = ctx.call('get_sessionId')
    return sessionId


def get_pos(image):
    """ 获取距离 """
    """ 
    原识别腾讯滑块验证 https://github.com/wkunzhi/Python3-Spider/blob/master/%E6%BB%91%E5%8A%A8%E9%AA%8C%E8%AF%81%E7%A0%81/%E3%80%90%E8%85%BE%E8%AE%AF%E3%80%91%E6%BB%91%E5%9D%97%E9%AA%8C%E8%AF%81/discriminate.py
    改写后识别喜马拉雅滑块验证的准确率在60-70%
    """
    blurred = cv.GaussianBlur(image, (5, 5), 0)
    canny = cv.Canny(blurred, 200, 400)
    contours, hierarchy = cv.findContours(canny, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    target_contour = None
    target_contourArea = 0
    for i, contour in enumerate(contours):
        m = cv.moments(contour)
        if m['m00'] == 0:
            cx = cy = 0
        else:
            cx, cy = m['m10'] / m['m00'], m['m01'] / m['m00']
        testcontourArea = cv.contourArea(contour)
        testarcLength = cv.arcLength(contour, True)
        # print(testcontourArea,testarcLength)
        # 初步筛选
        if 15 <= cv.contourArea(contour) and 250 < cv.arcLength(contour, True)<1200:
            # if cx < 150:
            #     continue
            testcontourArea = cv.contourArea(contour)
            testarcLength = cv.arcLength(contour, True)
            if testcontourArea > target_contourArea and cx >150:
                target_contour = contour
                target_contourArea = testcontourArea
    if not target_contourArea ==0:
        x, y, w, h = cv.boundingRect(target_contour)  # 外接矩形
        # 显示识别到的缺口
        # cv.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv.imshow('image', image)
        return x
    return 0

class Captcha:
    def __init__(self, sessionId):
        self.sessionId = sessionId
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }
        self.captcha_url = 'https://mobile.ximalaya.com/captcha-web/check/slide/get'
        self.slide_url = "https://mobile.ximalaya.com/captcha-web/valid/slider"

        self.captcha_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Origin': 'https://www.ximalaya.com',
            'Referer': 'https://www.ximalaya.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en;q=0.7',
        }
        self.session = requests.Session()
        self.session.headers.update(self.captcha_headers)

    @staticmethod
    def get_time():
        time_url = 'https://www.ximalaya.com/revision/time'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
        }
        response = requests.get(time_url, headers=headers)
        if response.status_code == 200:
            return response.text

    def get_captcha_url(self, sessionId):
        """ 获取captcha_url """
        params = {
            'bpId': '139',
            'sessionId': sessionId,
        }
        # response = requests.get(self.captcha_url,params=params,headers=self.headers)
        response = self.session.get(
            self.captcha_url, params=params, headers=self.captcha_headers)
        if response.status_code == 200:
            return response.json()

    def downlord_captcha(self, bg_url, bg_name):
        response = requests.get(bg_url, headers=self.headers)
        # saveImage(response.content,os.path.join(os.getcwd(),bg_name))
        with open(bg_name, 'wb') as f:
            f.write(response.content)
            f.close()
        print('Saved captcha ', bg_name)

    def get_distance(self, bg_name):
        img0 = cv.imread(bg_name)
        result = get_pos(img0)
        # print(result)
        cv.waitKey(0)
        cv.destroyAllWindows()
        return result

    def calculate_captcha_text(self, distance):
        """ 计算缺口偏移后的值 """
        d = float(distance)
        captcha_text_x = (((0.8*d)+10)*0.9247-9.6)/0.8+44
        return captcha_text_x

    def post_slide(self, captcha_text_X, sessionId):
        text_X = str(int(captcha_text_X))
        post_data = {
            'bpId': '139',
            'sessionId': sessionId,
            'type': "slider",
            'captchaText': text_X+","+str(random.randint(-10, 10)),
            'startX': str(500+random.randint(-10, 10)),
            'startY': str(180+random.randint(-10, 10)),
            'startTime': Captcha.get_time()
        }
        response = self.session.post(self.slide_url, data=json.dumps(
            post_data), headers=self.captcha_headers)
        if response.status_code == 200:
            return response.json()

    def check_captcha(self):
        # sessionId = 'xm_k6oksl4zdvza2u'
        sessionId = self.sessionId
        res_json = self.get_captcha_url(sessionId)
        self.downlord_captcha(res_json['data']['bgUrl'], 'captcha_img.jpg')
        distance = self.get_distance('captcha_img.jpg')
        captcha_text_X = self.calculate_captcha_text(distance)
        check_captcha_res = self.post_slide(captcha_text_X, sessionId)
        if check_captcha_res['result'] == 'true':
            print('recognized the captcha successfully')
            # return self.session
            removeImage('captcha_img.jpg')
            return check_captcha_res['token']
        else:
            removeImage('captcha_img.jpg')
            print('fail to recognized the captcha')

    def captcha_verify(self):
        """ 获得滑动验证通过后的token,最后的登录post需要添加到cookie中 """
        token = None
        while (token == None):
            token = self.check_captcha()
            time.sleep(1)
        
        return token


def ximalayaCaptchafun(sessionId):
    return Captcha(sessionId).check_captcha()


'''移动端登录喜马拉雅'''
class ximalayaMobile():
    is_callable = False
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in mobile mode'


'''扫码登录喜马拉雅'''
class ximalayaScanqr():
    is_callable = True
    def __init__(self, **kwargs):
        for key, value in kwargs.items(): setattr(self, key, value)
        self.info = 'login in ximalaya in scanqr mode'
        self.cur_path = os.getcwd()
        self.session = requests.Session()
        self.__initialize()
    '''登录函数'''
    def login(self, username='', password='', crack_captcha_func=None, **kwargs):
        # 设置代理
        self.session.proxies.update(kwargs.get('proxies', {}))
        # 获取二维码
        response = self.session.get(self.qrcode_url, verify=False)
        response_json = response.json()
        saveImage(base64.b64decode(response_json['img']), os.path.join(self.cur_path, 'qrcode.jpg'))
        showImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        # 检测二维码状态
        qr_id = response_json['qrId']
        while True:
            response = self.session.get(self.check_url.format(qr_id, int(time.time() * 1000)), verify=False)
            response_json = response.json()
            # --扫码成功
            if response_json['ret'] in [0]:
                break
            # --等待/正在扫码
            elif response_json['ret'] in [32000]:
                pass
            # --其他原因
            else:
                raise RuntimeError(response_json.get('msg', 'something error'))
            time.sleep(0.5)
        # 登录成功
        removeImage(os.path.join(self.cur_path, 'qrcode.jpg'))
        print('[INFO]: Account -> %s, login successfully' % response_json['uid'])
        infos_return = {'username': username}
        infos_return.update(response_json)
        return infos_return, self.session
    '''初始化'''
    def __initialize(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        }
        self.qrcode_url = 'https://passport.ximalaya.com/web/qrCode/gen?level=L'
        self.check_url = 'https://passport.ximalaya.com/web/qrCode/check/{}/{}'
        self.session.headers.update(self.headers)


'''
Function:
    喜马拉雅模拟登录
Detail:
    -login:
        Input:
            --username: 用户名
            --password: 密码
            --mode: mobile/pc/scanqr
            --crack_captcha_func: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
            --proxies: 为requests.Session()设置代理
        Return:
            --infos_return: 用户名等信息
            --session: 登录后的requests.Session()
'''
class ximalaya():
    def __init__(self, **kwargs):
        self.info = 'login in ximalaya'
        self.supported_modes = {
            'pc': ximalayaPC(**kwargs),
            'mobile': ximalayaMobile(**kwargs),
            'scanqr': ximalayaScanqr(**kwargs),
        }
    '''登录函数'''
    def login(self, username='', password='', mode='scanqr', crack_captcha_func=None, **kwargs):
        assert mode in self.supported_modes, 'unsupport mode %s in ximalaya.login' % mode
        selected_api = self.supported_modes[mode]
        if not selected_api.is_callable: raise NotImplementedError('not be implemented for mode %s in ximalaya.login' % mode)
        args = {
            'username': username,
            'password': password,
            'crack_captcha_func': crack_captcha_func,
        }
        args.update(kwargs)
        return selected_api.login(**args)


