# 文件说明

## counter.py

统计当前目录下合法的ts的翻译情况,显示如:
```
当前版本从 1015个资源文件中抽取了 16697 行需要翻译的字符串
目前的ts文件还有 15756 个字符串没有被翻译
已经翻译了 941 行
完成度 0.0607893633586872%

```



使用方式:
```bash

python counter.py eric6_zh_CN.ts

```

如果想保存每一行可翻译字符串,到当前目录下的文件,可以加上一个`true`:
```bash
python counter.py eric6_zh_CN.ts true
```

##  messageParser.py

从合法的 ts 文件中,解析`message`,没有使用`lxml`包,使用了正则表达式,使用方法:
```bash
python messageParser.py fortest.ts
# 或者
python messageParser.py fortest.ts true
```

## eric6_zh_CN.ts

Eric 6 (19.04) 的简体中文语言包;

## eric6_zh_CN.qm

上面那个文件编译过后的文件,可以放在 Eric 6 安装目录下的`i18n`目录中,例如
```
D:\tools\eric6-19.04\eric\i18n
```

重启 Eric, 可见到效果。

