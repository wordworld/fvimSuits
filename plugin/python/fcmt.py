#!/usr/bin/python
#coding:UTF-8
############################################################
##!  @brief	fcmt工具的主要逻辑 
##!    
##!    包含类Tag Lang{ Text: Cplus Shell Python Lua VimL }。实现向以上语言的代码文件插入自动化注释（行、文件头、函数、类等）功能
##!  @file	fcmt.py
##!  @path	prj/python/module
##!  @author	Fstone's ComMent Tool
##!  @date	2016-09-09
##!  @version	0.1.0
############################################################

import zsl
import fvim
import datetime
import re

# 定制内容
tag_author = "fstone.zh@foxmail.com" 		# 作者
UsrDecoratorCount 	= 60 			# 注释装饰符号数量，用于产生文件头的装饰框

# 标签
BRIEF 	= "brief"		
DETAIL 	= "detail"
PARAM 	= "param"
RETURN 	= "return"

PATH 	= "path"
FILE 	= "file"
AUTHOR 	= "author"
DATE 	= "date"
VERSION = "version"

ATTENTION = "attention"
NOTE 	= "note"
BUG 	= "bug"
INPUT 	= "input"
OUTPUT 	= "output"


##!  @brief	可选的标签
##!  
##!  键: 与定制内容一致 	# 值: 可自定义
class Tag:
	'标签'
	name 	= { BRIEF	: "@brief\t", 		DETAIL 	: "", 
		    PARAM	: "@param\t", 		RETURN 	: "@return\t",
		    PATH 	: "@path\t", 		FILE 	: "@file\t",
		    AUTHOR 	: "@author\t", 		DATE 	: "@date\t",
		    VERSION 	: "@version\t", 	NOTE 	: "@note\t",
		    ATTENTION 	: "@attention\t", 	BUG 	: "@bug\t",
		    INPUT 	: "@input\t", 		OUTPUT 	: "@output\t",
		}

	value 	= { BRIEF	: "", 			DETAIL 	: "", 
		    PARAM	: "", 		    	RETURN 	: "无",
		    PATH 	: "",		    	FILE 	: "",
		    AUTHOR 	: tag_author, 		DATE 	: datetime.date.today(),
		    VERSION 	: "0.1.0", 		NOTE 	: "",
		    ATTENTION 	: "", 			BUG 	: "",
		    INPUT 	: "", 			OUTPUT 	: "",
		}

	def __init__( self ):
		pass

	# 初始化
	@staticmethod
	def Update( buf ):
		import os.path
		if( None != buf ):
			Tag.value[ FILE ] = zsl.ParseFileName( buf.name )
			Tag.value[ PATH ] = zsl.ParseFilePath( buf.name )[ len(zsl.GetHomeDir()+"/"): ]
		Tag.value[ DATE ] = datetime.date.today()


