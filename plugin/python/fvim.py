#!/usr/bin/python
#coding:UTF-8
############################################################
##!  @brief	封装了vim基础功能
##!  
##!  功能包括行操作（删除、插入）、前缀操作（删除、添加）、光标位置、文件信息（路径、名称）等
##!  @file	fvim.py
##!  @path	prj/python/module
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
##!  @version	0.1.0
############################################################
import vim
import zsl


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
	if( 0 == lineRange[ 0 ] ):
		lineRange[ 0 ] = GetCurrentRow()
	if( 0 == lineRange[ 1 ] ):
		lineRange[ 1 ] = lineRange[ 0 ]
	buf = GetBuf( bufIndex )
	if( None == buf ):
		return None
	lineCnt = len( buf )
	if( lineRange[ 0 ] < 0 ):
		lineRange[ 0 ] += lineCnt
	if( lineRange[ 1 ] < 0 ):
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










