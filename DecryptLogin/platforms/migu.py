'''
Function:
	咪咕音乐模拟登录
		--PC端: http://www.migu.cn/
		--移动端暂不支持
Author:
	Charles
微信公众号:
	Charles的皮卡丘
GitHub:
	https://github.com/CharlesPikachu
更新日期:
	2020-04-11
'''
import execjs
import requests


'''js code'''
encrypt_js_code = r'''
navigator = {};
window = {};

function d(a, b, c) {
    null != a && ("number" == typeof a ? this.fromNumber(a, b, c) : null == b && "string" != typeof a ? this.fromString(a, 256) : this.fromString(a, b))
}

function e() {
    return new d(null)
}

function f(a, b, c, d, e, f) {
    for (; --f >= 0;) {
        var g = b * this[a++] + c[d] + e;
        e = Math.floor(g / 67108864),
            c[d++] = 67108863 & g
    }
    return e
}

function g(a, b, c, d, e, f) {
    for (var g = 32767 & b, h = b >> 15; --f >= 0;) {
        var i = 32767 & this[a]
            , j = this[a++] >> 15
            , k = h * i + j * g;
        i = g * i + ((32767 & k) << 15) + c[d] + (1073741823 & e),
            e = (i >>> 30) + (k >>> 15) + h * j + (e >>> 30),
            c[d++] = 1073741823 & i
    }
    return e
}

function h(a, b, c, d, e, f) {
    for (var g = 16383 & b, h = b >> 14; --f >= 0;) {
        var i = 16383 & this[a]
            , j = this[a++] >> 14
            , k = h * i + j * g;
        i = g * i + ((16383 & k) << 14) + c[d] + e,
            e = (i >> 28) + (k >> 14) + h * j,
            c[d++] = 268435455 & i
    }
    return e
}

function i(a) {
    return nb.charAt(a)
}

function j(a, b) {
    var c = ob[a.charCodeAt(b)];
    return null == c ? -1 : c
}

function k(a) {
    for (var b = this.t - 1; b >= 0; --b)
        a[b] = this[b];
    a.t = this.t,
        a.s = this.s
}

function l(a) {
    this.t = 1,
        this.s = 0 > a ? -1 : 0,
        a > 0 ? this[0] = a : -1 > a ? this[0] = a + this.DV : this.t = 0
}

function m(a) {
    var b = e();
    return b.fromInt(a),
        b
}

function n(a, b) {
    var c;
    if (16 == b)
        c = 4;
    else if (8 == b)
        c = 3;
    else if (256 == b)
        c = 8;
    else if (2 == b)
        c = 1;
    else if (32 == b)
        c = 5;
    else {
        if (4 != b)
            return void this.fromRadix(a, b);
        c = 2
    }
    this.t = 0,
        this.s = 0;
    for (var e = a.length, f = !1, g = 0; --e >= 0;) {
        var h = 8 == c ? 255 & a[e] : j(a, e);
        0 > h ? "-" == a.charAt(e) && (f = !0) : (f = !1,
            0 == g ? this[this.t++] = h : g + c > this.DB ? (this[this.t - 1] |= (h & (1 << this.DB - g) - 1) << g,
                this[this.t++] = h >> this.DB - g) : this[this.t - 1] |= h << g,
            g += c,
        g >= this.DB && (g -= this.DB))
    }
    8 == c && 0 != (128 & a[0]) && (this.s = -1,
    g > 0 && (this[this.t - 1] |= (1 << this.DB - g) - 1 << g)),
        this.clamp(),
    f && d.ZERO.subTo(this, this)
}

function o() {
    for (var a = this.s & this.DM; this.t > 0 && this[this.t - 1] == a;)
        --this.t
}

function p(a) {
    if (this.s < 0)
        return "-" + this.negate().toString(a);
    var b;
    if (16 == a)
        b = 4;
    else if (8 == a)
        b = 3;
    else if (2 == a)
        b = 1;
    else if (32 == a)
        b = 5;
    else {
        if (4 != a)
            return this.toRadix(a);
        b = 2
    }
    var c, d = (1 << b) - 1, e = !1, f = "", g = this.t, h = this.DB - g * this.DB % b;
    if (g-- > 0)
        for (h < this.DB && (c = this[g] >> h) > 0 && (e = !0,
            f = i(c)); g >= 0;)
            b > h ? (c = (this[g] & (1 << h) - 1) << b - h,
                c |= this[--g] >> (h += this.DB - b)) : (c = this[g] >> (h -= b) & d,
            0 >= h && (h += this.DB,
                --g)),
            c > 0 && (e = !0),
            e && (f += i(c));
    return e ? f : "0"
}

function q() {
    var a = e();
    return d.ZERO.subTo(this, a),
        a
}

function r() {
    return this.s < 0 ? this.negate() : this
}

function s(a) {
    var b = this.s - a.s;
    if (0 != b)
        return b;
    var c = this.t;
    if (b = c - a.t,
    0 != b)
        return this.s < 0 ? -b : b;
    for (; --c >= 0;)
        if (0 != (b = this[c] - a[c]))
            return b;
    return 0
}

function t(a) {
    var b, c = 1;
    return 0 != (b = a >>> 16) && (a = b,
        c += 16),
    0 != (b = a >> 8) && (a = b,
        c += 8),
    0 != (b = a >> 4) && (a = b,
        c += 4),
    0 != (b = a >> 2) && (a = b,
        c += 2),
    0 != (b = a >> 1) && (a = b,
        c += 1),
        c
}

function u() {
    return this.t <= 0 ? 0 : this.DB * (this.t - 1) + t(this[this.t - 1] ^ this.s & this.DM)
}

function v(a, b) {
    var c;
    for (c = this.t - 1; c >= 0; --c)
        b[c + a] = this[c];
    for (c = a - 1; c >= 0; --c)
        b[c] = 0;
    b.t = this.t + a,
        b.s = this.s
}

function w(a, b) {
    for (var c = a; c < this.t; ++c)
        b[c - a] = this[c];
    b.t = Math.max(this.t - a, 0),
        b.s = this.s
}

function x(a, b) {
    var c, d = a % this.DB, e = this.DB - d, f = (1 << e) - 1, g = Math.floor(a / this.DB),
        h = this.s << d & this.DM;
    for (c = this.t - 1; c >= 0; --c)
        b[c + g + 1] = this[c] >> e | h,
            h = (this[c] & f) << d;
    for (c = g - 1; c >= 0; --c)
        b[c] = 0;
    b[g] = h,
        b.t = this.t + g + 1,
        b.s = this.s,
        b.clamp()
}

function y(a, b) {
    b.s = this.s;
    var c = Math.floor(a / this.DB);
    if (c >= this.t)
        return void (b.t = 0);
    var d = a % this.DB
        , e = this.DB - d
        , f = (1 << d) - 1;
    b[0] = this[c] >> d;
    for (var g = c + 1; g < this.t; ++g)
        b[g - c - 1] |= (this[g] & f) << e,
            b[g - c] = this[g] >> d;
    d > 0 && (b[this.t - c - 1] |= (this.s & f) << e),
        b.t = this.t - c,
        b.clamp()
}

function z(a, b) {
    for (var c = 0, d = 0, e = Math.min(a.t, this.t); e > c;)
        d += this[c] - a[c],
            b[c++] = d & this.DM,
            d >>= this.DB;
    if (a.t < this.t) {
        for (d -= a.s; c < this.t;)
            d += this[c],
                b[c++] = d & this.DM,
                d >>= this.DB;
        d += this.s
    } else {
        for (d += this.s; c < a.t;)
            d -= a[c],
                b[c++] = d & this.DM,
                d >>= this.DB;
        d -= a.s
    }
    b.s = 0 > d ? -1 : 0,
        -1 > d ? b[c++] = this.DV + d : d > 0 && (b[c++] = d),
        b.t = c,
        b.clamp()
}

function A(a, b) {
    var c = this.abs()
        , e = a.abs()
        , f = c.t;
    for (b.t = f + e.t; --f >= 0;)
        b[f] = 0;
    for (f = 0; f < e.t; ++f)
        b[f + c.t] = c.am(0, e[f], b, f, 0, c.t);
    b.s = 0,
        b.clamp(),
    this.s != a.s && d.ZERO.subTo(b, b)
}

function B(a) {
    for (var b = this.abs(), c = a.t = 2 * b.t; --c >= 0;)
        a[c] = 0;
    for (c = 0; c < b.t - 1; ++c) {
        var d = b.am(c, b[c], a, 2 * c, 0, 1);
        (a[c + b.t] += b.am(c + 1, 2 * b[c], a, 2 * c + 1, d, b.t - c - 1)) >= b.DV && (a[c + b.t] -= b.DV,
            a[c + b.t + 1] = 1)
    }
    a.t > 0 && (a[a.t - 1] += b.am(c, b[c], a, 2 * c, 0, 1)),
        a.s = 0,
        a.clamp()
}

function C(a, b, c) {
    var f = a.abs();
    if (!(f.t <= 0)) {
        var g = this.abs();
        if (g.t < f.t)
            return null != b && b.fromInt(0),
                void (null != c && this.copyTo(c));
        null == c && (c = e());
        var h = e()
            , i = this.s
            , j = a.s
            , k = this.DB - t(f[f.t - 1]);
        k > 0 ? (f.lShiftTo(k, h),
            g.lShiftTo(k, c)) : (f.copyTo(h),
            g.copyTo(c));
        var l = h.t
            , m = h[l - 1];
        if (0 != m) {
            var n = m * (1 << this.F1) + (l > 1 ? h[l - 2] >> this.F2 : 0)
                , o = this.FV / n
                , p = (1 << this.F1) / n
                , q = 1 << this.F2
                , r = c.t
                , s = r - l
                , u = null == b ? e() : b;
            for (h.dlShiftTo(s, u),
                 c.compareTo(u) >= 0 && (c[c.t++] = 1,
                     c.subTo(u, c)),
                     d.ONE.dlShiftTo(l, u),
                     u.subTo(h, h); h.t < l;)
                h[h.t++] = 0;
            for (; --s >= 0;) {
                var v = c[--r] == m ? this.DM : Math.floor(c[r] * o + (c[r - 1] + q) * p);
                if ((c[r] += h.am(0, v, c, s, 0, l)) < v)
                    for (h.dlShiftTo(s, u),
                             c.subTo(u, c); c[r] < --v;)
                        c.subTo(u, c)
            }
            null != b && (c.drShiftTo(l, b),
            i != j && d.ZERO.subTo(b, b)),
                c.t = l,
                c.clamp(),
            k > 0 && c.rShiftTo(k, c),
            0 > i && d.ZERO.subTo(c, c)
        }
    }
}

function D(a) {
    var b = e();
    return this.abs().divRemTo(a, null, b),
    this.s < 0 && b.compareTo(d.ZERO) > 0 && a.subTo(b, b),
        b
}

function E(a) {
    this.m = a
}

function F(a) {
    return a.s < 0 || a.compareTo(this.m) >= 0 ? a.mod(this.m) : a
}

function G(a) {
    return a
}

function H(a) {
    a.divRemTo(this.m, null, a)
}

function I(a, b, c) {
    a.multiplyTo(b, c),
        this.reduce(c)
}

function J(a, b) {
    a.squareTo(b),
        this.reduce(b)
}

function K() {
    if (this.t < 1)
        return 0;
    var a = this[0];
    if (0 == (1 & a))
        return 0;
    var b = 3 & a;
    return b = b * (2 - (15 & a) * b) & 15,
        b = b * (2 - (255 & a) * b) & 255,
        b = b * (2 - ((65535 & a) * b & 65535)) & 65535,
        b = b * (2 - a * b % this.DV) % this.DV,
        b > 0 ? this.DV - b : -b
}

function L(a) {
    this.m = a,
        this.mp = a.invDigit(),
        this.mpl = 32767 & this.mp,
        this.mph = this.mp >> 15,
        this.um = (1 << a.DB - 15) - 1,
        this.mt2 = 2 * a.t
}

function M(a) {
    var b = e();
    return a.abs().dlShiftTo(this.m.t, b),
        b.divRemTo(this.m, null, b),
    a.s < 0 && b.compareTo(d.ZERO) > 0 && this.m.subTo(b, b),
        b
}

function N(a) {
    var b = e();
    return a.copyTo(b),
        this.reduce(b),
        b
}

function O(a) {
    for (; a.t <= this.mt2;)
        a[a.t++] = 0;
    for (var b = 0; b < this.m.t; ++b) {
        var c = 32767 & a[b]
            , d = c * this.mpl + ((c * this.mph + (a[b] >> 15) * this.mpl & this.um) << 15) & a.DM;
        for (c = b + this.m.t,
                 a[c] += this.m.am(0, d, a, b, 0, this.m.t); a[c] >= a.DV;)
            a[c] -= a.DV,
                a[++c]++
    }
    a.clamp(),
        a.drShiftTo(this.m.t, a),
    a.compareTo(this.m) >= 0 && a.subTo(this.m, a)
}

function P(a, b) {
    a.squareTo(b),
        this.reduce(b)
}

function Q(a, b, c) {
    a.multiplyTo(b, c),
        this.reduce(c)
}

function R() {
    return 0 == (this.t > 0 ? 1 & this[0] : this.s)
}

function S(a, b) {
    if (a > 4294967295 || 1 > a)
        return d.ONE;
    var c = e()
        , f = e()
        , g = b.convert(this)
        , h = t(a) - 1;
    for (g.copyTo(c); --h >= 0;)
        if (b.sqrTo(c, f),
        (a & 1 << h) > 0)
            b.mulTo(f, g, c);
        else {
            var i = c;
            c = f,
                f = i
        }
    return b.revert(c)
}

function T(a, b) {
    var c;
    return c = 256 > a || b.isEven() ? new E(b) : new L(b),
        this.exp(a, c)
}

function U() {
    this.i = 0,
        this.j = 0,
        this.S = new Array
}

function V(a) {
    var b, c, d;
    for (b = 0; 256 > b; ++b)
        this.S[b] = b;
    for (c = 0,
             b = 0; 256 > b; ++b)
        c = c + this.S[b] + a[b % a.length] & 255,
            d = this.S[b],
            this.S[b] = this.S[c],
            this.S[c] = d;
    this.i = 0,
        this.j = 0
}

function W() {
    var a;
    return this.i = this.i + 1 & 255,
        this.j = this.j + this.S[this.i] & 255,
        a = this.S[this.i],
        this.S[this.i] = this.S[this.j],
        this.S[this.j] = a,
        this.S[a + this.S[this.i] & 255]
}

function X() {
    return new U
}

function Y(a) {
    qb[rb++] ^= 255 & a,
        qb[rb++] ^= a >> 8 & 255,
        qb[rb++] ^= a >> 16 & 255,
        qb[rb++] ^= a >> 24 & 255,
    rb >= sb && (rb -= sb)
}

function Z() {
    Y((new Date).getTime())
}

function $() {
    if (null == pb) {
        for (Z(),
                 pb = X(),
                 pb.init(qb),
                 rb = 0; rb < qb.length; ++rb)
            qb[rb] = 0;
        rb = 0
    }
    return pb.next()
}

function _(a) {
    var b;
    for (b = 0; b < a.length; ++b)
        a[b] = $()
}

function ab() {
}

function bb(a, b) {
    return new d(a, b)
}

function cb(a, b) {
    if (b < a.length + 11)
        return alert("Message too long for RSA"),
            null;
    for (var c = new Array, e = a.length - 1; e >= 0 && b > 0;) {
        var f = a.charCodeAt(e--);
        128 > f ? c[--b] = f : f > 127 && 2048 > f ? (c[--b] = 63 & f | 128,
            c[--b] = f >> 6 | 192) : (c[--b] = 63 & f | 128,
            c[--b] = f >> 6 & 63 | 128,
            c[--b] = f >> 12 | 224)
    }
    c[--b] = 0;
    for (var g = new ab, h = new Array; b > 2;) {
        for (h[0] = 0; 0 == h[0];)
            g.nextBytes(h);
        c[--b] = h[0]
    }
    return c[--b] = 2,
        c[--b] = 0,
        new d(c)
}

function db() {
    this.n = null,
        this.e = 0,
        this.d = null,
        this.p = null,
        this.q = null,
        this.dmp1 = null,
        this.dmq1 = null,
        this.coeff = null
}

function eb(a, b) {
    null != a && null != b && a.length > 0 && b.length > 0 ? (this.n = bb(a, 16),
        this.e = parseInt(b, 16)) : alert("网络异常，请点击登录重试")
}

function fb(a) {
    return a.modPowInt(this.e, this.n)
}

function gb(a) {
    var b = cb(a, this.n.bitLength() + 7 >> 3);
    if (null == b)
        return null;
    var c = this.doPublic(b);
    if (null == c)
        return null;
    var d = c.toString(16);
    return 0 == (1 & d.length) ? d : "0" + d
}

var hb, ib = 0xdeadbeefcafe, jb = 15715070 == (16777215 & ib);
jb && "Microsoft Internet Explorer" == navigator.appName ? (d.prototype.am = g,
    hb = 30) : jb && "Netscape" != navigator.appName ? (d.prototype.am = f,
    hb = 26) : (d.prototype.am = h,
    hb = 28),
    d.prototype.DB = hb,
    d.prototype.DM = (1 << hb) - 1,
    d.prototype.DV = 1 << hb;
var kb = 52;
d.prototype.FV = Math.pow(2, kb),
    d.prototype.F1 = kb - hb,
    d.prototype.F2 = 2 * hb - kb;
var lb, mb, nb = "0123456789abcdefghijklmnopqrstuvwxyz", ob = new Array;
for (lb = "0".charCodeAt(0),
         mb = 0; 9 >= mb; ++mb)
    ob[lb++] = mb;
for (lb = "a".charCodeAt(0),
         mb = 10; 36 > mb; ++mb)
    ob[lb++] = mb;
for (lb = "A".charCodeAt(0),
         mb = 10; 36 > mb; ++mb)
    ob[lb++] = mb;
E.prototype.convert = F,
    E.prototype.revert = G,
    E.prototype.reduce = H,
    E.prototype.mulTo = I,
    E.prototype.sqrTo = J,
    L.prototype.convert = M,
    L.prototype.revert = N,
    L.prototype.reduce = O,
    L.prototype.mulTo = Q,
    L.prototype.sqrTo = P,
    d.prototype.copyTo = k,
    d.prototype.fromInt = l,
    d.prototype.fromString = n,
    d.prototype.clamp = o,
    d.prototype.dlShiftTo = v,
    d.prototype.drShiftTo = w,
    d.prototype.lShiftTo = x,
    d.prototype.rShiftTo = y,
    d.prototype.subTo = z,
    d.prototype.multiplyTo = A,
    d.prototype.squareTo = B,
    d.prototype.divRemTo = C,
    d.prototype.invDigit = K,
    d.prototype.isEven = R,
    d.prototype.exp = S,
    d.prototype.toString = p,
    d.prototype.negate = q,
    d.prototype.abs = r,
    d.prototype.compareTo = s,
    d.prototype.bitLength = u,
    d.prototype.mod = D,
    d.prototype.modPowInt = T,
    d.ZERO = m(0),
    d.ONE = m(1),
    U.prototype.init = V,
    U.prototype.next = W;
var pb, qb, rb, sb = 256;
if (null == qb) {
    qb = new Array,
        rb = 0;
    var tb;
    if (window.crypto && window.crypto.getRandomValues) {
        var ub = new Uint8Array(32);
        for (window.crypto.getRandomValues(ub),
                 tb = 0; 32 > tb; ++tb)
            qb[rb++] = ub[tb]
    }
    if ("Netscape" == navigator.appName && navigator.appVersion < "5" && window.crypto) {
        var vb = window.crypto.random(32);
        for (tb = 0; tb < vb.length; ++tb)
            qb[rb++] = 255 & vb.charCodeAt(tb)
    }
    for (; sb > rb;)
        tb = Math.floor(65536 * Math.random()),
            qb[rb++] = tb >>> 8,
            qb[rb++] = 255 & tb;
    rb = 0,
        Z()
}
ab.prototype.nextBytes = _,
    db.prototype.doPublic = fb,
    db.prototype.setPublic = eb,
    db.prototype.encrypt = gb,
    RSAKey = db;

function getEnpassword(pwd, pk) {
    c = new RSAKey;
    c.setPublic(pk.result.modulus, pk.result.publicExponent);
    return c.encrypt(pwd);
}

function rsaFingerprint(a, b) {
    var c = '"{"user_agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.13","language":"zh-CN","color_depth":"24","pixel_ratio":"1.5","hardware_concurrency":"12","resolution":"1280,720","available_resolution":"1280,680","timezone_offset":"-480","session_storage":"1","local_storage":"1","indexed_db":"1","open_database":"1","cpu_class":"unknown","navigator_platform":"Win32","do_not_track":"unknown","regular_plugins":"Chrome PDF Plugin::Portable Document Format::application/x-google-chrome-pdf~pdf,Chrome PDF Viewer::","webgl_vendor":"Google Inc.~ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)","adblock":"false","has_lied_languages":"false","has_lied_resolution":"false","has_lied_os":"false","has_lied_browser":"false","touch_support":"0,false,false","js_fonts":"Arial,Arial Black,Arial Narrow,Book Antiqua,Bookman Old Style,Calibri,Cambria,Cambria Math,Century,C"}"\n'
        , d = '6bd45ab31de0d0e446385addaee5ed78'
        , e = c.length
        , f = ""
        , g = new RSAKey;
    g.setPublic(a, b);
    for (var h = g.encrypt(d), i = 0; e > i; i += 117)
        f += g.encrypt(c.substr(i, 117));
    return {
        details: f,
        result: h
    }
}

function getFingerPrint(pk) {
    var b = rsaFingerprint(pk.result.modulus, pk.result.publicExponent);
    return b
}

function getRsaAccout(account, pk) {
    c = new RSAKey;
    c.setPublic(pk.result.modulus, pk.result.publicExponent);
    return c.encrypt(account);
}
'''