##!  @brief	支持的编程语言
##!  
##!  
class Lang:
	'编程语言'
	TEXT 	= "text"
	CPLUS 	= "cplus" 	# // 		/* 	*/
	SHELL 	= "shell" 	# #
	PYTHON 	= "python" 	# # 		''' 	''' 		""" 	"""
	LUA 	= "lua" 	# -- 		--[[ 	 ]] 		--[====[ 	 ]====]
	VIML 	= "vimL" 	# "
	def __init__( self ):
		pass

	##!  @brief	Text类
	##!  
	##!  
	class Text:
		'普通文本'
		# 已选的标签
		tag_file 	= [ BRIEF, DETAIL, DETAIL, FILE, PATH, AUTHOR, DATE, VERSION ]
		tag_class 	= [ BRIEF, DETAIL, DETAIL ]
		tag_function 	= [ BRIEF, DETAIL, DETAIL, PARAM, RETURN ]
		# 标识符      _/字母    字母/数字
		reId 	= r"(?: [a-zA-Z_] [a-zA-Z_0-9]* )"
		# 命名空间                top           ::       [          sub           ::   ]
		reScope = r"(?:" 	+ reId + r"\s* \:\:" + r"(?: \s*" + reId + r"\s* \:\: )* )"
		# 下标
		reSub 	= r"(?: \s* | \s* \[ \s* \d* \s* \] ) " #r"\[ \s* \d* \s* \]"
		# 类型                [auto static ]         [top::sub::]        int           [* *&]           [const]
		reType 	= r"(?: (?:"+ reId + r"\s+ )* (?:" + reScope + "\s*)?" + reId + r"(?: \s* [\*\&] )* (?: \s*" + reId + r" )? )"
		# 声明             类型       空白   标识符   or   类型               * *&         标识符 
		reDecl 	= r"(?: (?:" + reType + r"\s+" + reId + r"|" + reType + r"(?: \s* [\*\&] )+" + reId + r" ) \s*" + reSub + r"*)"
		# 赋值
		reAss 	= r"(?: \= \s* (?: [\"\'].*[\"\'] | \w*  )  )"
		# 定义
		reDef 	= r"(?:" + reDecl + r"\s*" + reAss + ")"
		# 声明/定义
		reDD 	= r"(?:" + reDecl + r"(?: \s*" + reAss + ")? )"
		# 参数
		rePara 	=  r"(?: \s* ( " + reId + r" | \.\.\.) \s*" + reSub + "\s* (?= [\,\=\)])  )"
		
		# 函数格式
		objFunc 	= zsl.RegCompile( r"\s*" + reType + r"?\s+" + reScope + "? \s*" + reId  + r"\s* \( "
				+ r"(?: \s* | \s* \.\.\. \s* |  \s*" + reDD + r"(?: \s* , \s*" + reDD + r" )* (?: \s*, \s* \.\.\. \s*)? )"
						+ r"\s*\)" )
		# 参数查找模式
		objPara 	= zsl.RegCompile( rePara, re.I )
		# 类格式
		objClass 	= zsl.RegCompile( r"\s*class \s+(" + reId +")" )

		def __init__( self ):
			self.name 	= Lang.TEXT
			self.syntax 	= [ ".txt", ]
			self.line 	= "§ " # 行注释
			self.start 	= "┌"  # 块注释：起始行
			self.middle 	= "│ " # 	 中间行
			self.end 	= "┘"  # 	 结束行
			self.decorator 	= "─"  # 装饰符
			self.tStart 	= "[ " # 行尾注释：起始符号
			self.tEnd 	= " ]" # 行尾注释：结束符号
			

		def Print( self ):
			print self.name

		# 光标位于 函数名所在行 或 上一行
		def atFunction( self, line, buf ):
			return self.objFunc.match( buf[ line-1 ] )

		# 光标位于 类名所在行 或 上一行
		def atClass( self, line, buf ):
			return self.objClass.match( buf[ line-1 ] )

		##!  @brief	获取参数列表
		##!  
		##!  
		##!  @param	self
		##!  @param	line
		##!  @param	buf
		##!  @return	无
		##!  @author	Fstone's ComMent Tool
		##!  @date	2016-09-12
		def GetParameters( self, line, buf ):
			return self.objPara.findall( buf[ line - 1 ] )


		# 注释分隔线
		def AnnotateSeparator( self, line, buf ):
			ident = zsl.LeftWhiteSpace( buf[ line - 1 ] )
			strSep = self.line + self.decorator * UsrDecoratorCount
			endLine = len( buf )
			while( line <= endLine  and  zsl.IsBlankLine( buf[ line - 1 ] ) ):
				line += 1
			if( line > endLine ):
				return
			if( cmp(  buf[ line - 1 ].strip(),  strSep ) ):
				fvim.insertTextLine( ident + strSep, line, buf )
			else:
				fvim.deleteLine( line, line, buf )
			print zsl.GetHomeDir()

		# 注释文件头
		def AnnotateFile( self, line, buf ):
			Tag.Update( buf )
			ident = zsl.LeftWhiteSpace( buf[ line - 1 ] )
			# 首行
			if( fvim.insertTextLine( ident + self.start + self.decorator * UsrDecoratorCount, line, buf ) ):
				line += 1
			# 中间行
			for key in self.tag_file:
				if( fvim.insertTextLine( ident + self.middle + Tag.name[key] + str( Tag.value[key] ), line, buf ) ):
					line += 1
			# 结束行
			fvim.insertTextLine( ident + self.decorator * UsrDecoratorCount + self.end, line, buf )

		# 注释类
		def AnnotateClass( self, line, buf ):
			ident = zsl.LeftWhiteSpace( buf[ line - 1 ] )
			# 首行
			if ( fvim.insertTextLine( ident + self.start, line, buf ) ):
				line += 1
			# 中间行
			for key in self.tag_class:
				if( fvim.insertTextLine( ident + self.middle + Tag.name[key] + str( Tag.value[key] ), line, buf ) ):
					line += 1
			# 结束行
			fvim.insertTextLine( ident + self.end, line, buf )

		# 注释函数
		def AnnotateFunction( self, line, buf ):
			ident = zsl.LeftWhiteSpace( buf[ line - 1 ] )
			# 首行
			if( fvim.insertTextLine( ident + self.start, line, buf ) ):
				line += 1
			# 函数tag
			for key in self.tag_function:
				if( not cmp(key, PARAM) ):
					params = self.GetParameters( line, buf )
					print params
					if( params ):
						cnt = len(params)
						i  = 0
						while( i < cnt ):
							if( fvim.insertTextLine( ident + self.middle + Tag.name[key] + str( Tag.value[key] ) + params[i], line, buf) ):
								line += 1
							i += 1
				elif( fvim.insertTextLine( ident + self.middle + Tag.name[key] + str( Tag.value[key] ), line, buf ) ):
					line += 1
			# 末行
			fvim.insertTextLine( ident + self.end, line, buf )

		# 注释行尾
		def AnnotateLineTail( self, line, buf ):
			strLine = buf[ line - 1 ].rstrip()
			postfix = self.tStart + self.tEnd
			# 已经存在行尾注释则删除
			tail = strLine.rfind( self.tStart.strip())
			if( 0 < tail ):
				strLine = strLine[ 0 : tail ].rstrip()
				fvim.setLineText( strLine, line, buf )
				tail = len( strLine )
			else: # 与前面行尾注释对齐
				align = 0
				preLine = line - 1
				while( preLine >= 1 ):
					index = buf[ preLine - 1 ].find( self.tStart.strip() )
					if( 0 <= index ):
						align = index - len( strLine )
						break
					preLine -= 1
				if( 1 > align ):
					align = 1
				strLine += " " * align + postfix
				fvim.setLineText( strLine, line, buf )
				tail = len( strLine ) - len( self.tEnd )
			# 设置光标位置
			fvim.SetCursor( -1, tail,  buf.number - 1  )


	##!  @brief 	C++ 类	
	##!  
	##!  
	class Cplus( Text ):
		'C++'
		def __init__( self ):
			# 语言名称
			self.name 	= Lang.CPLUS
			# 语法对应的文件类型
			self.syntax 	= [ ".h", ".c", ".hpp", ".cpp", ".hxx", ".cxx", ".java" ]
			# 注释符号
			self.line 	= "// " 	# 单行注释符
			self.start 	= "/**" 	# 多行注释 	首行 	首 注释符
			self.middle 	= " * " 	# 		中间行 	首 注释符
			self.end 	= "*/" 		# 		结束行 	尾 注释符
			self.decorator 	= "*"
			self.tStart 	= "/** " 	# 行尾注释：起始符号
			self.tEnd 	= " */" 	# 行尾注释：结束符号


	##!  @brief	Shell类
	##!  
	##!  
	class Shell( Text ):
		'Shell'
		tag_function 	= [ BRIEF, DETAIL, DETAIL, PARAM, OUTPUT, AUTHOR, DATE ]
		def __init__( self ):
			self.name 	= Lang.SHELL
			self.syntax 	= [ "", ".sh", ".SH", ".shell", ".Shell", ".svr", ".svn", ".bashrc", ".bash_profile", ".gdb", ".dump", ".mk" ]
			self.line 	= "# "
			self.start 	= ""
			self.middle 	= "##! "
			self.end 	= ""
			self.decorator 	= "#"
			self.tStart 	= "##! " 	# 行尾注释：起始符号
			self.tEnd 	= ""		# 行尾注释：结束符号
			# 函数格式
			self.objFunc 	= zsl.RegCompile( r"\s* function \s*" + self.reId + r"\s* \( \s* \).*" )
			# 参数匹配
			self.objPara = zsl.RegCompile( r"( \$\d | \$ \{\s* \d+ \s*\} )\b", re.M )


		# 解析参数
		def GetParameters( self, line, buf ):
			endLine = len( buf )
			funcEnd = line
			while( funcEnd <= endLine ):
				if( fvim.lineStartWith( "}", funcEnd, buf ) ):
					break
				funcEnd += 1
			# 在函数范围 line : funcEnd 内查找$0 $1 ...
			return self.objPara.findall( str( buf[ line : funcEnd-1 ] ) )

	##!  @brief	Python类
	##!  
	##!  
	class Python( Text ):
		'Python'
		def __init__( self ):
			self.name 	= Lang.PYTHON
			self.syntax 	= [ ".py", ".Py", ".PY", ".python", ".Python" ]
			self.line 	= "# "
			self.start 	= ""
			self.middle 	= "##!  "
			self.end 	= ""
			self.decorator 	= "#"
			self.tStart 	= "##! " 	# 行尾注释：起始符号
			self.tEnd 	= ""		# 行尾注释：结束符号
			# 函数格式
			self.objFunc 	= zsl.RegCompile( r"\s* def \s* " + self.reId + r"\s* \( \s* "
					+ r"(?: \s* | \s*\.\.\.\s* | " 
					+ self.reId + r"(?: \s*" + self.reAss + r")?" 
					+ r"(?: \s* \, \s*" + self.reId + r"(?: \s*" + self.reAss + r")?)*"
					+ r"(?: \s* ,  \s* \.\.\. \s*)?  ) \s* \)" )
	

	##!  @brief	Lua类
	##!  
	##!  
	class Lua( Text ):
		'Lua'
		def __init__( self ):
			self.name 	= Lang.LUA
			self.syntax 	= [ ".lua", ".Lua", ".LUA" ]
			self.line 	= "-- "
			self.start 	= ""
			self.middle 	= "--! "
			self.end 	= ""
			self.decorator 	= "-"
			self.tStart 	= "--! " 	# 行尾注释：起始符号
			self.tEnd 	= "" 	# 行尾注释：结束符号
			# 函数格式
			self.objFunc 	= zsl.RegCompile( r"\s* function \s* (?:" + self.reId + r"\s* : \s*)?" + self.reId + r"\s* \( \s* "
					+ r"(?: \s* | \s*\.\.\.\s* | " 
					+ self.reId + r"(?: \s*" + self.reAss + r")?" 
					+ r"(?: \s* \, \s*" + self.reId + r"(?: \s*" + self.reAss + r")?)*"
					+ r"(?: \s* ,  \s* \.\.\. \s*)?  ) \s* \)" )


	##!  @brief	VimL类
	##!  
	##!  
	class VimL( Text ):
		'VimL'
		def __init__( self ):
			self.name 	= Lang.VIML
			self.syntax 	= [ ".vim", ".vimrc" ]
			self.line 	= "\" "
			self.start 	= ""
			self.middle 	= "\"! "
			self.end 	= ""
			self.decorator 	= "\""
			self.tStart 	= "\"! " 	# 行尾注释：起始符号
			self.tEnd 	= "" 		# 行尾注释：结束符号
			# 函数格式
			self.objFunc 	= zsl.RegCompile( r"\s* function \s* \! \s*" + self.reId + r"\s* \( \s* "
					+ r"(?: \s* | \s*\.\.\.\s* | " 
					+ self.reId + r"(?: \s*" + self.reAss + r")?" 
					+ r"(?: \s* \, \s*" + self.reId + r"(?: \s*" + self.reAss + r")?)*"
					+ r"(?: \s* ,  \s* \.\.\. \s*)?  ) \s* \)" )


