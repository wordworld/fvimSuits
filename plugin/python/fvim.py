#!/usr/bin/python
#coding:UTF-8
############################################################
##!  @brief	封装了vim基础功能
##!  
##!  功能包括行操作（删除、插入）、前缀操作（删除、添加）、光标位置、文件信息（路径、名称）等
##!  @file	fvim.py
##!  @path	prj/fvimSuits/plugin/python
##!  @author	fstone.zh@foxmail.com
##!  @date	2016-12-16
##!  @version	0.1.0
############################################################
import vim
import zsl
import os


# ####################### 增 #####################################

##!  @brief	插入文本（不作验证）
##!  
##!  
##!  @param	text 	要插入的文本
##!  @param	line 	插入的位置
##!  @param	buf 	文件buffer
##!  @return	成功
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def insertLine( text, line, buf ):
	buf.append( text, line - 1 )
	vim.current.window.cursor = ( line, len(text) )
	return True


##!  @brief	增加有效性验证的文本插入函数
##!  
##!  如果text为空（仅包含空格、Tab内容）则不进入插入操作
##!  @param	text 	待插入文本
##!  @param	line 	位置
##!  @param	buf 	文件
##!  @return	空文本返回False
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def insertTextLine( text, line, buf ):
	if ( not zsl.IsBlankLine(text)  ):
		return insertLine( text, line, buf )
	return False


##!  @brief	表格绘制类
##!  
##!  
class Table:
	'Table'
	def __init__( self ):
		self.LU = '┌'
		self.MU = '┬'
		self.RU = '┐'
		self.LM = '├'
		self.MM = '┼'
		self.RM = '┤'
		self.LD = '└'
		self.MD = '┴'
		self.RD = '┘'
		self.H	= '─'
		self.V	= '│'
		self.S	= ' '
	##!  @brief	绘制表
	##!  
	##!  
	##!  @param	self
	##!  @param	row	行数
	##!  @param	col	列数
	##!  @param	width	列宽
	##!  @param	height	行高
	##!  @param	line	插入到第几行
	##!  @param	bufIdx
	##!  @return	无
	##!  @date	2016-12-13
	def Draw( self, row, col, width, height, prefix="", line = 0, bufIdx = 0 ):
		if( 1 > row or 1 > col ):
			return False
		lineRange = [ line, line ]
		buf = ValidIndex(lineRange, bufIdx)
		if( None == buf ):
			return False
		line = lineRange[0]
		up	= prefix + self.LU + self.H * width	# 顶行
		mid	= prefix + self.LM + self.H * width	# 中行
		down	= prefix + self.LD + self.H * width	# 底行
		# 第 [2,n-1] 列
		if(1 < col):
			up	+= ( self.MU + self.H * width ) * (col-1)
			mid	+= ( self.MM + self.H * width ) * (col-1)
			down	+= ( self.MD + self.H * width ) * (col-1)
		# 第 n 列
		up	+= self.RU
		mid	+= self.RM
		down	+= self.RD
		# 内容行
		text	= prefix + self.V  + ( self.S * width + self.V ) * col
		# 绘制表头行
		insertTextLine( up,	line,	buf )
		line += 1
		# 绘制第一行内容
		k = 0
		while( k < height ):
			insertTextLine( text,	line,	buf )
			line += 1
			k += 1
		# 绘制若干间隔行和内容行
		if( 1 < row ):
			i = 0
			while(i < row-1):
				insertTextLine( mid,	line,	buf )
				line += 1
				k = 0
				while( k < height ):
					insertTextLine( text,	line,	buf )
					line += 1
					k += 1
				i += 1
		# 绘制末行
		insertTextLine( down, line, buf )

