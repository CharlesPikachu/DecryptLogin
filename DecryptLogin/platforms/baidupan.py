'''
Function:
	百度网盘模拟登录
		--PC端: https://wappass.baidu.com/wp/api/login
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-03-10
'''
import os
import re
import time
import json
import execjs
import requests
from ..utils.misc import *


'''js code'''
encrypt_js_code = r'''
function BarrettMu(t) {
    this.modulus = biCopy(t),
    this.k = biHighIndex(this.modulus) + 1;
    var e = new BigInt;
    e.digits[2 * this.k] = 1,
    this.mu = biDivide(e, this.modulus),
    this.bkplus1 = new BigInt,
    this.bkplus1.digits[this.k + 1] = 1,
    this.modulo = BarrettMu_modulo,
    this.multiplyMod = BarrettMu_multiplyMod,
    this.powMod = BarrettMu_powMod
}
function BarrettMu_modulo(t) {
    var e = biDivideByRadixPower(t, this.k - 1),
        i = biMultiply(e, this.mu),
        n = biDivideByRadixPower(i, this.k + 1),
        r = biModuloByRadixPower(t, this.k + 1),
        o = biMultiply(n, this.modulus),
        s = biModuloByRadixPower(o, this.k + 1),
        a = biSubtract(r, s);
    a.isNeg && (a = biAdd(a, this.bkplus1));
    for (var u = biCompare(a, this.modulus) >= 0; u;) a = biSubtract(a, this.modulus), u = biCompare(a, this.modulus) >= 0;
    return a
}
function BarrettMu_multiplyMod(t, e) {
    var i = biMultiply(t, e);
    return this.modulo(i)
}
function BarrettMu_powMod(t, e) {
    var i = new BigInt;
    i.digits[0] = 1;
    for (var n = t, r = e; 0 != (1 & r.digits[0]) && (i = this.multiplyMod(i, n)), r = biShiftRight(r, 1), 0 != r.digits[0] || 0 != biHighIndex(r);) n = this.multiplyMod(n, n);
    return i
}
function setMaxDigits(t) {
    maxDigits = t, ZERO_ARRAY = new Array(maxDigits);
    for (var e = 0; e < ZERO_ARRAY.length; e++) ZERO_ARRAY[e] = 0;
    bigZero = new BigInt, bigOne = new BigInt, bigOne.digits[0] = 1
}
function BigInt(t) {
    this.digits = "boolean" == typeof t && 1 == t ? null : ZERO_ARRAY.slice(0), this.isNeg = !1
}
function biFromDecimal(t) {
    for (var e, i = "-" == t.charAt(0), n = i ? 1 : 0; n < t.length && "0" == t.charAt(n);)++n;
    if (n == t.length) e = new BigInt;
    else {
        var r = t.length - n,
            o = r % dpl10;
        for (0 == o && (o = dpl10), e = biFromNumber(Number(t.substr(n, o))), n += o; n < t.length;) e = biAdd(biMultiply(e, lr10), biFromNumber(Number(t.substr(n, dpl10)))), n += dpl10;
        e.isNeg = i
    }
    return e
}
function biCopy(t) {
    var e = new BigInt(!0);
    return e.digits = t.digits.slice(0), e.isNeg = t.isNeg, e
}
function biFromNumber(t) {
    var e = new BigInt;
    e.isNeg = 0 > t, t = Math.abs(t);
    for (var i = 0; t > 0;) e.digits[i++] = t & maxDigitVal, t >>= biRadixBits;
    return e
}
function reverseStr(t) {
    for (var e = "", i = t.length - 1; i > -1; --i) e += t.charAt(i);
    return e
}
function biToString(t, e) {
    var i = new BigInt;
    i.digits[0] = e;
    for (var n = biDivideModulo(t, i), r = hexatrigesimalToChar[n[1].digits[0]]; 1 == biCompare(n[0], bigZero);) n = biDivideModulo(n[0], i), digit = n[1].digits[0], r += hexatrigesimalToChar[n[1].digits[0]];
    return (t.isNeg ? "-" : "") + reverseStr(r)
}
function biToDecimal(t) {
    var e = new BigInt;
    e.digits[0] = 10;
    for (var i = biDivideModulo(t, e), n = String(i[1].digits[0]); 1 == biCompare(i[0], bigZero);) i = biDivideModulo(i[0], e), n += String(i[1].digits[0]);
    return (t.isNeg ? "-" : "") + reverseStr(n)
}
function digitToHex(t) {
    var e = 15,
        n = "";
    for (i = 0; 4 > i; ++i) n += hexToChar[t & e], t >>>= 4;
    return reverseStr(n)
}
function biToHex(t) {
    for (var e = "", i = (biHighIndex(t), biHighIndex(t)); i > -1; --i) e += digitToHex(t.digits[i]);
    return e
}
function charToHex(t) {
    var e, i = 48,
        n = i + 9,
        r = 97,
        o = r + 25,
        s = 65,
        a = 90;
    return e = t >= i && n >= t ? t - i : t >= s && a >= t ? 10 + t - s : t >= r && o >= t ? 10 + t - r : 0
}
function hexToDigit(t) {
    for (var e = 0, i = Math.min(t.length, 4), n = 0; i > n; ++n) e <<= 4, e |= charToHex(t.charCodeAt(n));
    return e
}
function biFromHex(t) {
    for (var e = new BigInt, i = t.length, n = i, r = 0; n > 0; n -= 4, ++r) e.digits[r] = hexToDigit(t.substr(Math.max(n - 4, 0), Math.min(n, 4)));
    return e
}
function biFromString(t, e) {
    var i = "-" == t.charAt(0),
        n = i ? 1 : 0,
        r = new BigInt,
        o = new BigInt;
    o.digits[0] = 1;
    for (var s = t.length - 1; s >= n; s--) {
        var a = t.charCodeAt(s),
            u = charToHex(a),
            c = biMultiplyDigit(o, u);
        r = biAdd(r, c), o = biMultiplyDigit(o, e)
    }
    return r.isNeg = i, r
}
function biDump(t) {
    return (t.isNeg ? "-" : "") + t.digits.join(" ")
}
function biAdd(t, e) {
    var i;
    if (t.isNeg != e.isNeg) e.isNeg = !e.isNeg, i = biSubtract(t, e), e.isNeg = !e.isNeg;
    else {
        i = new BigInt;
        for (var n, r = 0, o = 0; o < t.digits.length; ++o) n = t.digits[o] + e.digits[o] + r, i.digits[o] = 65535 & n, r = Number(n >= biRadix);
        i.isNeg = t.isNeg
    }
    return i
}
function biSubtract(t, e) {
    var i;
    if (t.isNeg != e.isNeg) e.isNeg = !e.isNeg, i = biAdd(t, e), e.isNeg = !e.isNeg;
    else {
        i = new BigInt;
        var n, r;
        r = 0;
        for (var o = 0; o < t.digits.length; ++o) n = t.digits[o] - e.digits[o] + r, i.digits[o] = 65535 & n, i.digits[o] < 0 && (i.digits[o] += biRadix), r = 0 - Number(0 > n);
        if (-1 == r) {
            r = 0;
            for (var o = 0; o < t.digits.length; ++o) n = 0 - i.digits[o] + r, i.digits[o] = 65535 & n, i.digits[o] < 0 && (i.digits[o] += biRadix), r = 0 - Number(0 > n);
            i.isNeg = !t.isNeg
        } else i.isNeg = t.isNeg
    }
    return i
}
function biHighIndex(t) {
    for (var e = t.digits.length - 1; e > 0 && 0 == t.digits[e];)--e;
    return e
}
function biNumBits(t) {
    var e, i = biHighIndex(t),
        n = t.digits[i],
        r = (i + 1) * bitsPerDigit;
    for (e = r; e > r - bitsPerDigit && 0 == (32768 & n); --e) n <<= 1;
    return e
}
function biMultiply(t, e) {
    for (var i, n, r, o = new BigInt, s = biHighIndex(t), a = biHighIndex(e), u = 0; a >= u; ++u) {
        for (i = 0, r = u, j = 0; s >= j; ++j, ++r) n = o.digits[r] + t.digits[j] * e.digits[u] + i, o.digits[r] = n & maxDigitVal, i = n >>> biRadixBits;
        o.digits[u + s + 1] = i
    }
    return o.isNeg = t.isNeg != e.isNeg, o
}
function biMultiplyDigit(t, e) {
    var i, n, r;
    result = new BigInt, i = biHighIndex(t), n = 0;
    for (var o = 0; i >= o; ++o) r = result.digits[o] + t.digits[o] * e + n, result.digits[o] = r & maxDigitVal, n = r >>> biRadixBits;
    return result.digits[1 + i] = n, result
}
function arrayCopy(t, e, i, n, r) {
    for (var o = Math.min(e + r, t.length), s = e, a = n; o > s; ++s, ++a) i[a] = t[s]
}
function biShiftLeft(t, e) {
    var i = Math.floor(e / bitsPerDigit),
        n = new BigInt;
    arrayCopy(t.digits, 0, n.digits, i, n.digits.length - i);
    for (var r = e % bitsPerDigit, o = bitsPerDigit - r, s = n.digits.length - 1, a = s - 1; s > 0; --s, --a) n.digits[s] = n.digits[s] << r & maxDigitVal | (n.digits[a] & highBitMasks[r]) >>> o;
    return n.digits[0] = n.digits[s] << r & maxDigitVal, n.isNeg = t.isNeg, n
}
function biShiftRight(t, e) {
    var i = Math.floor(e / bitsPerDigit),
        n = new BigInt;
    arrayCopy(t.digits, i, n.digits, 0, t.digits.length - i);
    for (var r = e % bitsPerDigit, o = bitsPerDigit - r, s = 0, a = s + 1; s < n.digits.length - 1; ++s, ++a) n.digits[s] = n.digits[s] >>> r | (n.digits[a] & lowBitMasks[r]) << o;
    return n.digits[n.digits.length - 1] >>>= r, n.isNeg = t.isNeg, n
}
function biMultiplyByRadixPower(t, e) {
    var i = new BigInt;
    return arrayCopy(t.digits, 0, i.digits, e, i.digits.length - e), i
}
function biDivideByRadixPower(t, e) {
    var i = new BigInt;
    return arrayCopy(t.digits, e, i.digits, 0, i.digits.length - e), i
}
function biModuloByRadixPower(t, e) {
    var i = new BigInt;
    return arrayCopy(t.digits, 0, i.digits, 0, e), i
}
function biCompare(t, e) {
    if (t.isNeg != e.isNeg) return 1 - 2 * Number(t.isNeg);
    for (var i = t.digits.length - 1; i >= 0; --i) if (t.digits[i] != e.digits[i]) return t.isNeg ? 1 - 2 * Number(t.digits[i] > e.digits[i]) : 1 - 2 * Number(t.digits[i] < e.digits[i]);
    return 0
}
function biDivideModulo(t, e) {
    var i, n, r = biNumBits(t),
        o = biNumBits(e),
        s = e.isNeg;
    if (o > r) return t.isNeg ? (i = biCopy(bigOne), i.isNeg = !e.isNeg, t.isNeg = !1, e.isNeg = !1, n = biSubtract(e, t), t.isNeg = !0, e.isNeg = s) : (i = new BigInt, n = biCopy(t)), new Array(i, n);
    i = new BigInt, n = t;
    for (var a = Math.ceil(o / bitsPerDigit) - 1, u = 0; e.digits[a] < biHalfRadix;) e = biShiftLeft(e, 1), ++u, ++o, a = Math.ceil(o / bitsPerDigit) - 1;
    n = biShiftLeft(n, u), r += u;
    for (var c = Math.ceil(r / bitsPerDigit) - 1, l = biMultiplyByRadixPower(e, c - a); - 1 != biCompare(n, l);)++i.digits[c - a], n = biSubtract(n, l);
    for (var d = c; d > a; --d) {
        var f = d >= n.digits.length ? 0 : n.digits[d],
            h = d - 1 >= n.digits.length ? 0 : n.digits[d - 1],
            g = d - 2 >= n.digits.length ? 0 : n.digits[d - 2],
            p = a >= e.digits.length ? 0 : e.digits[a],
            m = a - 1 >= e.digits.length ? 0 : e.digits[a - 1];
        i.digits[d - a - 1] = f == p ? maxDigitVal : Math.floor((f * biRadix + h) / p);
        for (var v = i.digits[d - a - 1] * (p * biRadix + m), b = f * biRadixSquared + (h * biRadix + g); v > b;)--i.digits[d - a - 1], v = i.digits[d - a - 1] * (p * biRadix | m), b = f * biRadix * biRadix + (h * biRadix + g);
        l = biMultiplyByRadixPower(e, d - a - 1), n = biSubtract(n, biMultiplyDigit(l, i.digits[d - a - 1])), n.isNeg && (n = biAdd(n, l), --i.digits[d - a - 1])
    }
    return n = biShiftRight(n, u), i.isNeg = t.isNeg != s, t.isNeg && (i = s ? biAdd(i, bigOne) : biSubtract(i, bigOne), e = biShiftRight(e, u), n = biSubtract(e, n)), 0 == n.digits[0] && 0 == biHighIndex(n) && (n.isNeg = !1), new Array(i, n)
}
function biDivide(t, e) {
    return biDivideModulo(t, e)[0]
}
function biModulo(t, e) {
    return biDivideModulo(t, e)[1]
}
function biMultiplyMod(t, e, i) {
    return biModulo(biMultiply(t, e), i)
}
function biPow(t, e) {
    for (var i = bigOne, n = t; 0 != (1 & e) && (i = biMultiply(i, n)), e >>= 1, 0 != e;) n = biMultiply(n, n);
    return i
}
function biPowMod(t, e, i) {
    for (var n = bigOne, r = t, o = e; 0 != (1 & o.digits[0]) && (n = biMultiplyMod(n, r, i)), o = biShiftRight(o, 1), 0 != o.digits[0] || 0 != biHighIndex(o);) r = biMultiplyMod(r, r, i);
    return n
}
function RSAKeyPair(t, e, i) {
    this.e = biFromHex(t),
    this.d = biFromHex(e),
    this.m = biFromHex(i),
    console.log(this.e), console.log(this.d), console.log(this.m),
    this.chunkSize = 2 * biHighIndex(this.m),
    this.radix = 16,
    this.barrett = new BarrettMu(this.m)
}
function twoDigit(t) {
    return (10 > t ? "0" : "") + String(t)
}
function encryptedString(t, e) {
    for (var i = new Array, n = e.length, r = 0; n > r;) i[r] = e.charCodeAt(r), r++;
    for (; i.length % t.chunkSize != 0;) i[r++] = 0;
    var o, s, a, u = i.length,
        c = "";
    for (r = 0; u > r; r += t.chunkSize) {
        for (a = new BigInt, o = 0, s = r; s < r + t.chunkSize; ++o) a.digits[o] = i[s++], a.digits[o] += i[s++] << 8;
        var l = t.barrett.powMod(a, t.e),
            d = 16 == t.radix ? biToHex(l) : biToString(l, t.radix);
        c += d + " "
    }
    return c.substring(0, c.length - 1)
}
function encryptPass(pass, serverTime) {
    var password = SBCtoDBC(pass) + serverTime;
    setMaxDigits(131);
    console.log(password);
    var u = new RSAKeyPair("10001", "", "B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F");
    password = encryptedString(u, password);
    console.log(password);
    return password;
}
function SBCtoDBC(t) {
    var e = "";
    if (t) {
        for (var i = t.length, n = 0; i > n; n++) {
            var r = t.charCodeAt(n);
            r = r >= 65281 && 65374 >= r ? r - 65248 : r, r = 12288 == r ? 32 : r, e += String.fromCharCode(r)
        }
        return e
    }
}
function decryptedString(t, e) {
    var i, n, r, o = e.split(" "),
        s = "";
    for (i = 0; i < o.length; ++i) {
        var a;
        for (a = 16 == t.radix ? biFromHex(o[i]) : biFromString(o[i], t.radix), r = t.barrett.powMod(a, t.d), n = 0; n <= biHighIndex(r); ++n) s += String.fromCharCode(255 & r.digits[n], r.digits[n] >> 8)
    }
    return 0 == s.charCodeAt(s.length - 1) && (s = s.substring(0, s.length - 1)), s
}
var biRadixBase = 2,
    biRadixBits = 16,
    bitsPerDigit = biRadixBits,
    biRadix = 65536,
    biHalfRadix = biRadix >>> 1,
    biRadixSquared = biRadix * biRadix,
    maxDigitVal = biRadix - 1,
    maxInteger = 9999999999999998,
    maxDigits, ZERO_ARRAY, bigZero, bigOne;
setMaxDigits(20);
var dpl10 = 15,
    lr10 = biFromNumber(1e15),
    hexatrigesimalToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"),
    hexToChar = new Array("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"),
    highBitMasks = new Array(0, 32768, 49152, 57344, 61440, 63488, 64512, 65024, 65280, 65408, 65472, 65504, 65520, 65528, 65532, 65534, 65535),
    lowBitMasks = new Array(0, 1, 3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 16383, 32767, 65535);
'''


