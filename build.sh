############################################################
##! @brief	fcmt注释工具开发脚本
##!
##! 在命令行执行 ./build cbpi 完成对工具的
##! 	清理（删除python目标文件，参数c）
##! 	构建（编译python代码，生成.pyc目标文件，参数b）
##! 	打包（发布.zip压缩包，不包含代码，参数p）
##! 	安装（配置插件，自动向~/.vimrc添加配置项，参数i）
##! @file	build.sh
##! @author	Fstone's ComMent Tool
##! @date	2016-09-19
##! @version	0.1.2
############################################################

`finclude $0 zsl.sh`

#缺省运行命令参数
option=bi 			# 构建（编译）Build + 安装Install

# 部署选项
plugin_name=fvimSuits 		# 插件文件夹名
plugin_version= 		# 插件版本
package_name=$plugin_name$plugin_version 	# 压缩包(.zip格式)名字(不含后缀名)
src_package=$plugin_name"_src"$plugin_version 	# 源码包
# 安装目录结构：
# $install_dir/
# $install_dir/fcmt/
# $install_dir/fcmt/*.sh
# $install_dir/fcmt/plugin/fvim.vim
# $install_dir/fcmt/plugin/python/*.pyc
plugin_dir=plugin 		# 插件(fvim.vim)目录
python_dir=python 		# python目标文件(.pyc)目录
tmp_dir=fcmt_tmp_dir 		# 临时目录


# 获取脚本绝对路径 build_dir
fullPath=`GetFullPath $0`
build_script=${fullPath##*/}
build_dir=${fullPath%/*}

cd $build_dir
echo 【running $build_script ...】

# 获取命令参数 option
if [ $# -eq 1 ];then
	option=$1
fi

# 清除 Clean ( c )
sn=`expr index "$option" c`
if [ $sn -gt 0 ];then
	echo \>cleaning ...
	cd $build_dir
	if [ -d "$plugin_dir/$python_dir" ];then
		rm -f $plugin_dir/$python_dir/*.pyc
	fi
	if [ -f "$package_name.zip" ];then
		rm -f $package_name.zip
	fi
	if [ -f "$src_package.zip" ];then
		rm -f $src_package.zip
	fi
fi

# 构建 Build ( b )
sn=`expr index "$option" b`
if [ $sn -gt 0 ];then
	# 路径检查
	echo && echo \>building ... && cd $build_dir
	# 编译pyc
	# export PYTHONPATH=$PYTHONPATH:$plugin_dir/$python_dir
	python -m py_compile $plugin_dir/$python_dir/zsl.py 
	python -m py_compile $plugin_dir/$python_dir/fvim.py 
	python -m py_compile $plugin_dir/$python_dir/fcmt.py 
fi

# 打包 Package ( p )
sn=`expr index "$option" p`
if [ $sn -gt 0 ];then
	# 源码包
	echo && echo \>packing $plugin_name to $src_package.zip ...
	cd $build_dir/.. && TryMakeDir $tmp_dir
	mv $build_dir/$plugin_dir/$python_dir/*.pyc $tmp_dir/
	zip -r $src_package.zip $plugin_name
	mv $tmp_dir/*.pyc $build_dir/$plugin_dir/$python_dir/

	# 可执行包
	echo && echo \>packing $plugin_name to $package_name.zip ... && cd $build_dir/..
	mv $build_dir/$plugin_dir/$python_dir/*.py $tmp_dir/
	zip -r $package_name.zip $plugin_name
	mv $tmp_dir/*.py $build_dir/$plugin_dir/$python_dir
	mv $src_package.zip $package_name.zip $build_dir/ && rm -r $tmp_dir

fi

# 安装 Install ( i )
sn=`expr index "$option" i`
if [ $sn -gt 0 ];then
	echo \>installing ...
	# 进行配置 ( 影响 fcmt.vim 和 ~/.vimrc )
	cd $build_dir
	fcmt_file="$build_dir/$plugin_dir/fcmt.vim"
	dir_tag="let s:install_dir"
	FindReplaceLine "$fcmt_file" "$dir_tag" "${dir_tag} = \'$build_dir/$plugin_dir\'"
	# FindSetLines "$HOME/.vimrc" "\" Fstone's ComMent Tool" "source $fcmt_file"
fi

