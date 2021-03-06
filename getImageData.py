#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import fileObject

def deleteAnnoationCode(codeString):
    annoationList1 = re.compile('/\*[^(/\*|\*/)]+\*/').findall(codeString)
    for string in annoationList1:
        codeString = codeString.replace(string,'')
    annoationList2 = re.compile('//.*\n').findall(codeString)
    for string in annoationList2:
        codeString = codeString.replace(string,'')
    return codeString

path = os.getcwd() + "/.." #文件夹目录
os.chdir(path)
imageList = fileObject.getFile(path,['imageset'])
codePath = path
fileList = [codePath]
jointString = []
for filePath in fileList:
    files = os.listdir(filePath)
    for thisFile in files:
        if 'thirdparty' == thisFile:
            continue
        if thisFile.endswith('.m') or thisFile.endswith('.mm') or thisFile.endswith('.xib') or thisFile.endswith('.storyboard') or thisFile.endswith('.xml') or thisFile.endswith('.plist'):
            try :
                codeFile = open(filePath+'/'+thisFile,encoding='utf8')
            except IOError as e:
                print('tryError')
            else:
                try:
                    codeString = codeFile.read()
                except IOError as e:
                    print('tryopenFileError')
                else:
                    codeString = deleteAnnoationCode(codeString)
                    connectImage = re.compile('"[^"\n%:=]+%').findall(codeString)
                    jointString.extend(connectImage)
                    imageList = [thisImage for thisImage in imageList if ('"'+os.path.splitext(os.path.basename(thisImage))[0]+'"') not in codeString and not os.path.splitext(os.path.basename(thisImage))[0].startswith('{')]
                    codeFile.close()
    dirFileList = [filePath+'/'+thisFile for thisFile in files if os.path.isdir(filePath+'/'+thisFile) and not thisFile == 'Pods' and '.' not in thisFile]
    fileList.extend(dirFileList)
index = len(imageList) - 1
while (index >= 0):
    thisImage = imageList[index]
    thisImage = os.path.splitext(os.path.basename(thisImage))[0]
    for joint in jointString:
        string = joint[1:-1]
        if thisImage.startswith(string):
            imageList.pop(index)
            break
    index -= 1


for string in imageList:
    svnstring = 'rm -rf '
    svnstring = svnstring + '"' + string + '"'
    print(svnstring)
    os.system(svnstring)
