import os
import sys  # 反射
import pickle  # 存对象


class Course:
    def __init__(self, name, price, period, teacher):
        self.name = name
        self.price = price
        self.period = period
        self.teacher = teacher

class Person:
    def show_courses(self):
        with open('course_info', 'rb', ) as f:
            count = 0
            while True:
                try:
                    count += 1
                    course_obj = pickle.load(f)
                    print(count, course_obj.name,
                          course_obj.price,
                          course_obj.period,
                          course_obj.teacher)
                except EOFError:
                    break
class Student(Person):
    operate_lst = [
        ('查看所有课程', 'show_courses'),
        ('选择课程', 'select_course'),
        ('查看已选课程', 'check_selected_course'),
        ('退出', 'exit')
    ]

    def __init__(self, name):
        self.name = name
        self.courses = []

    # def show_courses(self):
    #
    #     print('查看可选课程')

    def select_course(self):
        self.show_courses()
        num = int(input('num>>>'))
        count = 1
        with open('course_info','rb') as f:
            while True:
                try:
                    course_obj = pickle.load(f)
                    if count == num:
                        self.courses.append(course_obj)
                        print('您选择了{}课程'.format(course_obj.name))
                        break
                    count += 1
                except EOFError:
                    print('没有您选择的课程')
                    break
        # print('选择课程')

    def check_selected_course(self):
        # print('查看已选课程')
        for course in self.courses:
            print(course.name,course.teacher)

    def exit(self):
        with open('student_info','rb') as f1,open('student_info_bak','wb') as f2:
            while True:
                try:
                    student_obj = pickle.load(f1)
                    # 如果从原文件找到了学生对象和我当前的对象是一个名字，就认为是一个人
                    if student_obj.name == self.name:
                        # 应该把现在新的学生对象写到文件中
                        pickle.dump(self,f2)
                    else:
                        # 反之，应该原封不动的把学生对象写回f2
                        pickle.dump(student_obj,f2)
                except EOFError:
                    break
        os.remove('student_info')
        os.rename('student_info_bak','student_info')
        exit()

    @staticmethod
    def init(name):
        # 返回一个学生的对象就行
        # 学生对象在 student_info 文件中
        # 找到符合的对象之后，直接将load 出来的对象返回
        with open('student_info', 'rb') as f:
            while True:
                try:
                    stu_obj = pickle.load(f)
                    if stu_obj.name == name:
                        return stu_obj
                except EOFError:
                    print('没有这个学生')
                    break


class Manager(Person):
    operate_lst = [('创建课程', 'create_course'),
                   ('创建学生', 'create_student'),
                   ('查看所有课程', 'show_courses'),
                   ('查看所有学生', 'show_students'),
                   ('查看所有学生的选课情况', 'show_student_course'),
                   ('退出', 'exit')]

    def __init__(self, name):
        self.name = name
        # self.course = []

    def create_course(self):
        name = input('course name :')
        price = input('course price :')
        period = input('course period')
        teacher = input('course teacher :')
        course_obj = Course(name, price, period, teacher)
        with open('course_info', 'ab') as f:
            pickle.dump(course_obj, f)
        print('{}课程创建成功'.format(course_obj.name))

    def create_student(self):
        # print('创建学生')
        # 用户名和密码记录到 userinfo文件，将学生对象存储在 student_info 文件
        stu_name = input('student name :')
        stu_pwd = input('student password :')
        stu_auth = '{}|{}|Student\n'.format(stu_name, stu_pwd)  # 添加一个学生信息到 userinfo 文件
        stu_obj = Student(stu_name)  # 实例化学生
        with open('userinfo', 'a', encoding='utf-8') as f:
            f.write(stu_auth)
        with open('student_info', 'ab') as f:
            pickle.dump(stu_obj, f)
        print('{}学生创建成功'.format(stu_obj.name))

    def show_courses(self):
        with open('course_info', 'rb', ) as f:
            count = 0
            while True:
                try:
                    count += 1
                    course_obj = pickle.load(f)
                    print(count, course_obj.name,
                          course_obj.price,
                          course_obj.period,
                          course_obj.teacher)
                except EOFError:
                    break

    def show_students(self):
        with open('student_info', 'rb') as f:
            count = 0
            while True:
                try:
                    count += 1
                    student_obj = pickle.load(f)
                    print(count, student_obj.name)
                except EOFError:
                    break
        # print('查看所有学生')

    def show_student_course(self):
        with open('student_info','rb') as f:
            while True:
                try:
                    student_obj = pickle.load(f)
                    course_name = [course.name for course in student_obj.courses]
                    # print(student_obj.name,'所选课程{}'.format('|'.join(course_name )))
                    print(student_obj.name,'所选课程%s'%'|'.join(course_name ))
                except EOFError:
                    break
        # print('查看所有学生的选课情况')

    def exit(self):
        exit()

    @classmethod
    def init(cls, name):
        return cls(name)  # 管理员的对象


# 学生：登陆就可以选课了
# 有学生账号了
# 有课程了

# 管理员：
# 学生的账号是管理员创建的
# 课程也是管理员创建的

# 应该先站在管理员的角度上开发
# 登陆
# 登陆必须能够自动识别身份
# 用户名|密码|身份
def login():
    name = input('username :')
    pawd = input('passwword :')
    with open('userinfo', encoding='utf-8') as  f:
        for line in f:
            usr, pwd, identify = line.strip().split('|')
            if usr == name and pawd == pwd:
                return {'result': True, 'name': name, 'id': identify}
        else:
            return {'result': False, 'name': name}


ret = login()
if ret['result']:
    print('登陆成功')
    if hasattr(sys.modules[__name__], ret['id']):
        cls = getattr(sys.modules[__name__], ret['id'])
        obj = cls.init(ret['name'])
        # obj = cls(ret['name'])  # 实例化
        while True:
            for id, item in enumerate(cls.operate_lst, 1):
                print(id, item[0])
            func_str = cls.operate_lst[int(input('>>>')) - 1][1]
            if hasattr(obj, func_str):
                getattr(obj, func_str)()
else:
    print('登陆失败')

    # if ret['id'] == 'Manager':
    #     obj = Manager(ret['name'])
    #     for id, item in enumerate(Manager.operate_lst, 1):
    #         print(id, item[0])
    #     func_str = Manager.operate_lst[int(input('>>>')) - 1][1]
    #     if hasattr(obj, func_str):
    #         getattr(obj, func_str)()
    #
    # elif ret['id'] == 'Student':
    #     obj = Student(ret['name'])
    #     for id, item in enumerate(Student.operate_lst, 1):
    #         print(id, item[0])
    #     func_str = Student.operate_lst[int(input('>>>')) - 1][1]
    #     if hasattr(obj, func_str):
    #         getattr(obj, func_str)()
