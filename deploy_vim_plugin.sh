#!/bin/bash
############################################################
##! @brief	vim 插件部署脚本
##! 
##! 
##! @file	deploy_vim_plugin.sh
##! @path	.vim/bundle/fcmt
##! @author	fstone.zh@foxmail.com
##! @date	2023-02-16
##! @version	0.1.2
############################################################
if [ -f "zsl.sh" ];then	bash zsl.sh setup_finclude_cmd;fi
`finclude $0 portable_deploy_vim_plugin.sh`
if [ $? -ne 0 ];then exit; fi

mkdir -p $dir_auto $dir_bundle
cd $dir_auto

# 1. 插件管理器 pathogen
HighLightStep 3 download ${plugin_mgr[0]} from ${plugin_mgr[1]}
$TEST curl -LSso ${plugin_mgr[0]} ${plugin_mgr[1]}
if [ $? -ne 0 ];then exit; fi

cd $dir_bundle

# 2. 注释工具
GitCheck "${src_comment[@]}"

# 3. 自动完成括号输入 auto-pairs
GitCheck "${brackets_complete[@]}"

# 4. 文件目录树 NERDTree
GitCheck "${directory_tree[@]}"

# 5. 文件标签
GitCheck "${tab_label[@]}"

# 6. 符号定义列表 TagList
GitCheck "${taglist[@]}"

# 7. 粘贴板
GitCheck "${clipboard[@]}"

# 8. gdb调试
# GitCheck "${gdb_runner[@]}"

# 9. c语言
GitCheck "${code_c[@]}"

# 10. 配色
GitCheck "${color_theme[@]}"
sed -i 's/\r//g' $dir_bundle/${color_theme[1]}/colors/PaperColor.vim

# 11. 状态栏
GitCheck "${status_bar[@]}"
GitCheck "${status_bar_themes[@]}"