'''
Function:
	咪咕音乐模拟登录
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
class migu():
	def __init__(self, **kwargs):
		self.info = 'migu'
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
			# 编译js代码
			js = execjs.compile(encrypt_js_code)
			# 获得publickey
			res = self.session.post(self.publickey_url)
			publickey = res.json()
			# 获得finger print
			finger_print = js.call('getFingerPrint', publickey)
			# 模拟登录
			data = {
						'sourceID': '208003',
						'appType': '0',
						'relayState': '',
						'loginID': js.call('getRsaAccout', username, publickey),
						'enpassword': js.call('getEnpassword', password, publickey),
						'captcha': '',
						'imgcodeType': '1',
						'rememberMeBox': '1',
						'fingerPrint': finger_print.get('details', ''),
						'fingerPrintDetail': finger_print.get('details', ''),
						'isAsync': 'true'
					}
			res = self.session.post(self.login_url, data=data)
			res_json = res.json()
			# 登录成功
			if res_json['status'] == 2000:
				print('[INFO]: Account -> %s, login successfully...' % username)
				infos_return = {'username': username}
				infos_return.update(res_json)
				return infos_return, self.session
			# 账户密码错误
			elif res_json['status'] in [4001]:
				raise RuntimeError('Account -> %s, fail to login, username or password error...' % username)
			# 其他错误
			else:
				raise ValueError(res_json['message'])
		else:
			raise ValueError('Unsupport argument in migu.login -> mode %s, expect <mobile> or <pc>...' % mode)
	'''初始化PC端'''
	def __initializePC(self):
		self.headers = {
						'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
						'Origin': 'https://passport.migu.cn'
					}
		self.publickey_url = 'https://passport.migu.cn/password/publickey'
		self.login_url = 'https://passport.migu.cn/authn'
		self.session.headers.update(self.headers)
	'''初始化移动端'''
	def __initializeMobile(self):
		pass


'''test'''
if __name__ == '__main__':
	migu().login('', '')