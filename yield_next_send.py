def fun():
    for i in range(20):
        x = yield (i+1)
        print('good', x)


if __name__ == '__main__':
    a=fun()#初始化 已经循环一次了
    print(a)
    y=a.__next__()  # __next__使用
    print(y)#循环第二次 输出1
    z=a.send(5)     #send使用
    print(z)        #输出第三次循环 2
