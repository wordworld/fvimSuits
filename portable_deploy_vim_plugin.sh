#!/bin/bash
############################################################
##! @brief	vim 插件部署脚本(portable版)
##! 
##! 
##! @file	portable_deploy_vim_plugin.sh
##! @path	.vim/bundle/fcmt
##! @author	fstone.zh@foxmail.com
##! @date	2023-02-17
##! @version	0.1.0
############################################################
if [ -f "zsl.sh" ];then	bash zsl.sh setup_finclude_cmd;fi
`finclude $0 zsl.sh`
if [ $? -ne 0 ];then exit; fi

SetTEST $@

dir_vim=$HOME/.vim
dir_auto=$dir_vim/autoload
dir_bundle=$dir_vim/bundle
vimrc=$HOME/.vimrc
bashrc=$HOME/.bashrc


vim_cfg_item=(
'set nocompatible'	# vi兼容性设定
'set fileencodings=utf-8,gbk' # 文件编码，支持中文
'set autowrite'		# 自动保存
'set autoindent'	# 自动缩进
'set smartindent'	# 智能缩进
# 'set cindent'		# 使用 C/C++ 的自动缩进方式
'set linebreak'		# 整词换行
'set showmatch'		# 显示 括号匹配
'set backspace=2'	# 使能 退格键
'set mouse=a'		# 使能 鼠标
'set pastetoggle=<F12>'	# F12 切换原文粘贴模式（此模式下暂停自动缩进等功能）
'set history=50'	# 历史记录50条
'set hidden'		# Hide buffers when they are abandoned
'set number'		# 显示 行号
'set showcmd'		# 显示 输入的命令
'set showmode'		# 显示 当前模式
'set ruler'		# 显示 窗口标尺，用于显示光标所在”行号，列号“。如果窗口有状态行，标尺显示在状态行上。否则，显示在屏幕最后一行。
'set laststatus=2'	# 显示 最后一个窗口的状态行；设为1则窗口数多于一个的时候显示最后一个窗口的状态行；0不显示最后一个窗口的状态行
'set previewwindow'	# 标识 预览窗口
'set ignorecase'	# 模式串 忽略大小写
'set smartcase'		# 模式串 包含大写字母时，不忽略大小写
'set incsearch'		# 匹配串 即时定位
'set hlsearch'		# 匹配串 高亮显示
'nnoremap s :w<CR>'	# s 保存
'nnoremap ( :bp<CR>'	# ( 打开上一个文件
'nnoremap ) :bn<CR>'	# ) 打开下一个文件
'map <C-d> :q<CR>' 	# Ctrl+w 退出
'map <C-z> :shell<CR>' 	# Ctrl+z vim 中打开 shell
'map <F7> :w<CR> :!clear<CR> :!g++ -std=c++11 -g % -o %:h/%:r<CR>'	# F7 g++编译
'map <F9> :!chmod +x %:h/%:r<CR> :!clear<CR> :!./%:h/%:r<CR>'		# F9 运行
'map <F5> :!gdb %:h/%:r<CR>'						# F5 gdb调试

# 态栏主题 vim-airline-themes settings
'let g:airline_powerline_fonts=1'
"let g:airline_theme='distinguished'"
# 去掉状态栏右端红色警告
"let g:airline_section_warning = ''"
# unicode symbols
"let g:airline_left_sep = '>'"
"let g:airline_right_sep = '>'"
"if !exists('g:airline_symbols')"
"    let g:airline_symbols = {}"
"endif"
"let g:airline_symbols.colnr = ' ℅'"
"let g:airline_symbols.crypt = '🔒'"
"let g:airline_symbols.linenr = ' ␊'"
"let g:airline_symbols.branch = '⎇'"

# 光标可从行首/末跳到另一行
'set whichwrap'
'=b,s,<,>,[,]' 

# 记住上次打开位置
'au BufReadPost'
" * if line(\"\'\\\\\"\") > 0 && line(\"\'\\\\\"\") <= line(\"\$\") | exe \"normal g\'\\\\\"\" | endif" 
)

