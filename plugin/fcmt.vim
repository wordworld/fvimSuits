""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""! @brief	fcmt 插件 for Vim
""! 
""! 
""! @file	fcmt.vim
""! @path	prj/fvimSuits/plugin
""! @author	fstone.zh@foxmail.com
""! @date	2016-12-14
""! @version	0.1.0
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
" 保证只加载一次
if exists("g:fstone_comment")
    finish
endif

" 安装目录(以 / 开始的绝对路径)
let s:install_dir = escape(expand('<sfile>:p:h'), '\')

" 初始化
python3<<EOF
import vim
sys.path.append( str( vim.eval( "s:install_dir" ) ) + "/python" )
EOF


" cf : 注释本行
" command! -nargs=0 CCL call DoCmtCurLine()
nnoremap cf :call DoCmtCurLine()<CR>

function! DoCmtCurLine()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.ValidDo( )
EOF
endfunction


" df : 取消注释本行
" command! -nargs=0 UCCL call UndoCmtCurLine()
nnoremap df :call UndoCmtCurLine()<CR>

function! UndoCmtCurLine()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.ValidUndo( )
EOF
endfunction


" f : 注释/取消 本行
" command! -nargs=0 CCLT call CmtCurLineToggle()
nnoremap f :call CmtCurLineToggle()<CR>

function! CmtCurLineToggle()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.CommentToggle( )
EOF
endfunction


" m : 模块注释文件、函数、类
" command! -nargs=0 CM call CmtModule()
nnoremap m :call CmtModule()<CR>

function! CmtModule()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.Module( )
EOF
endfunction


" Ctrl+L : 添加/删除 一行注释分隔符
" command! -nargs=0 CST call CmtSeparatorToggle()
nnoremap <C-L> :call CmtSeparatorToggle()<CR>

function! CmtSeparatorToggle()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.SeparatorToggle()
EOF
endfunction


" t : 添加/删除 行尾注释符
" command! -nargs=0 CLTT call CmtLineTailToggle()
nnoremap t :call CmtLineTailToggle()<CR>

function! CmtLineTailToggle()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.LineTailToggle()
EOF
endfunction

" 保存时自动更新 
function! CmtAutoUpdate()
python3<<EOF
import fcmt
cmt = fcmt.Comment()
cmt.AutoUpdate()
EOF
endfunction

autocmd BufWritePre * call CmtAutoUpdate()
" autocmd BufNewFile * call 


"! @brief	绘制表格 
"! 
"! 
"! @param	...	row, col, width=4, height=1	
"! @return	无
"! @date	2016-12-13
function! DrawTable(...)
python3<<EOF
import fcmt
rcwh=[2, 8, 4, 1, None] # 默认2行8列，列宽4,行高1, 前缀 None
cnt = int(vim.eval("a:0"))
if(len(rcwh) < cnt):
	cnt = len(rcwh)
idx = 1
while( idx <= cnt ):
	rcwh[idx-1] = vim.eval("a:"+str(idx))
	idx+=1
cmt = fcmt.Comment()
cmt.DrawTable(rcwh[0], rcwh[1], rcwh[2], rcwh[3], rcwh[4])
EOF
endfunction
:com -nargs=* Tbl call DrawTable(<f-args>)


"! @brief	绘制目录
"! 
"! 
"! @param	... dir, level
"! @return	无
"! @date	2016-12-13
function! DrawDir(...)
python3<<EOF
import fcmt
# 默认绘制当前目录, 递归绘制, 无前缀, 不显示全部
args=[ "./", 0, None, 0 ]
cnt = int(vim.eval("a:0"))
if(cnt > len(args)):
	cnt = len(args)
idx=1
while(idx<=cnt):
	args[idx-1] = vim.eval("a:"+str(idx))
	idx+=1
cmt = fcmt.Comment()
cmt.DrawDir(args[0], args[1], args[2], args[3])
EOF
endfunction
:com -nargs=* -complete=file Dir call DrawDir(<f-args>)
