# open(".txt", 'w') 擦去原纪录 重写
try:
    f = open('test.txt', 'w')
    f.write('HelloWorld' + '\n')
finally:
    # pass
    f.close()

# with 语句适用于对资源进行访问的场合，确保不管使用过程中是否发生异常都会执行必要的“清理”操作，释放资源，比如文件使用后自动关闭、线程中锁的自动获取和释放等。
#   open(".txt", 'a')   插入新数据

with open('test.txt', 'a') as f:
    f.write('Hello!' + '\n')