# 0.[1] 设置.vimrc
HighLightStep 3 config  ~/.vimrc 
cfg_item_cnt=${#vim_cfg_item[@]}
normal_cfg_cnt=$(($cfg_item_cnt-4))
i=0
while [ $i -lt $normal_cfg_cnt ];do
	$TEST FindSetLines "$vimrc" "${vim_cfg_item[i]}" "${vim_cfg_item[i]}"
	((i++))
done

while [ $i -lt $cfg_item_cnt ]; do
	$TEST FindSetLines "$vimrc" "${vim_cfg_item[i]}" "${vim_cfg_item[*]:i:2}"
	((i+=2))
done

# 1.[2] 插件管理器 pathogen
plugin_mgr=("pathogen.vim" "https://tpo.pe/pathogen.vim")
cfg_plugin_mgr=("execute pathogen#infect()" "syntax on") # "filetype plugin indent on" 可能导致.py文件中以空格代替Tab
HighLightStep 3 config ${plugin_mgr[0]}
$TEST FindSetLines $vimrc "${cfg_plugin_mgr[0]}" "${cfg_plugin_mgr[@]}"

# 2. 注释工具
src_comment=("fvimSuits" "fcmt" "git://github.com/wordworld/fvimSuits.git")

# 3. 自动完成括号输入 auto-pairs
brackets_complete=("autopairs" "auto-pairs" "https://github.com/jiangmiao/auto-pairs.git")

# 4.[3] 文件目录树 NERDTree
directory_tree=("NERDTree" "nerdtree" "https://github.com/scrooloose/nerdtree.git")
cfg_directory_tree=( "map <C-t> :NERDTreeToggle<CR>")
GitCheck "${directory_tree[@]:0:2}"
$TEST FindSetLines $vimrc "${cfg_directory_tree[0]}" "${cfg_directory_tree[0]}"

# 5. 文件标签
tab_label=( "MiniBufExplorer" "minibufexplorer" "https://github.com/vim-scripts/minibufexplorerpp.git")

# 6.[4] 符号定义列表 TagList
taglist=("TagList" "taglist" "https://github.com/vim-scripts/taglist.vim.git")
cfg_taglist=(
	"map <C-a> :TlistToggle<CR>"
	"let Tlist_Show_One_File=1" 
	"let Tlist_Exit_OnlyWindow=1" 
	"let Tlist_Use_Right_Window=1" 
	"let Tlist_Sort_Type=\"name\""
	)
GitCheck "${taglist[@]:0:2}"
$TEST FindSetLines $vimrc "${cfg_taglist[0]}" "${cfg_taglist[@]}"

# 7.[5] 粘贴板
clipboard=("Yank-Ring" "yank-ring" "https://github.com/vim-scripts/YankRing.vim.git")
cfg_clipboard=("map <C-y> :YRShow<CR>")
GitCheck "${clipboard[@]:0:2}"
$TEST FindSetLines $vimrc "${cfg_clipboard[0]}" "${cfg_clipboard[@]}"

# 8. gdb调试
# gdb_runner=("conque-gdb" "conque-gdb" "https://github.com/vim-scripts/Conque-GDB.git")

# 9. c语言
code_c=("c.vim" "c" "https://github.com/vim-scripts/c.vim")

# 10.[6] 配色
color_theme=("PaperColor" "papercolor" "https://github.com/vim-scripts/PaperColor.vim.git")
cfg_color_theme=("let g:PaperColor_Dark_Override = { 'background' : '#1c1c1c', 'cursorline' : '#262626', 'matchparen' : '#3a3a3a', 'comment' : '#5f875f'  }"
	"let g:PaperColor_Light_Override = { 'background' : '#abcdef', 'cursorline' : '#dfdfff', 'matchparen' : '#d6d6d6' , 'comment' : '#8e908c'  }"
	"set t_Co=256"
	"set background=dark"
	"colorscheme PaperColor")
GitCheck "${color_theme[@]:0:2}"
$TEST FindSetLines $vimrc "${cfg_color_theme[0]}" "${cfg_color_theme[@]}"

# 11. 状态栏
status_bar=("AirLine" "airline" "https://github.com/vim-airline/vim-airline.git")
status_bar_themes=("AirLineThemes" "airline-themes" "https://github.com/vim-airline/vim-airline-themes.git")

