'''
Function:
	知乎模拟登录
		--PC端: https://www.zhihu.com/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-31
'''
import os
import time
import hmac
import base64
import execjs
import hashlib
import requests
from ..utils.misc import *
from urllib.parse import urlencode
from requests_toolbelt import MultipartEncoder


'''js code'''
encrypt_js_code = r'''
window = {
    navigator: {
        userAgent: "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
}
function atob(str) {
  return Buffer.from(str, 'base64').toString('binary');
}
function f(module, exports, __webpack_require__) {
    "use strict";
    function t(e) {
        return (t = "function" == typeof Symbol && "symbol" == typeof Symbol.A ? function(e) {
            return typeof e
        }
        : function(e) {
            return e && "function" == typeof Symbol && e.constructor === Symbol && e !== Symbol.prototype ? "symbol" : typeof e
        }
        )(e)
    }
    exports['__esModule'] = !0
    var A = "2.0"
      , __g = {};
    function s() {}
    function i(e) {
        this.t = (2048 & e) >> 11,
        this.s = (1536 & e) >> 9,
        this.i = 511 & e,
        this.h = 511 & e
    }
    function h(e) {
        this.s = (3072 & e) >> 10,
        this.h = 1023 & e
    }
    function a(e) {
        this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
    }
    function c(e) {
        this.s = e >> 10 & 3,
        this.i = 1023 & e
    }
    function n() {}
    function e(e) {
        this.a = (3072 & e) >> 10,
        this.c = (768 & e) >> 8,
        this.n = (192 & e) >> 6,
        this.t = 63 & e
    }
    function o(e) {
        this.h = (4095 & e) >> 2,
        this.t = 3 & e
    }
    function r(e) {
        this.s = e >> 10 & 3,
        this.i = e >> 2 & 255,
        this.t = 3 & e
    }
    s.prototype.e = function(e) {
        e.o = !1
    }
    ,
    i.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.r[this.s] = this.i;
            break;
        case 1:
            e.r[this.s] = e.k[this.h]
        }
    }
    ,
    h.prototype.e = function(e) {
        e.k[this.h] = e.r[this.s]
    }
    ,
    a.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.r[this.a] = e.r[this.c] + e.r[this.n];
            break;
        case 1:
            e.r[this.a] = e.r[this.c] - e.r[this.n];
            break;
        case 2:
            e.r[this.a] = e.r[this.c] * e.r[this.n];
            break;
        case 3:
            e.r[this.a] = e.r[this.c] / e.r[this.n];
            break;
        case 4:
            e.r[this.a] = e.r[this.c] % e.r[this.n];
            break;
        case 5:
            e.r[this.a] = e.r[this.c] == e.r[this.n];
            break;
        case 6:
            e.r[this.a] = e.r[this.c] >= e.r[this.n];
            break;
        case 7:
            e.r[this.a] = e.r[this.c] || e.r[this.n];
            break;
        case 8:
            e.r[this.a] = e.r[this.c] && e.r[this.n];
            break;
        case 9:
            e.r[this.a] = e.r[this.c] !== e.r[this.n];
            break;
        case 10:
            e.r[this.a] = t(e.r[this.c]);
            break;
        case 11:
            e.r[this.a] = e.r[this.c]in e.r[this.n];
            break;
        case 12:
            e.r[this.a] = e.r[this.c] > e.r[this.n];
            break;
        case 13:
            e.r[this.a] = -e.r[this.c];
            break;
        case 14:
            e.r[this.a] = e.r[this.c] < e.r[this.n];
            break;
        case 15:
            e.r[this.a] = e.r[this.c] & e.r[this.n];
            break;
        case 16:
            e.r[this.a] = e.r[this.c] ^ e.r[this.n];
            break;
        case 17:
            e.r[this.a] = e.r[this.c] << e.r[this.n];
            break;
        case 18:
            e.r[this.a] = e.r[this.c] >>> e.r[this.n];
            break;
        case 19:
            e.r[this.a] = e.r[this.c] | e.r[this.n];
            break;
        case 20:
            e.r[this.a] = !e.r[this.c]
        }
    }
    ,
    c.prototype.e = function(e) {
        e.Q.push(e.C),
        e.B.push(e.k),
        e.C = e.r[this.s],
        e.k = [];
        for (var t = 0; t < this.i; t++)
            e.k.unshift(e.f.pop());
        e.g.push(e.f),
        e.f = []
    }
    ,
    n.prototype.e = function(e) {
        e.C = e.Q.pop(),
        e.k = e.B.pop(),
        e.f = e.g.pop()
    }
    ,
    e.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.u = e.r[this.a] >= e.r[this.c];
            break;
        case 1:
            e.u = e.r[this.a] <= e.r[this.c];
            break;
        case 2:
            e.u = e.r[this.a] > e.r[this.c];
            break;
        case 3:
            e.u = e.r[this.a] < e.r[this.c];
            break;
        case 4:
            e.u = e.r[this.a] == e.r[this.c];
            break;
        case 5:
            e.u = e.r[this.a] != e.r[this.c];
            break;
        case 6:
            e.u = e.r[this.a];
            break;
        case 7:
            e.u = !e.r[this.a]
        }
    }
    ,
    o.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.C = this.h;
            break;
        case 1:
            e.u && (e.C = this.h);
            break;
        case 2:
            e.u || (e.C = this.h);
            break;
        case 3:
            e.C = this.h,
            e.w = null
        }
        e.u = !1
    }
    ,
    r.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            for (var t = [], n = 0; n < this.i; n++)
                t.unshift(e.f.pop());
            e.r[3] = e.r[this.s](t[0], t[1]);
            break;
        case 1:
            for (var r = e.f.pop(), i = [], o = 0; o < this.i; o++)
                i.unshift(e.f.pop());
            e.r[3] = e.r[this.s][r](i[0], i[1]);
            break;
        case 2:
            for (var a = [], s = 0; s < this.i; s++)
                a.unshift(e.f.pop());
            e.r[3] = new e.r[this.s](a[0],a[1])
        }
    }
    ;
    var k = function(e) {
        for (var t = 66, n = [], r = 0; r < e.length; r++) {
            var i = 24 ^ e.charCodeAt(r) ^ t;
            n.push(String.fromCharCode(i)),
            t = i
        }
        return n.join("")
    };
    function Q(e) {
        this.t = (4095 & e) >> 10,
        this.s = (1023 & e) >> 8,
        this.i = 1023 & e,
        this.h = 63 & e
    }
    function C(e) {
        this.t = (4095 & e) >> 10,
        this.a = (1023 & e) >> 8,
        this.c = (255 & e) >> 6
    }
    function B(e) {
        this.s = (3072 & e) >> 10,
        this.h = 1023 & e
    }
    function f(e) {
        this.h = 4095 & e
    }
    function g(e) {
        this.s = (3072 & e) >> 10
    }
    function u(e) {
        this.h = 4095 & e
    }
    function w(e) {
        this.t = (3840 & e) >> 8,
        this.s = (192 & e) >> 6,
        this.i = 63 & e
    }
    function G() {
        this.r = [0, 0, 0, 0],
        this.C = 0,
        this.Q = [],
        this.k = [],
        this.B = [],
        this.f = [],
        this.g = [],
        this.u = !1,
        this.G = [],
        this.b = [],
        this.o = !1,
        this.w = null,
        this.U = null,
        this.F = [],
        this.R = 0,
        this.J = {
            0: s,
            1: i,
            2: h,
            3: a,
            4: c,
            5: n,
            6: e,
            7: o,
            8: r,
            9: Q,
            10: C,
            11: B,
            12: f,
            13: g,
            14: u,
            15: w
        }
    }
    Q.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            e.f.push(e.r[this.s]);
            break;
        case 1:
            e.f.push(this.i);
            break;
        case 2:
            e.f.push(e.k[this.h]);
            break;
        case 3:
            e.f.push(k(e.b[this.h]))
        }
    }
    ,
    C.prototype.e = function(A) {
        switch (this.t) {
        case 0:
            var t = A.f.pop();
            A.r[this.a] = A.r[this.c][t];
            break;
        case 1:
            var s = A.f.pop()
              , i = A.f.pop();
            A.r[this.c][s] = i;
            break;
        case 2:
            var h = A.f.pop();
            A.r[this.a] = eval(h)
        }
    }
    ,
    B.prototype.e = function(e) {
        e.r[this.s] = k(e.b[this.h])
    }
    ,
    f.prototype.e = function(e) {
        e.w = this.h
    }
    ,
    g.prototype.e = function(e) {
        throw e.r[this.s]
    }
    ,
    u.prototype.e = function(e) {
        var t = this
          , n = [0];
        e.k.forEach(function(e) {
            n.push(e)
        });
        var r = function(r) {
            var i = new G;
            return i.k = n,
            i.k[0] = r,
            i.v(e.G, t.h, e.b, e.F),
            i.r[3]
        };
        r.toString = function() {
            return "() { [native code] }"
        }
        ,
        e.r[3] = r
    }
    ,
    w.prototype.e = function(e) {
        switch (this.t) {
        case 0:
            for (var t = {}, n = 0; n < this.i; n++) {
                var r = e.f.pop();
                t[e.f.pop()] = r
            }
            e.r[this.s] = t;
            break;
        case 1:
            for (var i = [], o = 0; o < this.i; o++)
                i.unshift(e.f.pop());
            e.r[this.s] = i
        }
    }
    ,
    G.prototype.D = function(e) {
        for (var t = atob(e), n = t.charCodeAt(0) << 8 | t.charCodeAt(1), r = [], i = 2; i < n + 2; i += 2)
            r.push(t.charCodeAt(i) << 8 | t.charCodeAt(i + 1));
        this.G = r;
        for (var o = [], a = n + 2; a < t.length; ) {
            var s = t.charCodeAt(a) << 8 | t.charCodeAt(a + 1)
              , c = t.slice(a + 2, a + 2 + s);
            o.push(c),
            a += s + 2
        }
        this.b = o
    }
    ,
    G.prototype.v = function(e, t, n) {
        for (t = t || 0,
        n = n || [],
        this.C = t,
        "string" == typeof e ? this.D(e) : (this.G = e,
        this.b = n),
        this.o = !0,
        this.R = Date.now(); this.o; ) {
            var r = this.G[this.C++];
            if ("number" != typeof r)
                break;
            var i = Date.now();
            if (500 < i - this.R)
                return;
            this.R = i;
            try {
                this.e(r)
            } catch (e) {
                this.U = e,
                this.w && (this.C = this.w)
            }
        }
    }
    ,
    G.prototype.e = function(e) {
        var t = (61440 & e) >> 12;
        new this.J[t](e).e(this)
    }
    ,
    (new G).v("AxjgB5MAnACoAJwBpAAAABAAIAKcAqgAMAq0AzRJZAZwUpwCqACQACACGAKcBKAAIAOcBagAIAQYAjAUGgKcBqFAuAc5hTSHZAZwqrAIGgA0QJEAJAAYAzAUGgOcCaFANRQ0R2QGcOKwChoANECRACQAsAuQABgDnAmgAJwMgAGcDYwFEAAzBmAGcSqwDhoANECRACQAGAKcD6AAGgKcEKFANEcYApwRoAAxB2AGcXKwEhoANECRACQAGAKcE6AAGgKcFKFANEdkBnGqsBUaADRAkQAkABgCnBagAGAGcdKwFxoANECRACQAGAKcGKAAYAZx+rAZGgA0QJEAJAAYA5waoABgBnIisBsaADRAkQAkABgCnBygABoCnB2hQDRHZAZyWrAeGgA0QJEAJAAYBJwfoAAwFGAGcoawIBoANECRACQAGAOQALAJkAAYBJwfgAlsBnK+sCEaADRAkQAkABgDkACwGpAAGAScH4AJbAZy9rAiGgA0QJEAJACwI5AAGAScH6AAkACcJKgAnCWgAJwmoACcJ4AFnA2MBRAAMw5gBnNasCgaADRAkQAkABgBEio0R5EAJAGwKSAFGACcKqAAEgM0RCQGGAYSATRFZAZzshgAtCs0QCQAGAYSAjRFZAZz1hgAtCw0QCQAEAAgB7AtIAgYAJwqoAASATRBJAkYCRIANEZkBnYqEAgaBxQBOYAoBxQEOYQ0giQKGAmQABgAnC6ABRgBGgo0UhD/MQ8zECALEAgaBxQBOYAoBxQEOYQ0gpEAJAoYARoKNFIQ/zEPkAAgChgLGgkUATmBkgAaAJwuhAUaCjdQFAg5kTSTJAsQCBoHFAE5gCgHFAQ5hDSCkQAkChgBGgo0UhD/MQ+QACAKGAsaCRQCOYGSABoAnC6EBRoKN1AUEDmRNJMkCxgFGgsUPzmPkgAaCJwvhAU0wCQFGAUaCxQGOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQMOZISPzZPkQAaCJwvhAU0wCQFGAUaCxQSOZISPzZPkQAaCJwvhAU0wCQFGAkSAzRBJAlz/B4FUAAAAwUYIAAIBSITFQkTERwABi0GHxITAAAJLwMSGRsXHxMZAAk0Fw8HFh4NAwUABhU1EBceDwAENBcUEAAGNBkTGRcBAAFKAAkvHg4PKz4aEwIAAUsACDIVHB0QEQ4YAAsuAzs7AAoPKToKDgAHMx8SGQUvMQABSAALORoVGCQgERcCAxoACAU3ABEXAgMaAAsFGDcAERcCAxoUCgABSQAGOA8LGBsPAAYYLwsYGw8AAU4ABD8QHAUAAU8ABSkbCQ4BAAFMAAktCh8eDgMHCw8AAU0ADT4TGjQsGQMaFA0FHhkAFz4TGjQsGQMaFA0FHhk1NBkCHgUbGBEPAAFCABg9GgkjIAEmOgUHDQ8eFSU5DggJAwEcAwUAAUMAAUAAAUEADQEtFw0FBwtdWxQTGSAACBwrAxUPBR4ZAAkqGgUDAwMVEQ0ACC4DJD8eAx8RAAQ5GhUYAAFGAAAABjYRExELBAACWhgAAVoAQAg/PTw0NxcQPCQ5C3JZEBs9fkcnDRcUAXZia0Q4EhQgXHojMBY3MWVCNT0uDhMXcGQ7AUFPHigkQUwQFkhaAkEACjkTEQspNBMZPC0ABjkTEQsrLQ==");
    var b = function(e) {
        return __g._encrypt(encodeURIComponent(e))
    };
    exports.ENCRYPT_VERSION = A,
    exports.default = b
}

function encrypt(data) {
    const r = {exports: {}, i: 452, l: false}
    const o = f(r, r.exports)
    return r.exports.default(data)
}
'''


