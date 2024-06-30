# MBPC
更好的 Python 类。

## 快速开始
在 MBPC 中定义类时，需要使用 `classdef` 函数。
下面是一个简单的例子：
```
from mbpc.classdef import classdef

@classdef()
def Person(self, name: str, age: int):
    self.super.initialize()
    self.name = name
    self.age = age

    @self.method
    def printInfo():
        print(self.name, self.age)
```
**注意：**
- MBPC 类的第一个参数必须为 `self`
- MBPC 类的构造函数第一行必须为 `self.super.initialize(...)`
- 定义方法时，需要使用 `self.method` 函数

## MBPC 类的继承
在 MBPC 中实现类的继承时，只需将父类写在 `classdef` 函数的括号中。
下面是一个简单的例子：

```
from mbpc.classdef import classdef

@classdef()
def Person(self, name: str, age: int):
    self.super.initialize()
    self.name = name
    self.age = age

    @self.method
    def printInfo():
        print(self.name, self.age)

@classdef(Person)
def Student(self, name: str, age: int, school: str):
    self.super.initialize(name, age)
    self.school = school

    @self.method
    def printInfo():
        print(self.name, self.age, self.school)
```
**注意：**
- MBPC 类不支持多继承
- `classdef` 中没有参数时，默认继承 `Base` 类 

## 静态方法
利用 MBPC 类的 `method` 函数可以实现静态方法。
下面是一个简单的例子：

```
from mbpc.classdef import classdef

@classdef()
def Person(self): ...

Person.count = 0

@Person.method
def increase(by: int):
    Person.count += by

Person.initialize()
```
**注意：**
- 在书写完静态方法后，需要调用 `initialize` 方法，帮助 MBPC 完成对类的一些必要检查

## 接口
在 MBPC 中，可以通过 `interfacedef` 函数定义接口。
下面是一个简单的例子：
```
from mbpc.interfacedef import interfacedef

@interfacedef()
def Named(interface):
    @interface.method
    def changeName(newName: str): ...

@Named.method
def increase(ny: int): ... # 对静态方法的声明
```
**注意：**
- MBPC 接口的第一个参数必须为 `interface`
- 定义方法时，需要使用 `interface.method` 函数
- 定义静态方法时，需要使用接口的 `method` 函数

在实现接口时，方法名、参数名称、参数类型、参数个数、返回值类型必须和接口声明的一致，
否则将触发 `InterfaceException`。
可以在 `classdef` 函数中指定需要实现的接口，可以同时实现多个接口。
```
from mbpc.classdef import classdef

@classdef(Named)
def Person(self, name: str, age: int):
    self.super.initialize()
    self.name = name
    self.age = age

    @self.method
    def printInfo():
        print(self.name, self.age)

    @self.method
    def changeName(newName: str):
        self.name = newName

Person.count = 0

@Person.method
def increase(by: int):
    Person.count += by

Person.initialize()
```
此外，接口也可以继承，子接口将继承父接口的全部声明。
可以在 `interfacedef` 函数中声明父接口，支持多继承。
```
from mbpc.interfacedef import interfacedef

@interfacedef()
def Interface1(interface):
    @interface.method
    def func1(): ...

@interfacedef()
def Interface2(interface):
    @interface.method
    def func2(): ...

@interfacedef(Interface1, Interface2)
def Interface3(interface):
    @interface.method
    def func3(): ... 
    
# 此时实现 Interface3 的类需要同时实现 func1、func2 及 func3
```