class Directory:
	'目录'
	def __init__( self ):
		self.forUncle	= '│   '
		self.forBro	= '├── '
		self.last	= '└── '
		self.empty	= '    '
	##!  @brief	绘制目录树状结构
	##!  
	##!  
	##!  @param	self
	##!  @param	dir	目录
	##!  @param	maxLevel最深层次，默认0递归
	##!  @param	prefix	前缀
	##!  @param	line
	##!  @param	bufIdx
	##!  @return	无
	##!  @date	2016-12-14
	def Draw(self, dir, maxLevel = 0, prefix = "", show_all=0, line=0, bufIdx=0):
		dirUncle = ""
		fileUncle = ""
		lineRange = [ line, line ]
		buf = ValidIndex(lineRange, bufIdx)
		if( None == buf ):
			return False
		line = lineRange[0]
		# 根目录
		startLine = line
		text = prefix + dir
		insertTextLine( text,	line,	buf )
		line += 1
		if(dir[-1] != "/"):
			dir += "/"
		# dir = os.path.abspath(dir)
		bRootDir = True
		# 迭代打印目录
		for root, dirs, files in os.walk(dir):
			# 目录层次，从0开始
			level = root.replace(dir, '').count(os.sep)
			curDir = os.path.split(root)[1]		# 目录
			if( (0 >= maxLevel or maxLevel > level) and (show_all !=0 or not '.' in root[1:]) ):
				dirUncle = self.forUncle * level
				if( not bRootDir ):
					text = prefix + dirUncle + self.forBro + curDir
					insertTextLine( text,	line,	buf )
					line += 1
					level+= 1

				if(0 >= maxLevel or maxLevel > level):	# 文件
					fileUncle = self.forUncle * (level)
					for f in files[1:]:
						text = prefix + fileUncle + self.forBro + f
						insertTextLine( text,	line,	buf )
						line += 1
					if( len(files) > 0 ):
						text = prefix + fileUncle + self.last + files[0]
						insertTextLine( text,	line,	buf )
						line += 1
			if(bRootDir):
				bRootDir = False
		self.EraseFakeUncle(startLine, line-1, buf)

	def EraseFakeUncle(self, startLine, endLine, buf, firstCall=True):
		if( startLine >= endLine ):
			return True
		lastLine = buf[ endLine-1 ]
		limit = len(lastLine)
		if(firstCall):
			lastLine = lastLine.replace( self.forUncle, self.empty )
			buf[endLine-1] = self.FindReplaceWith(lastLine, '├', self.last, self.forBro, "")
		
		text = buf[endLine-2]
		# 删除已经没有子目录/文件时的 │ 连接符
		text = self.FindReplaceWith(text, '│', self.empty, self.forUncle, lastLine)
		# 将最后一个目录/文件的 ├ 替换为 └
		text = self.FindReplaceWith(text, '├', self.last, self.forBro, lastLine)

		buf[ endLine-2 ] = text
		self.EraseFakeUncle( startLine, endLine-1, buf, False)
	##!  @brief	查找 pattern, 并将 pattern 处的 old 替换为 new 
	##!  
	##!  
	##!  @param	self
	##!  @param	text		字符串
	##!  @param	pattern		模式串
	##!  @param	new		新内容
	##!  @param	old		旧内容
	##!  @param	followLine	下一行内容
	##!  @return	无
	##!  @date	2016-12-16
	def FindReplaceWith(self, text, pattern, new, old, followLine):
		idx = -1
		limit = len(followLine)
		while( True ):
			idx = text.find(pattern, idx+1)
			if( 0 > idx ):
				break
			if( idx > limit or ( idx != followLine.find('│', idx) and idx != followLine.find('└', idx) and idx != followLine.find('├', idx) ) ):
				pretext = ""
				if( 0 < idx ):
					pretext = text[0:idx]
				text = pretext + text[idx:].replace(old, new, 1)
		return text
		





# ######################## 删 ####################################

def deleteLine( startLine, endLine, buf ):
	del buf[ startLine-1 : endLine ]

##!  @brief	删除指定范围内的行
##!  
##!  验证范围行的正确性
##!  @param	startLine 	起始行
##!  @param	endLine 	结束行，为0表示只删除开始行
##!  @param	bufIndex 	文件buffer索引，如果为0表示当前文件
##!  @return	删除成功
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ValidDeleteLine( startLine, endLine = 0, bufIndex = 0 ):
	buf = ValidIndex( startLine, endLine, bufIndex ) 
	if( None != buf ):
		deleteLine( startLine, endLine, buf )
		return True
	return False

##!  @brief	删除行文本前缀
##!  
##!  
##!  @param	prefix 	前缀文本
##!  @param	line 	行号
##!  @param	buf 	文件buffer
##!  @return	删除成功
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def deletePrefix( prefix, line, buf ):
	prefixLen = len( prefix )
	strLine = buf[ line -1 ]
	indent = zsl.LeftWhiteSpaceLen( strLine ) 
	#print "strLine[", indent, ":", indent , "+", prefixLen, "] =", strLine[ indent : indent + prefixLen ]
	if( prefix == strLine[ indent : indent + prefixLen ] ):
		setLineText( strLine[ 0 : indent ] + strLine[ indent + prefixLen : ], line, buf )
		return True
	return False

##!  @brief 	兼容地删除行文本前缀
##!  
##!  考虑前缀中包含空格和无空格的情形
##!  @param	prefix
##!  @param	line
##!  @param	buf
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def compatibleDeletePrefix( prefix, line, buf ):
	if( deletePrefix( prefix, line, buf ) ):
		return True
	compatible = prefix.strip()
	if( len( compatible ) < len ( prefix ) ):
		return deletePrefix( compatible, line, buf )
	return False

