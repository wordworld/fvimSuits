#!/usr/bin/python
#coding:UTF-8
############################################################
##!  @brief	通用程序
##!  
##!  
##!  @file	zsl.py
##!  @path	prj/python/module
##!  @author	Fstone's ComMent Tool
##!  @date	2016-10-27
##!  @update 	更新 ParseFileExtension以支持 .name name 这样的文件
##!  @version	0.1.1
############################################################


# ###################### 文件路径字符串相关 ######################################

##!  @brief	从完整文件名 解析 路径
##!  
##!  
##!  @param	fullFileName "/path/filename.ext"
##!  @return	"/path"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ParseFilePath( fullFileName ):
	import os.path
	head, tail = os.path.split( fullFileName )
	return head

##!  @brief	从完整文件名 解析 文件名
##!  
##!  
##!  @param	fullFileName
##!  @return	"filename.ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ParseFileName( fullFileName ):
	import os.path
	head, tail = os.path.split( fullFileName )
	return tail

##!  @brief	从完整文件名 解析 扩展名
##!  
##!  
##!  @param	fullFileName
##!  @return	".ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ParseFileExtension( fullFileName ):
	import os.path
	fileName=ParseFileName(fullFileName)
	root, ext = os.path.splitext( fileName )
	if( not cmp(ext, "" ) ):
		if( len(root) > 0 and root[0] == '.' ):
			ext=root
			root=""
	return ext

##!  @brief	分隔完整文件名为 路径，文件名，扩展名
##!  
##!  
##!  @param	fullFileName
##!  @return	"/path" "filename" ".ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ParseFileDescription( fullFileName ):
	import os.path
	filePath, fileName = os.path.split( fullFileName )
	fileName, extension = os.path.splitext( fileName )
	return filePath, fileName, extension

##!  @brief	获取用户目录绝对路径
##!  
##!  
##!  @return	返回$HOME绝对路径字符串
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetHomeDir():
	import os.path
	return os.path.expanduser("~")


# ######################### 字符串处理相关 ###################################

##!  @brief	左侧空白长度
##!  
##!  
##!  @param	text 	行内容
##!  @return	是/否
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def LeftWhiteSpaceLen( text ):
	return len(text) - len( text.lstrip() )

##!  @brief	获取左侧空白字符串
##!  
##!  
##!  @param	text
##!  @return	左侧空白字符串
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def LeftWhiteSpace( text ):
	return text[ 0 : LeftWhiteSpaceLen( text ) ]

##!  @brief	是否空行
##!  
##!  
##!  @param	strLine 行内容
##!  @return	是/否
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def IsBlankLine( strLine ):
	return 0 == len( strLine.strip() )

# 正则表达式字符串预处理
def RegCompile( pattern, flags = 0 ):
	import re
	return re.compile( pattern.replace( ' ', '' ).replace( '\t', '' ), flags )