'''
Function:
	知乎模拟登录
Detail:
	-login:
		Input:
			--username: 用户名
			--password: 密码
			--mode: mobile/pc
			--crackvcFunc: 若提供验证码接口, 则利用该接口来实现验证码的自动识别
			--proxies: 为requests.Session()设置代理
		Return:
			--infos_return: 用户名等信息
			--session: 登录后的requests.Session()
'''
class zhihu():
	def __init__(self, **kwargs):
		self.info = 'zhihu'
		self.cur_path = os.getcwd()
		self.session = requests.Session()
	'''登录函数'''
	def login(self, username, password, mode='pc', crackvcFunc=None, **kwargs):
		# 设置代理
		self.session.proxies.update(kwargs.get('proxies', {}))
		# 移动端接口
		if mode == 'mobile':
			raise NotImplementedError
		# PC端接口
		elif mode == 'pc':
			self.__initializePC()
			# 初始化
			self.session.get(self.signin_url)
			# 验证码处理
			res = self.session.get(self.captcha_url, headers=self.captcha_headers)
			if 'true' in res.text:
				self.captcha_headers.update({'origin': 'https://www.zhihu.com'})
				res = self.session.put(self.captcha_url, headers=self.captcha_headers)
				img_base64 = res.json()['img_base64'].replace('\\n', '')
				saveImage(base64.b64decode(img_base64), os.path.join(self.cur_path, 'captcha.jpg'))
				if crackvcFunc is None:
					showImage(os.path.join(self.cur_path, 'captcha.jpg'))
					captcha = input('Input the Verification Code:')
				else:
					captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
				data = {'input_text': captcha}
				data = MultipartEncoder(fields=data, boundary='----WebKitFormBoundary')
				headers = {
							'content-type': data.content_type,
							'origin': 'https://www.zhihu.com',
							'referer': 'https://www.zhihu.com/signin',
							'x-requested-with': 'fetch'
						}
				self.session.post(self.captcha_url, data=data, headers=headers)
			removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
			# 构造登录请求
			client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
			timestamp = str(int(time.time() * 1000))
			grant_type = 'password'
			source = 'com.zhihu.web'
			signature = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
			signature.update(bytes((grant_type+client_id+source+timestamp), 'utf-8'))
			signature = signature.hexdigest()
			data = {
					'client_id': client_id,
					'grant_type': grant_type,
					'source': source,
					'username': '+86'+username,
					'password': password,
					'lang': 'en',
					'ref_source': 'other_https://www.zhihu.com/signin',
					'utm_source': '',
					'captcha': '',
					'timestamp': timestamp,
					'signature': signature
					}
			js = execjs.compile(encrypt_js_code)
			data = js.call('encrypt', urlencode(data))
			res = self.session.post(self.login_url, data=data, headers=self.login_headers)
			res_json = res.json()
			# 登录成功
			if 'user_id' in res_json:
				self.session.cookies.update(res_json['cookie'])
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账号密码错误
			elif 'error' in res_json and res_json.get('error').get('code') == 100005:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 验证码错误
			elif 'error' in res_json and res_json.get('error').get('code') == 120005:
				raise RuntimeError('Account -> %s, fail to login, crack captcha error...' % username)
			# 其他错误
			else:
				raise RuntimeError(res_json.get('error').get('message'))
		else:
			raise ValueError('Unsupport argument in zhihu.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
							'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
							'referer': 'https://www.zhihu.com/',
							'host': 'www.zhihu.com',
							'accept-encoding': 'gzip, deflate, br',
							'accept-language': 'zh-CN,zh;q=0.9',
							'accept': '*/*'
						}
		self.captcha_headers = {
									'referer': 'https://www.zhihu.com/signin',
									'x-requested-with': 'fetch',
									'x-zse-83': '3_2.0'
								}
		self.login_headers = {
								'content-type': 'application/x-www-form-urlencoded',
								'origin': 'https://www.zhihu.com',
								'referer': 'https://www.zhihu.com/signin',
								'x-requested-with': 'fetch',
								'x-zse-83': '3_2.0'
							}
		self.captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
		self.signin_url = 'https://www.zhihu.com/signin'
		self.login_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	zhihu().login('', '')