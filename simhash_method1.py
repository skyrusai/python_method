import re
import jieba
import hashlib
import numpy as np


def iter_join(*args):
    for arg in args:
        for elem in arg:
            yield elem


def cut_wrap():
    re_han = re.compile(r'[\u4e00-\u9fa5]')
    re_eng = re.compile(r'[a-zA-Z]')
    re_num = re.compile(r'\d')
    trans_map = {ord('.'): ord('。'), ord('*'): ord('1')}

    def __iter(s):
        for seg in jieba.cut(re.sub('\s', '', s)):
            if re_han.match(seg):
                yield seg
            elif re_eng.match(seg):
                yield seg.lower()
            elif re_num.match(seg):
                yield '*' * len(seg)
            else:
                yield seg

    def __wrapper():
        s = ''
        while True:
            s = yield __iter(s.translate(trans_map))

    wrapper = __wrapper()
    next(wrapper)
    return wrapper.send


class SimHash:
    def __init__(self, num):
        self.oct_digest = num

    def bin_digest(self):
        return bin(self.oct_digest)[2:]

    def hex_digest(self):
        return hex(self.oct_digest)[2:]


class CalculateSimHash:
    def __init__(self):
        self.__re_han = re.compile(u'[\u4e00-\u9fa5]+')
        self.__re_blank = re.compile('\s')

    def sim_hash(self, text='', length=128):
        res = 0
        feature_iters = [self.__text2feature_iter(word, length)
                         for word in iter_join(('',), cut(text))]
        for i in range(length):
            res <<= 1
            res += self.__sum2bin(next(feature_iter) for feature_iter in feature_iters)
        return SimHash(res)

    def sim_hamming(self, text1, text2):
        return self.hamming(self.sim_hash(text1).oct_digest, self.sim_hash(text2).oct_digest)

    @staticmethod
    def __sum2bin(num_iter):
        return sum(num_iter) > 0 and 1 or 0

    @staticmethod
    def hamming(x, y):
        r, s = 0, x ^ y
        while s:
            r += s & 1
            s >>= 1
        return r

    def __text2feature_iter(self, text, length):
        idf = self.__text2idf(text)
        for bin_pos in self.__text2md5_bin_iter(text, length):
            yield idf * (2 * bin_pos - 1)

    def __text2idf(self, text):
        if self.__re_han.match(text):
            return round(6 - np.log10((jieba.dt.FREQ.get(text) or 0) + 1))
        elif self.__re_blank.match(text):
            return 0
        else:
            return 1

    def __text2md5_bin_iter(self, text, length):
        md5_hex = self.__text2md5(text)
        for i in range(length):
            yield md5_hex & 1
            md5_hex >>= 1

    @staticmethod
    def __text2md5(text=''):
        # print(int(hashlib.md5(text.encode()).hexdigest(), 16))
        return int(hashlib.md5(text.encode()).hexdigest(), 16)


cut = cut_wrap()
csh = CalculateSimHash()
sim_hash = csh.sim_hash
hamming = csh.sim_hamming
sim_hamming = csh.sim_hamming

outPutString0 = "一个比例中，两个内项都是6，而且两个比的比值都是5，x是一个外项，列出这个比例并解答．"
outPutString1 = "一个比例中两个内项都是而且两个比的比值都是是一个外项列出这个比例并解答"
outPutString2 = "按照下面的条件列出比例，并且解比例．比例的两个外项分别是和，两个内项分别是x和．"
outPutString3 = "如图，如果D和E成正比例，空格应填　 　；如果D和E成反比例，空格应填　 　．"
outPutString4 = "右表中，如果a和b成正比例，x应填　 　，如果a和b成反比例，x应填　 　． "
outPutString5 = "两个变量X和Y，当X•Y=45时，X和Y是（　　）A．成正比例量                      B．成反比例量                    C．不成比例量"
outPutString6 = "用一块橡皮泥捏不同的圆柱体，圆柱体的底面积和高（　　）A．成正比例                          B．成反比例                        C．不成比例"

if __name__ == '__main__':
    print(sim_hash(outPutString0).hex_digest())
    # return str: fa0a4c3a3b88018544b9888755b0a869
    print(sim_hamming(outPutString0, outPutString1))
    # return 4

# https://www.cnblogs.com/Liqiongyu/p/6213323.html
# 16年blog