##!  @brief	删除带有prefix前缀的第num行
##!  
##!  
##!  @param	num 	行号
##!  @param	prefix 	前缀
##!  @return	成功
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def DeletePrefixedLine( num, prefix ):
	lineBuf = vim.current.buffer[num-1] 	# 行内容
	lineSize = len(lineBuf) 		# 行长度
	prefixLen = len(prefix) 		# 行前缀长度
	i = 0
	while( i + prefixLen  <= lineSize and (lineBuf[i] == ' ' or lineBuf[i] == '\t') ): # 过滤行首空格、Tab
		i += 1
	if( i + prefixLen <= lineSize  and  lineBuf.find(prefix, i) > -1 ): 	# 查找注释头 
		DeleteLines( num )
		return True
	return False

# ##################### 改  #######################################

##!  @brief	设置buf第line行,内容为text
##!  
##!  
##!  @param	text 	内容
##!  @param	line 	行号
##!  @param	buf 	文件buffer
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def setLineText( text, line, buf ):
	buf[ line-1 ] = text


##!  @brief	验证索引有效，然后设置buf第line行,内容为text
##!  
##!  
##!  @param	text 	内容
##!  @param	line 	行号
##!  @param	bufIndex 文件buffer索引
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ValidSetLineText( text, line, bufIndex = 0 ):
	buf = ValidIndex( line, line, bufIndex )
	if( None != buf ):
		buf[ line-1 ] = text

##!  @brief	向buf第line行, pos索引位置，插入text
##!  
##!  
##!  @param	text 	插入内容
##!  @param	pos 	在行中的位置( 0,1 ... )
##!  @param	line 	行号
##!  @param	buf 	文件buffer
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def insertText( text, pos, line, buf ):
	strLine = buf[ line-1 ]
	lineLength = len( strLine )
	pre = ""
	middle = ""
	last = ""
	if( 0 >= pos ):
		pre = text
		middle = strLine
	elif( 0 < pos  and pos < lineLength ):
		pre = strLine[ 0 : pos ]
		middle = text
		last = strLine[ pos : lineLength ]
	else: # pos >= lineLength, append
		pre = strLine
		middle = text
	setLineText( pre + middle + last, line, buf )

##!  @brief	验证索引有效，然后向buf的第line行, pos索引位置，插入text
##!  
##!  
##!  @param	text
##!  @param	pos
##!  @param	line
##!  @param	bufIndex 1,2,3 ...
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ValidInsertText( text, pos, line, bufIndex ):
	buf = ValidIndex( line, line, bufIndex )
	if( Nonebuf ):
		inserText( text, pos, line, buf )
		return True
	return False

##!  @brief	设置光标位置
##!  
##!  
##!  @param	x
##!  @param	y
##!  @param	winIndex(0,1,2 ...) 
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-12
def SetCursor( x, y, winIndex ):
	win = GetWindow( int(winIndex) )
	if( None == win ):
		return False
	row, col = win.cursor
	if( 0 <= x ):
		row = x
	if( 0 <= y ):
		col = y
	win.cursor = (row, col)
	return True
	


# ######################## 查 ####################################

##!  @brief	通过index获取buffer
##!  
##!  
##!  @param	bufIndex 有效取值是1,2, ... <=0时返回当前buffer
##!  @return	指定索引的bufer
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetBuf( bufIndex ):
	if( 0 >= bufIndex ):
		return vim.current.buffer
	elif( 0 < bufIndex  and  bufIndex <= len( vim.buffers ) ):
		return vim.buffers[ bufIndex ]
	print "error: invalid file buffer"
	return None

##!  @brief	通过索引获取窗口
##!  
##!  
##!  @param	winIndex 有效取值是0,1,2 ... 当 <0 时返回当前窗口
##!  @return	window对象
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetWindow( winIndex ):
	if( 0 >= winIndex ):
		return vim.current.window
	elif( 0 < winIndex  and winIndex <= len( vim.windows ) ):
		return vim.windows[ winIndex ]
	print "error: invalid window", winIndex
	return None

##!  @brief	获取当前光标位置
##!  
##!  
##!  @param	winIndex(0,1,2 ...) 默认是当前窗口索引
##!  @return	当前 行,列 位置
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetCursorPos( winIndex = 0 ):
	win = GetWindow( winIndex )
	if( None != win ):
		return win.cursor
	return 1,1

##!  @brief	获取当前行
##!  
##!  
##!  @return	行号
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetCurrentRow():
	row, col = GetCursorPos()
	return row

