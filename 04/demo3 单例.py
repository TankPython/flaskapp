#coding:utf-8

# 实例化一个单例
class a(object):
    def __init__(self,age,name):
        age ="11"
        name = 1


class Singleton(a):
    instance = None

    def __new__(cls, age, name):
        #如果类属性__instance的值为None，
        #那么就创建一个对象，并且赋值为这个对象的引用，保证下次调用这个方法时
        #能够知道之前已经创建过对象了，这样就保证了只有1个对象
        if not cls.instance:
            cls.instance = a.__new__(cls)
            print cls.instance
            cls.instance = a.__new__(Singleton)
            print cls.instance
            cls.instance = super(Singleton,cls).__new__(Singleton)
            print cls.instance

            # cls.instance = object.__new__(a)
            # print cls.instance
        return cls.instance

a = Singleton(18, "dongGe")
b = Singleton(8, "dongGe")

print(id(a))
print(id(b))

a.age = 19 #给a指向的对象添加一个属性
print b.age #获取b指向的对象的age属性