##!  @brief	注释类
##!  
##!  
class Comment:
	'注释'
	# 构造函数
	def __init__( self ):
		self.langPool 	= [ Lang.Text(), Lang.Cplus(), Lang.Shell(), Lang.Python(), Lang.Lua(), Lang.VimL() ]
		self.lang 	= self.langPool[ 0 ]

	# 当前语法环境匹配( lang.syntax 与 当前文件匹配 )
	def MatchSyntax( self, bufIndex = 0 ):
		ext = fvim.GetFileExtension( bufIndex )
		if( ext in self.lang.syntax ): 	
			return True
		for L in self.langPool:
			if( ext in L.syntax ):
				self.lang = L
				return True
		print "error: not supported file type \"" + ext + "\""
		return False

	# 是否 有效的命令
	def ValidCommand( self, lineRange, bufIndex ):
		if( self.MatchSyntax( bufIndex ) ):
			buf = fvim.ValidIndex( lineRange, bufIndex )
			return buf
		return None

	# 注释
	def do( self, startLine, endLine , buf ):
		commentedLine = 0
		line = startLine
		while( line <= endLine ):
			if ( not fvim.lineStartWith( self.lang.line, line, buf ) ):
				fvim.insertText( self.lang.line, zsl.LeftWhiteSpaceLen( buf[ line-1  ] ), line, buf )
				commentedLine += 1
			line += 1
		return commentedLine
	def ValidDo( self, startLine = 0, endLine = 0, bufIndex = 0 ):
		lineRange = [startLine, endLine] 
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None != buf ):
			self.do( lineRange[0], lineRange[1], buf)
			return True
		return False

		
	# 取消注释
	def undo( self, startLine, endLine, buf ):
		uncommentedLine = 0
		line = startLine
		while( line <= endLine ):
			if( fvim.compatibleDeletePrefix( self.lang.line, line, buf ) ):
				uncommentedLine += 1
			line += 1
		return uncommentedLine
	def ValidUndo( self, startLine = 0, endLine = 0, bufIndex = 0 ):
		lineRange = [startLine, endLine] 
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None != buf ):
			self.undo( lineRange[0], lineRange[1], buf)
			return True
		return False
		
	##!  @brief	注释/取消 第[startLine, endLine]行
	##!    
	##!    使用默认参数时，只对当前 buffer 的 startLine 行进行操作
	##!  @param	self 		对象
	##!  @param	startLine 	注释起始行
	##!  @param	endLine 	注释结束行
	##!  @param	bufIndex 	vim buffer的索引(1,2 ...)
	##!  @return	返回受到影响的行数
	##!  @author	Fstone's ComMent Tool
	##!  @date	2016-09-09
	def CommentToggle( self, startLine = 0, endLine = 0, bufIndex = 0 ):
		# 数据有效性
		lineRange = [ startLine, endLine ]
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None == buf ):
			return 0
		# 注释/取消 记数
		commentedLine = 0
		uncommentedLine = 0
		# 循环 注释/取消 每一行 
		line = lineRange[ 0 ]
		while( line <= lineRange[ 1 ] ):
			if( fvim.compatibleDeletePrefix( self.lang.line, line, buf ) ): 	# 取消
				uncommentedLine += 1
			else: 							# 注释
				fvim.insertText( self.lang.line, zsl.LeftWhiteSpaceLen( buf[ line-1  ] ), line, buf )
				commentedLine += 1
			line += 1
		return commentedLine + uncommentedLine
	
	##!  @brief	添加/删除 自动注释 函数 类 文件头
	##!    
	##!    TODO 注释已存在时自动同步模块更新
	##!  @param	self
	##!  @param	line 		光标所在行
	##!  @param	bufIndex 	打开的文件
	##!  @return	是否生成注释
	##!  @author	Fstone's ComMent Tool
	##!  @date	2016-09-09
	def Module( self, line = 0, bufIndex = 0 ):
		lineRange = [ line, line ]
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None == buf ):
			return False
		line = lineRange[0]
		#   ……     函数名所在行 或 上一行
		if( self.lang.atFunction( line, buf ) ):
			return self.lang.AnnotateFunction( line, buf )
		#   ……     类名所在行 或 上一行
		if( self.lang.atClass( line, buf ) ):
			return self.lang.AnnotateClass( line, buf )
		#  文件前10行
		if( fvim.atFileTop( line, buf) ): 	
			return self.lang.AnnotateFile( line, buf )
		return False

	##!  @brief	插入分隔线
	##!  
	##!  
	##!  @param	self
	##!  @param	line 	行号
	##!  @param	bufIndex 文件buffer索引，默认为当前文件
	##!  @return	True插入, False删除
	##!  @author	Fstone's ComMent Tool
	##!  @date	2016-09-09
	def SeparatorToggle( self, line = 0, bufIndex = 0 ):
		lineRange = [ line, line ]
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None == buf ):
			return False
		self.lang.AnnotateSeparator( lineRange[0], buf )
		return True

	##!  @brief	行尾添加注释
	##!  
	##!  
	##!  @param	self
	##!  @param	line 行号
	##!  @param	bufIndex 文件buffer索引
	##!  @return	无
	##!  @author	Fstone's ComMent Tool
	##!  @date	2016-09-12
	def LineTailToggle( self, line = 0, bufIndex = 0 ):
		lineRange = [ line, line ]
		buf = self.ValidCommand( lineRange, bufIndex )
		if( None == buf ):
			return False
		return self.lang.AnnotateLineTail( lineRange[ 0 ], buf )
