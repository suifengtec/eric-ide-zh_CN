# -*- coding: utf-8 -*-
# @Author: suifengtec
# @Date:   2019-04-18 01:54:16
# @Last Modified by:    suifengtec
# @Last Modified time: 2019-04-18 03:43:40
from os import (getcwd, access, R_OK)
from os.path import (isfile, join)
import regex
from sys import argv
from sys import exit

'''parse messages in a ts file to list.

解析message为

["也许是个注释","tab after keyword","",StrSrc的行号,StrTranslated的行号,当前是否被翻译]

格式为
[
self.msgComment,
self.msgStrSrc,
self.msgStrTranslated,
self.msgLineOfStrSrc,
self.msgLineOfStrTranslated,
self.isMsgTranslated
]

上面的格式是下面提到的listMessages的元素格式;


具体步骤

1. 打开文件,解析message(注释,原文,译文,是否被翻译),并记录message到self.listMsgs,
在循环每一行的同时,把每一行都记录在self.listAllLines;
3. 把 self.listMsgs 提供给 QTableWidget 显示,并记录使用者的更改;
4. 当保存文件时, 循环self.listMsgs,把相应的翻译过的内容,写入到对应的行。

[
self.msgComment,
self.msgStrSrc,
self.msgStrTranslated,
self.msgLineOfStrSrc,
self.msgLineOfStrTranslated,
self.isMsgTranslated
]

'''


class MsgParser:
    def __init__(self, fileName):

        filePath = join(getcwd(), fileName)
        if self.isFileReadable(filePath):
            self.fileName = filePath
        else:
            self.fileName = None
            print("未找到文件！！")
            exit(1)
        self.theFiles = []
        self.translationLines = []
        self.linesNeedToBeTranslated = []

        # message 的各个部分
        self.msgLocation = ""
        self.msgComment = ""
        self.msgStrSrc = ""
        self.msgStrTranslated = ""
        self.isMsgTranslated = False

        self.msgLineOfStrSrc = 0
        self.msgLineOfStrTranslated = 0
        # 所有行
        self.listAllLines = []
        # listMsgs
        self.listMsgs = []

    def isFileReadable(self, fileName):
        try:
            if isfile(fileName) and access(fileName, R_OK):
                return True
            return False
        except:
            return False

    def isStrContain(self, s, t):

        if s is None or len(s) == 0:
            return False
        return str.find(s, t) != -1

    def getFileNameByStr(self, theLineContent):
        try:
            theFileName = ""
            reg = r'.*filename="(.*?)"'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            return ret.groups(0)[0]
        except:
            return -1

    def isMessageStart(self, theLineContent):
        try:
            reg = r'.*<message>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            print(ret.groups(0)[0])
            return True
        except:
            return False

    def isMessageEnd(self, theLineContent):
        try:
            reg = r'.*</message>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            print(ret.groups(0)[0])
            return True
        except:
            return False

    def isStrInSlice(self, matchFilePath):
        return matchFilePath in self.theFiles

    def getStrSrc(self, theLineContent):
        try:
            reg = r'.*<source>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            return ret.groups(0)[0]
        except:
            return -1

    def getStrNeedToBeTranslated(self, theLineContent):
        try:
            # reg = r'.*type="unfinished">(.*?)<.*'
            reg = r'.*<message+\s*>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            print(ret.groups(0)[0])
            return ret.groups(0)[0]
        except:
            return -1

    def getComment(self, theLineContent):
        try:
            reg = r'.*<comment>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            # print(ret.groups(0)[0])
            return ret.groups(0)[0]
        except:
            return -1

    def getMsgs(self, shouldReturnMsgs=False):

        if self.fileName is None:
            print("文件名为空?")
            return False
        try:
            with open(self.fileName, "r", encoding="utf-8") as fp:
                line = fp.readline()
                idx = 1
                while line:
                    theLineContent = line.strip()
                    if self.isStrContain(theLineContent, "filename="):
                        self.msgLocation = theLineContent
                    elif self.isStrContain(theLineContent, "</source>") == True:
                        strSrc = self.getStrSrc(theLineContent)
                        if strSrc != -1:
                            self.msgStrSrc = strSrc
                            self.msgLineOfStrSrc = idx-1
                    elif self.isStrContain(theLineContent, "<comment>"):
                        cmt = self.getComment(theLineContent)
                        if cmt != -1:
                            self.msgComment = cmt
                    elif self.isStrContain(theLineContent, '<translation>') == True:

                        self.msgLineOfStrTranslated = idx-1
                        if self.isStrContain(theLineContent, "type"):
                            self.isMsgTranslated = True
                        else:
                            self.isMsgTranslated = False
                        theLineContent = theLineContent.replace(
                            '<translation>', '')
                        theLineContent = theLineContent.replace(
                            '</translation>', '')
                        theLineContent = theLineContent.replace(
                            '<translation type="unfinished">',  '')
                        self.msgStrTranslated = theLineContent

                    if self.isStrContain(theLineContent, "</message>"):
                        self.listMsgs.append(
                            [self.msgComment, self.msgStrSrc,
                             self.msgStrTranslated, self.msgLineOfStrSrc,
                             self.msgLineOfStrTranslated, self.isMsgTranslated, self.msgLocation])

                    self.listAllLines.append(theLineContent)
                    line = fp.readline()
                    idx += 1

                fp.close()
                if shouldReturnMsgs != None and shouldReturnMsgs == True:
                    return self.listMsgs
                else:
                    return True
        except:
            if fp != None:
                fp.close()
            return False

    def reloadContent(self):
        if len(self.listMsgs) > 0:
            '''
            strSrc = <source></source>
            msg[1]
            所在行号为 msg[3]

            strTranslated = <translation></translation>
            msg[2]
            所在行号为
            msg[4]

            是否已翻译,由 msg[5] 维护

            ===========
            else:
                    self.listAllLines[msg[4]] = '<translation type="unfinished">'+msg[2]+\
                    '</translation>'
            '''
            for msg in self.listMsgs:
                if msg[4] == True:
                    self.listAllLines[msg[4]] = '<translation>'+msg[2] +\
                        '</translation>'

    def fire(self, shouldOutPutToFile):
        '''

        模拟修改

            self.listMsgs[0][2] = "卧槽啊"

            self.listMsgs[0][2] = "卧槽啊"

        self.listAllLines[7] = "<translation>" + \
            self.listMsgs[0][2]+"</translation>"

        '''
        self.getMsgs()

        print(self.listMsgs)
        print("================================================================")
        print(self.listAllLines)

        # for line in self.listAllLines
        if shouldOutPutToFile:
            self.writeMassagesToFile(self.listAllLines, "messages.txt")

    def writeMassagesToFile(self, content, fileName):
        try:
            filePath = join(getcwd(), fileName)
            with open(filePath, "w", encoding="utf-8") as fp:
                if isinstance(content, list):
                    contentInStr = "\n".join(content)
                    fp.write(contentInStr)
                    # fp.writelines(content)
                elif isinstance(content, list):
                    fp.write(content)
            return True
        except Exception as err:
            print("Error:", err)
            return False


def main():
    try:
        if len(argv) < 2:
            print("Usage:\npython messageParser.py "
                  "fortest.ts\nor as following:\npython messageParser.py fortest.ts true")
            exit(1)
        args = argv[1:]
        i18nFile = args[0]
        shouldOutPutToFile = False
        if len(args) > 1 and args[1] == "true":
            shouldOutPutToFile = True
        h = MsgParser(i18nFile)
        h.fire(shouldOutPutToFile)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

'''使用


python messageParser.py fortest.ts
python messageParser.py fortest.ts true



'''
