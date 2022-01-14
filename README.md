<h1 align="center"><img style="width: 90%; padding-top:20px;" src="./lbsh_icon_sm.png"></h1>

## 简介
一些好用的脚本工具，使用 **[lbsh_installer](./lbsh_installer/lbsh_installer)** (以下称`安装器`)安装和更新，也可以脱离安装器单独安装。

## 安装方式(安装器)
1. clone本仓库 `git clone https://github.com/luobozz/my_shell.git $HOME/.lbsh/.git_repositories`
2. 进入lbsh_installer tty模式选择你要的命令, `$HOME/.lbsh/.git_repositories/lbsh_installer/lbsh_installer`，或者使用 `$HOME/.lbsh/.git_repositories/lbsh_installer/lbsh_installer -i ${cmd_name}`安装

## 安装方式(其他)
本仓库每个命令都在`lbsh`目录下，每个命令根目录中都有个`install`命令，使用`install`命令安装
> 环境变量问题：所有项目环境变量都在 [安装器目录](./lbsh_installer/) 的 [环境变量文件](./lbsh_installer/libs/lbsh_profile) 中，把该文件添加进你的环境中然后重新source环境即可，建议脚本 `[ ! -f \"$HOME/.lbsh/.lbsh_profile\" ] || source $HOME/.lbsh/.lbsh_profile` ,

## 已支持命令
- lssh 一个命令行远程管理器，类似docker的操作模式
- lgh git访问嵌套命令，通过更改github.com到国内源加速http访问github资源 `lgh 你的克隆命令`
## feature

- [ ] lb_one_key_for_linux linux的环境重塑脚本，方便在重新装机后重塑自己的桌面环境、开发环境等
- [ ] others...