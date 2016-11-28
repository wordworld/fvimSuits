vim套装 fvimSuits
====================
fvimSuits 是一个帮助用户在 Linux 上快速搭建基于 vim 的 IDE ( 集成开发环境 ) 的辅助工具。它包含一个用于下载 vim 插件的部署脚本 deploy_vim_plugin.sh ，和作者编写的一个用于注释各类代码文件的 vim 插件 fcmt 。

1.安装
--------------------
### 首次需 git 安装
(1) 安装 git		：$sudo apt-get install git <br/>
(2) 下载 fvimSuits	：$git clone git://github.com/wordworld/fvimSuits.git <br/>
(3) 下载、部署插件 (下载过程用时较长，请耐心等待)：$cd fvimSuits && ./deploy_vim_plugin.sh <br/>
### 移植已经安装好的 fvimSuits 到其他电脑
(1) 复制整个 $HOME/.vim/ 目录到其他 Linux 主机的 $HOME 目录 <br/>
(2) 部署插件		：$cd ~/.vim/bundle/fcmt && ./portable_deploy_vim_plugin.sh

2.使用
--------------------
### 作者编写的插件
		注释工具 fcmt
		--------------------
		快捷键 m （光标在文件前10行）：自动生成文件头注释，可自定义如作者信息、文件名、更新日期等内容
		快捷键 m （光标在函数名所在行）：自动生成函数注释，可自定义包括摘要说明、参数、返回值等内容
		快捷键 f ：注释/取消注释光标所在行
		快捷键 Ctrl+l ：添加/删除间隔注释行

### 插件管理器 pathogen
包含 ~/.vim/autoload/pathogen.vim 和 ~/.vim/bundle 目录 <br/>
新的插件只需放在 ~/.vim/bundle 目录下，即完成安装。

### 自动完成括号 auto-pairs
当输入左括号，即自动补全右括号，光标回到括号中 <br/>
对 () [] {} 均有效

### 文件目录树 NERDTree
快捷键 Ctrl+n ：在左侧显示当前目录结构

### 文件标签页 miniBufExplorer
已经打开的文件名在顶部行显示，通过双击进行切换

### Taglist
快捷键 Ctrl+a ：在右侧显示当前源代码文件中定义的符号

### 粘贴板管理 Yank-Ring
快捷键 Ctrl+y ：在底部显示本地所有 terminal 中复制的内容，选中后按p进行粘贴。

### 调试插件 congue-gdb

### C语法支持 c.vim

### 配色方案 PaperColor

