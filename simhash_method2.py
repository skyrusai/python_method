# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import numpy as np
import json


class simhash:
    def __init__(self, content):
        self.simhash = self.simhash(content)

    def __str__(self):
        return str(self.simhash)

    def simhash(self, content):
        seg = jieba.cut(content)
        # for featu in seg:
        #     # print(featu)
        #     pass

        # jieba.analyse.set_stop_words('stopword.txt')
        # keyWord = jieba.analyse.extract_tags(
        #     '|'.join(seg), topK=50, withWeight=True, allowPOS=())  # 在这里对jieba的tfidf.py进行了修改
        # 将tags = sorted(freq.items(), key=itemgetter(1), reverse=True)修改成tags = sorted(freq.items(), key=itemgetter(1,0), reverse=True)
        # 即先按照权重排序，再按照词排序
        keyList = []
        # print(keyWord)
        for feature in seg:
            weight = int(1 * 20)
            print(feature)
            # print(weight)
            feature = self.string_hash(feature)
            print(feature)
            temp = []
            for i in feature:
                if (i == '1'):
                    temp.append(weight)
                else:
                    temp.append(-weight)
            # print(temp)
            keyList.append(temp)
        list1 = np.sum(np.array(keyList), axis=0)
        # print(list1)
        if (keyList == []):  # 编码读不出来
            return '00'
        simhash = ''
        for i in list1:
            if (i > 0):
                simhash = simhash + '1'
            else:
                simhash = simhash + '0'
        return simhash

    def string_hash(self, source):
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7  # 二进制计算 <<(右移)
            print(source)
            m = 1000003
            mask = 2 ** 128 - 1
            print(mask)
            for c in source:
                x = ((x * m) ^ ord(c)) & mask  # 二进制计算  &(与)
            x ^= len(source)
            if x == -1:
                x = -2
            x = bin(x).replace('0b', '').zfill(64)[-64:]
            # print(source, x)

            return str(x)

        '''
        以下是使用系统自带hash生成，虽然每次相同的会生成的一样，
        不过，对于不同的汉子产生的二进制，在计算海明码的距离会不一样，
        即每次产生的海明距离不一致
        所以不建议使用。
        '''
        # x=str(bin(hash(source)).replace('0b','').replace('-','').zfill(64)[-64:])
        # print(source,x,len(x))
        # return x

    def hammingDis(self, com):
        t1 = '0b' + self.simhash
        t2 = '0b' + com.simhash
        n = int(t1, 2) ^ int(t2, 2)  # 二进制计算 ^(异或)
        i = 0
        while n:
            n &= (n - 1)
            i += 1
        return i


outPutString0 = "．你好"
outPutString1 = "按照下面的条件列出比例，并且解比例．比例的两个外项分别是和，两个内项分别是x和．...."
outPutString2 = "按照下面的条件列出比例，并且解比例．比例的两个外项分别是和，两个内项分别是x和．"
outPutString3 = "如图，如果D和E成正比例，空格应填　 　；如果D和E成反比例，空格应填　 　．"
outPutString4 = "右表中，如果a和b成正比例，x应填　 　，如果a和b成反比例，x应填　 　． "
outPutString5 = "两个变量X和Y，当X•Y=45时，X和Y是（　　）A．成正比例量                      B．成反比例量                    C．不成比例量"
outPutString6 = "用一块橡皮泥捏不同的圆柱体，圆柱体的底面积和高（　　）A．成正比例                          B．成反比例                        C．不成比例"

if __name__ == '__main__':
    simhash(outPutString0)
    # print(simhash.hammingDis(simhash(outPutString0),simhash(outPutString1)))

    # https://blog.csdn.net/madujin/article/details/53152619
    # 16年blog
    # https://blog.csdn.net/kevinelstri/article/details/70139797
    # 17年blog
