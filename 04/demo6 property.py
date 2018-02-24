#coding:utf-8

class User(object):  # 这里必须传参数

    __id= 1

    @property
    def make(self):
        return self.__id

    @make.setter
    def make(self,value):
        if value>5:
            self.__id = 7
        else:
            self.__id = value+5

s = User()
print s.make
s.make = 5
print s.make
s.make = 6
print s.make


# class Student(object):
#     def __init__(self, name, score):
#         self.name = name
#         self.__score = score
#     def get_score(self):
#         return self.__score
#     def set_score(self, score):
#         if score < 0 or score > 100:
#             raise ValueError('invalid score')
#         self.__score = score
#
# s = Student('Bob', 59)
# print s.get_score()
# s.set_score(60)
# print s.get_score()
# #print s.set_score()  这是硬伤不能传参数


# class Student(object):
#
#     @property
#     def score(self):
#         return self._score
#
#     @score.setter
#     def score(self, value):
#         if not isinstance(value, int):
#             raise ValueError('score must be an integer!')
#         if value < 0 or value > 100:
#             raise ValueError('score must between 0 ~ 100!')
#         self._score = value
#
# s = Student()
# s.score = 60
# print s.score