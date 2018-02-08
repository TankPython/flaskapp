
#coding:utf-8

# class haha():
#     a = 10
#
# b = haha().a
#
# print b
class dog(object):
    def hhh(self):
        print 222

class Cat(object):
    def __init__(self,name):
        self.name = name
        self.color = 'yellow'

    def hhh(self):
        print "hhh"


class Bosi(Cat,dog):

    def __init__(self,name,a):
        self.a = a

        # 调用父类的__init__方法1(python2)
        # Cat.__init__(self,color)
        # 调用父类的__init__方法2
        super(Bosi,self).__init__(name)

        # 调用父类的__init__方法3
        # super().__init__(name)

    def getName(self):
        print self.color
        dog.hhh(self)
        return "aa"

bosi = Bosi('xiaohua',"a")

print(bosi.name)
print(bosi.color)
print bosi.getName()