# eric-ide-zh_CN


[Eric-IDE](https://sourceforge.net/projects/eric-ide/files/eric6/stable/) 是使用 Python 基于 PyQt5 写成的免费开源的,写 GUI 程序比较好用的 IDE。

本项目维护其简体中文翻译包。




## ts 和 qm 是什么

都是 Qt 的国际化/本地化(i18n)文件, ts 是可编辑的文件, qm 是编译后的文件格式。

ts 采用的是类 xml 的语法的文件;
qm 是二进制的文件;



## ts=>qm
使用 lconvert:
```bash
# run the following command to find lconvert
where lconvert
# or as following on Linux:
whereis lconvert

# if found it, run
lconvert  eric6_zh_CN.ts -o eric6_zh_CN.qm

# may need to copy it to eric i18n dirctory

cp D:\tools\python36\Lib\site-packages\eric6\i18n\eric-ide-zh_CN\v6\eric6_zh_CN.qm D:\tools\python36\Lib\site-packages\eric6\i18n

```




## Eric 6
19.04版本,含有从 1015个资源文件中抽取了 16697 行需要翻译的字符串;
简体中文版,我翻译了一百多行常用的,后续将会写一个GUI程序,以实现自动翻译。



## 备忘
Eric 装在下面的位置:
```
D:\tools\python36\Lib\site-packages\eric6\i18n

```
项目 tsTranslator 的位置在：
```

Y:\pyqt\tsTranslaTor

```