##!  @brief	获取当前列
##!  
##!  
##!  @return	列号
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetCurrentColumn():
	row, col = GetCursorPos()
	return col

##!  @brief	验证 是否 有效索引
##!  
##!  
##!  @param	lineRange 包含[ 起始行号，结束行号 ] 的列表
##!  @param	bufIndex 文件buffer索引
##!  @return	有效返回buffer对象，否则返回None
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ValidIndex( lineRange , bufIndex=0 ):
	buf = GetBuf( bufIndex )
	if( None == buf ):
		print "error: invalid buffer index:", bufIndex
		return None
	lineCnt = len( buf )
	if( 0 == lineRange[ 0 ] ):
		lineRange[ 0 ] = GetCurrentRow()
	if( 0 == lineRange[ 1 ] ):
		lineRange[ 1 ] = lineRange[ 0 ]
	if( lineCnt < lineRange[0] ):
		lineRange[0] = lineCnt
	if( lineCnt < lineRange[1] ):
		lineRange[1] = lineCnt
	while( 0 > lineRange[ 0 ] ):
		lineRange[ 0 ] += lineCnt
	while( 0 > lineRange[ 1 ] ):
		lineRange[ 1 ] += lineCnt
	if( lineRange[ 0 ] > lineRange[ 1 ] ):
		lineRange[ 0 ], lineRang[ 1 ] = lineRange[ 1 ], lineRang[ 0 ] 
	if( 0 >= lineRange[ 0 ]  or  lineRange[ 1 ] > lineCnt ):
		print "error: line number overflow", lineRange[0], lineRange[1]
		return None
	return buf

##!  @brief	行以prefix开始
##!  
##!  
##!  @param	prefix 	前缀
##!  @param	line 	行号
##!  @param	buf 	文件buffer
##!  @return	是/否
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def lineStartWith( prefix, line, buf ):
	return buf[ line-1 ].lstrip().startswith( prefix )

##!  @brief	行以postfix结束
##!  
##!  
##!  @param	postfix 后缀
##!  @param	line
##!  @param	buf
##!  @return	无
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-12
def lineEndWith( postfix, line, buf ):
	return buf[ line-1 ].rstrip().endswith( postfix )

##!  @brief	验证索引有效，然后判断行是否以prefix开头
##!  
##!  
##!  @param	prefix 	前缀
##!  @param	line 	行号
##!  @param	bufIndex 文件buffer索引
##!  @return	是/否
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def ValidLineStartWith( prefix, line, bufIndex ):
	buf = ValidIndex( line, line, bufIndex ) 
	if( None != buf ):
		return LineStartWith(prefix, line, buf )
	return False


##!  @brief	获取完整文件名（包含路径）
##!  
##!  
##!  @param	bufIndex =0时获取当前完整文件名
##!  @return	"/path/filename.ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetFullFileName( bufIndex = 0 ):
	fullFileName = ""
	buf = GetBuf( bufIndex )
	if( None != buf ):
		fullFileName = buf.name
	return fullFileName

##!  @brief	获取文件路径
##!  
##!  
##!  @param	bufIndex
##!  @return	"/path"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetFilePath( bufIndex = 0 ):
	return zsl.ParseFilePath( GetFullFileName( bufIndex ) )

##!  @brief	获取文件名
##!  
##!  
##!  @param	bufIndex
##!  @return	"filename.ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetFileName( bufIndex = 0 ):
	return zsl.ParseFileName( GetFullFileName( bufIndex ) )

##!  @brief	获取文件扩展名
##!  
##!  
##!  @param	bufIndex
##!  @return	".ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetFileExtension( bufIndex = 0 ):
	return zsl.ParseFileExtension( GetFullFileName( bufIndex ) )

##!  @brief	获取文件路径、文件名（无扩展名）、扩展名
##!  
##!  
##!  @param	bufIndex
##!  @return	"/path" "filename" ".ext"
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def GetFileDescription( bufIndex = 0 ):
	return zsl.ParseFileDescription( GetFullFileName( bufIndex ) )


##!  @brief	判断光标位于文件头（前10行）
##!  
##!  
##!  @param	line 	光标所在行
##!  @param	buf 	文件buffer
##!  @return	光标位于文件头部
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
def atFileTop( line, buf ):
	return line in range(1, 11) # 注释掉此行，则以是否是第一个非空行 判断 光标在文件头.当前认为1-10行为文件头
	line -= 1
	while( 0 < line ):
		if( not zsl.IsBlankLine( buf[ line - 1 ] ) ):
			return False
		line -= 1
	return True


