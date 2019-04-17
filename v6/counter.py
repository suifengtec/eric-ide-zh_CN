# -*- coding: utf-8 -*-
# @Author: suifengtec
# @Date:   2019-04-17 17:51:45
# @Last Modified by:    suifengtec
# @Last Modified time: 2019-04-18 00:57:03
'''

parse eric i18n file.



'''
from os import (getcwd, access, R_OK)
from os.path import (isfile, join)
import regex
from sys import argv
from sys import exit


class ParseEric6I18nFile:
    def __init__(self, fileName):

        self.theFiles = []
        self.translationLines = []
        self.linesNeedToBeTranslated = []

        filePath = join(getcwd(), fileName)
        if self.isFileReadable(filePath):
            self.fileName = filePath
        else:
            self.fileName = None
            print("未找到文件！！")

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

    def getTranslationStrSrc(self, theLineContent):
        try:
            reg = r'.*<source>(.*?)<.*'
            p = regex.compile(reg)
            ret = p.match(theLineContent)
            return ret.groups(0)[0]
        except:
            return -1

    def isStrInSlice(self, matchFilePath):

        return matchFilePath in self.theFiles

    def read(self, shouldOutPutToFile):

        if self.fileName is None:
            print("文件名为空?")
            return

        try:
            with open(self.fileName, "r", encoding="utf-8") as fp:
                line = fp.readline()
                cnt = 1
                while line:
                    theLineContent = line.strip()
                    if self.isStrContain(theLineContent, "filename="):
                        matchFilePath = self.getFileNameByStr(theLineContent)
                        if matchFilePath != -1 and self.isStrInSlice(matchFilePath) != True:
                            self.theFiles.append(matchFilePath)
                    elif self.isStrContain(theLineContent, "</source>") == True:
                        strSrc = self.getTranslationStrSrc(theLineContent)
                        if strSrc != -1:
                            self.translationLines.append(strSrc)

                    elif self.isStrContain(theLineContent, 'type="unfinished"') == True:
                        self.linesNeedToBeTranslated.append(theLineContent)
                        # print("Line {}: {}".format(cnt, theLineContent))
                    line = fp.readline()
                    cnt += 1

                if shouldOutPutToFile:
                    self.writeToFile(self.theFiles, "fromFiles.txt")
                    self.writeToFile(self.translationLines,
                                     "needTranslateStrs.txt")

                countAllLines = len(self.translationLines)
                countAllNeedToBeTranslated = len(self.linesNeedToBeTranslated)
                contAllTranslated = countAllLines-countAllNeedToBeTranslated
                print("当前版本从 {0}个资源文件中抽取了 {1} 行需要翻译的字符串\n目前的ts文件还有"
                      " {2} 个字符串没有被翻译\n已经翻译了 {3} 行\n完成度 {4}%。".format(
                          len(self.theFiles),
                          countAllLines,
                          countAllNeedToBeTranslated,
                          contAllTranslated,
                          contAllTranslated/countAllLines))
        finally:
            fp.close()

    def writeToFile(self, content, fileName):
        try:
            filePath = join(getcwd(), fileName)
            with open(filePath, "w", encoding="utf-8") as fp:
                if isinstance(content, list):
                    #contentInStr = "\n".join(content)
                    # fp.write(contentInStr)
                    fp.writelines(content)
                elif isinstance(content, list):
                    fp.write(content)
            return True
        except Exception as err:
            print("Error:", err)
            return False


'''

python counter.py eric6_zh_CN.ts

# save strings need to be translated to file named needTranslateStrs.txt;
# save file names to named fromFiles.txt;


python counter.py eric6_zh_CN.ts true

'''


def main():
    try:
        if len(argv) < 2:
            print("Usage:\npython counter.py eric6_zh_CN.ts\nor as following:\npython counter.py eric6_zh_CN.ts true")
            exit(1)
        args = argv[1:]
        i18nFile = args[0]
        shouldOutPutToFile = False
        if len(args) > 1 and args[1] == "true":
            shouldOutPutToFile = True
        h = ParseEric6I18nFile(i18nFile)
        h.read(shouldOutPutToFile)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