'''
Function:
	百度网盘模拟登录
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
class baidupan():
	def __init__(self, **kwargs):
		self.info = 'baidupan'
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
			# 访问home_url, 初始化cookies
			self.session.get(self.home_url)
			# 获得servertime
			servertime = self.__getServertime()
			# 获得publickkey
			publickkey_modulus, publickkey_exponent = self.__getPublicKey()
			# 获得traceid
			traceid = self.__getTraceId()
			# 加密password
			js = execjs.compile(encrypt_js_code)
			password = js.call("encryptPass", password, servertime)
			# 获得时间戳
			timestamp = str(int(time.time()/1000)) + '773_357'
			# 模拟登录
			is_need_captcha = False
			is_need_phone_email_verify = False
			captcha = ''
			codestring = ''
			vcodestr = ''
			goto_url = ''
			while True:
				# --需要图片验证码
				if is_need_captcha:
					res = self.session.get(self.genimage_url+codestring)
					saveImage(res.content, os.path.join(self.cur_path, 'captcha.jpg'))
					if crackvcFunc is None:
						showImage(os.path.join(self.cur_path, 'captcha.jpg'))
						captcha = input('Input the Verification Code:')
					else:
						captcha = crackvcFunc(os.path.join(self.cur_path, 'captcha.jpg'))
					removeImage(os.path.join(self.cur_path, 'captcha.jpg'))
				# --需要验证手机/邮箱
				if is_need_phone_email_verify:
					res_json = self.__verifyPhoneEmail(goto_url)
					self.session.get(res_json['data']['u'])
				# --不需要验证手机/邮箱, 直接构造并发送登录请求
				if not is_need_phone_email_verify:
					data = {
							'username': username,
							'password': password,
							'verifycode': captcha,
							'vcodestr': vcodestr,
							'isphone': '0',
							'loginmerge': '1',
							'action': 'login',
							'uid': timestamp,
							'skin': 'default_v2',
							'connect': '0',
							'dv': 'tk0.0095975573224773571583831604201@aadbAkqLI24oCwthDIxGB4p0K-2RKwxRuKp-sZxYJmRY9V2ZGq__rd0tmpV6wAk2zomRZ9DBLI24oCwthDIxGB4p0K-2RKwx-sntgOKCTp-9YAk2Y9SR~9-6QA4ChD1sH0BwGKwhDB4T~94xGMv4-MQsiM3CTCmmOEmuldwJ5hudj9HRYAkFRBdbsvLRAVqRoDBWp-Bwp-9Y9V0Qp-9wp-2wok9z9-2Z9k0Y9k2_jdVOrClMr9cAYxQsQMju348JrBjuZxgAY~wP3CXJ3XjJn0_~db9mRRAk2w9D1L9VFlAk2w9-uLokulAk2w9-uL9DB-pSRz9V0_',
							'getpassUrl': '/passport/getpass?clientfrom=&adapter=0&ssid=&from=&authsite=&bd_page_type=&uid="+timestamp+"&pu=&tpl=wimn&u=https://m.baidu.com/usrprofile%3Fuid%3D"+timestamp+"%23logined&type=&bdcm=060d5ffd462309f7e5529822720e0cf3d7cad665&tn=&regist_mode=&login_share_strategy=&subpro=wimn&skin=default_v2&client=&connect=0&smsLoginLink=1&loginLink=&bindToSmsLogin=&overseas=&is_voice_sms=&subpro=wimn&hideSLogin=&forcesetpwd=&regdomestic=',
							'mobilenum': 'undefined',
							'servertime': servertime,
							'gid': 'DA7C3AE-AF1F-48C0-AF9C-F1882CA37CD5',
							'logLoginType': 'wap_loginTouch',
							'FP_UID': '0b58c206c9faa8349576163341ef1321',
							'traceid': traceid
						}
					res = self.session.post(self.login_url, headers=self.login_headers, data=data)
					res_json = res.json()
				# --登录成功
				if res_json['errInfo'].get('no') in ['0']:
					print('[INFO]: Account -> %s, login successfully...' % username)
					infos_return = {'username': username}
					infos_return.update(res_json)
					return infos_return, self.session
				# --需要验证码
				elif res_json['errInfo'].get('no') in ['500002']:
					codestring = res_json['data'].get('codeString')
					is_need_captcha = True
				# --需要验证手机/邮箱
				elif res_json['errInfo'].get('no') in ['400101', '400023']:
					goto_url = res_json.get('data').get('gotoUrl')
					is_need_phone_email_verify = True
					is_need_captcha = False
				# --其他原因
				else:
					raise RuntimeError(res_json['errInfo'].get('msg'))
		else:
			raise ValueError('Unsupport argument in baidupan.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''手机/邮箱验证'''
	def __verifyPhoneEmail(self, goto_url):
		# 提取必要的数据
		res = self.session.get(goto_url)
		res.encoding = 'utf-8'
		raw_phone = re.search(r'<p class="verify-type-li-tiptop">(.*?)</p>\s+<p class="verify-type-li-tipbottom">通过手机验证码验证身份</p>', res.text)
		raw_email = re.search(r'<p class="verify-type-li-tiptop">(.*?)</p>\s+<p class="verify-type-li-tipbottom">通过邮箱验证码验证身份</p>', res.text)
		raw_token = re.search(r'token=([^&]+).*?&u=([^&]+)&', goto_url)
		phone = raw_phone.group(1) if raw_phone else None
		email = raw_phone.group(1) if raw_email else None
		token, u = raw_token.group(1), raw_token.group(2)
		# 选择验证方式
		verify_type = input('Your account has to be verified by using binded phone or email, please choose phone(enter 0, by default) or email(enter 1):')
		verify_type = 'email' if verify_type == '1' else 'mobile'
		# 发送验证码
		url = 'https://wappass.baidu.com/passport/authwidget?action=send&tpl=&type={}&token={}&from=&skin=&clientfrom=&adapter=2&updatessn=&bindToSmsLogin=&upsms=&finance='.format(verify_type, token)
		res = self.session.get(url)
		# 输入验证码
		vcodestr = input('Please enter the verify code you have accepted:')
		# 验证验证码
		headers = {
					'Connection': 'keep-alive',
					'Host': 'wappass.baidu.com',
					'Upgrade-Insecure-Requests': '1',
					'Pragma': 'no-cache'
				}
		timestamp = str(int(time.time())) + '773_357994'
		url = 'https://wappass.baidu.com/passport/authwidget?v={}&vcode={}&token={}&u={}&action=check&type={}&tpl=&skin=&clientfrom=&adapter=2&updatessn=&bindToSmsLogin=&isnew=&card_no=&finance=&callback=jsonp1'.format(timestamp, vcodestr, token, u, verify_type)
		res = self.session.get(url, headers=headers)
		res_json = res.text[len("jsonp1("): -1].strip()
		res_json = json.loads(res_json)
		return res_json
	'''获得servertime'''
	def __getServertime(self):
		res = self.session.get(self.servertime_url)
		servertime = res.json().get('time')
		return servertime
	'''获得publickey'''
	def __getPublicKey(self):
		res = self.session.get(self.publickkey_url)
		publickkey_modulus = re.findall(r',rsa:\"(.*?)\",error:', res.text)
		publickkey_modulus = publickkey_modulus[0] if len(publickkey_modulus) > 0 else "B3C61EBBA4659C4CE3639287EE871F1F48F7930EA977991C7AFE3CC442FEA49643212E7D570C853F368065CC57A2014666DA8AE7D493FD47D171C0D894EEE3ED7F99F6798B7FFD7B5873227038AD23E3197631A8CB642213B9F27D4901AB0D92BFA27542AE890855396ED92775255C977F5C302F1E7ED4B1E369C12CB6B1822F"
		publickkey_exponent = '10001'
		return publickkey_modulus, publickkey_exponent
	'''获得traceid'''
	def __getTraceId(self):
		res = self.session.get(self.traceid_url)
		traceid = res.headers.get('Trace-Id')
		return traceid
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
						'Referer': 'https://www.baidu.com/'
						}
		self.login_headers = {
								'Content-Type': 'application/x-www-form-urlencoded',
								'Accept': 'application/json',
								'Referer': 'https://wappass.baidu.com/',
								'X-Requested-With': 'XMLHttpRequest',
								'Connection': 'keep-alive'
							}
		self.home_url = 'https://www.baidu.com/'
		self.servertime_url = 'https://wappass.baidu.com/wp/api/security/antireplaytoken'
		self.publickkey_url = 'https://wappass.baidu.com/static/touch/js/login_d9bffc9.js'
		self.traceid_url = 'https://wappass.baidu.com/'
		self.login_url = 'https://wappass.baidu.com/wp/api/login'
		self.genimage_url = 'https://wappass.baidu.com/cgi-bin/genimage?'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	s = baidupan().login('', '')
	print(s)