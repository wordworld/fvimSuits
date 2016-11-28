#!/bin/bash
############################################################
##! @brief	vim 插件部署脚本
##! 
##! 
##! @file	deploy_vim_plugin.sh
##! @path	fvimSuits
##! @author	fstone.zh@foxmail.com
##! @date	2016-11-24
##! @version	0.1.2
############################################################
bash zsl.sh setup_finclude_cmd
if [ $? -ne 0 ];then exit; fi

`finclude $0 zsl.sh`
echo $@ | grep -q "\-t" && TEST=echo || TEST=''

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
'set cindent'		# 使用 C/C++ 的自动缩进方式
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
'map <C-w> :q<CR>' 	# Ctrl+w 退出
'map <F7> :w<CR> :!clear<CR> :!g++ -std=c++11 -g % -o %:h/%:r<CR>'	# F7 g++编译
'map <F9> :!chmod +x %:h/%:r<CR> :!clear<CR> :!./%:h/%:r<CR>'		# F9 运行
'map <F5> :!gdb %:h/%:r<CR>'						# F5 gdb调试

# 光标可从行首/末跳到另一行
'set whichwrap'
'=b,s,<,>,[,]' 

# 记住上次打开位置
'au BufReadPost'
" * if line(\"\'\\\\\"\") > 0 && line(\"\'\\\\\"\") <= line(\"\$\") | exe \"normal g\'\\\\\"\" | endif" 
)

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

mkdir -p $dir_auto $dir_bundle
cd $dir_auto

# 插件管理器 pathogen
plugin_mgr=("pathogen.vim" "https://tpo.pe/pathogen.vim")
cfg_plugin_mgr=("execute pathogen#infect()" "syntax on" "filetype plugin indent on")
HighLightStep 2 check ${plugin_mgr[0]} from ${plugin_mgr[1]}
$TEST curl -LSso ${plugin_mgr[0]} ${plugin_mgr[1]}
if [ $? -ne 0 ];then exit; fi
$TEST FindSetLines $vimrc "${cfg_plugin_mgr[0]}" "${cfg_plugin_mgr[@]}"

cd $dir_bundle

# 注释工具
suits=("fvimSuits" "git://github.com/wordworld/fvimSuits.git" "fvimSuits")
GitCheck "${suits[@]}"

# 自动完成括号输入 auto-pairs
brackets_complete=("autopairs.vim" "git://github.com/jiangmiao/auto-pairs.git" "auto-pairs")
GitCheck "${brackets_complete[@]}"

# 文件目录树 NERDTree
directory_tree=("NERDTree.vim" "git://github.com/scrooloose/nerdtree.git" "nerdtree")
cfg_directory_tree=( "map <C-n> :NERDTreeToggle<CR>")
GitCheck "${directory_tree[@]}"
$TEST FindSetLines $vimrc "${cfg_directory_tree[0]}" "${cfg_directory_tree[0]}"

# 文件标签
tab_label=( "MiniBufExplorer" "git://github.com/vim-scripts/minibufexplorerpp.git" "minibufexplorer")
GitCheck "${tab_label[@]}"

# 符号定义列表 TagList
taglist=("taglist" "git://github.com/vim-scripts/taglist.vim.git" "taglist")
cfg_taglist=(
	"map <C-a> :TlistToggle<CR>"
	"let Tlist_Show_One_File=1" 
	"let Tlist_Exit_OnlyWindow=1" 
	"let Tlist_Use_Right_Window=1" 
	"let Tlist_Sort_Type=\"name\""
	)
GitCheck "${taglist[@]}"
$TEST FindSetLines $vimrc "${cfg_taglist[0]}" "${cfg_taglist[@]}"

# 粘贴板
clipboard=("yank-ring" "git://github.com/vim-scripts/YankRing.vim.git" "yank-ring")
GitCheck "${clipboard[@]}"
cfg_clipboard=("map <C-y> :YRShow<CR>")
$TEST FindSetLines $vimrc "${cfg_clipboard[0]}" "${cfg_clipboard[@]}"

# gdb调试
gdb_runner=("conque-gdb" "git://github.com/vim-scripts/Conque-GDB.git" "conque-gdb")
GitCheck "${gdb_runner[@]}"

# c语言
code_c=("c.vim" "https://github.com/vim-scripts/c.vim" "c")
GitCheck "${code_c[@]}"

# 词典
# dict=("StarDict" "git://github.com/vim-scripts/vim-stardict.git" "StarDict")
# cfg_dict=("nnoremap <leader>lw :StarDict<CR>"	"nnoremap <leader>lc :StarDictCursor<CR>")
# GitCheck "${dict[@]}"
# $TEST FindSetLines $vimrc "${cfg_dict[0]}" "${cfg_dict[@]}"

# 配色
color_theme=("PaperColor" "git://github.com/vim-scripts/PaperColor.vim.git" "PaperColor")
cfg_color_theme=("let g:PaperColor_Dark_Override = { 'background' : '#1c1c1c', 'cursorline' : '#abcdef', 'matchparen' : '#3a3a3a', 'comment' : '#5f875f'  }"
	"let g:PaperColor_Light_Override = { 'background' : '#abcdef', 'cursorline' : '#dfdfff', 'matchparen' : '#d6d6d6' , 'comment' : '#8e908c'  }"
	"set t_Co=256"
	"set background=dark"
	"colorscheme PaperColor")
GitCheck "${color_theme[@]}"
sed -i 's/\r//g' $dir_bundle/${color_theme[2]}/colors/PaperColor.vim
$TEST FindSetLines $vimrc "${cfg_color_theme[0]}" "${cfg_color_theme[@]}"

