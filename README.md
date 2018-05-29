# python + vue project

this project use python api process the data, with the separation of web page file;

# run it
should run respectively python and web page; 
** install **
install python depend， run it
install Vuejs depend， run it
---
# hasan
# deploy desciption(hasan发布模块实现)
# 原理

**通过监听 可控分支，实现自动构建 并部署到测试环境。（gitlab.yml）,并将构建包同步到 HTTP发布服务器**
**生产环境通过 HTTP发布服务器 自行编写发布流程（Python、ansible palybook.yml、Vue前端**
自动部署涉及了若干个角色，主要介绍如下：

GitLab-CI

GitLab自带的持续集成系统，你装的GitLab的那台服务器上就有，无需自行安装。GitLab-CI负责解析.gitlab-ci.yml

.gitlab-ci.yml

GitLab-CI使用YAML文件来管理项目配置，在git项目的根目录下创建此文件，文件中包含一系列的阶段和执行规则。GitLab-CI在push后解析它，根据里面的内容调用runner来执行。YAML配置语法

GitLab-Runner

这个是脚本执行的承载者， .gitlab-ci.yml的script部分就是由runner来负责的。GitLab-CI解析项目里的.gitlab-ci.yml文件之后，根据里面的规则，分配到各个Runner来运行相应的脚本script

# 搭建步骤：

**基础服务环境**
* - 服务器之间需要 开启免密传输（基础环境）
* - 要一套 Vue代码
* - 一个gitlab 服务器1
* - 需要在Vue代码中 加入 gitlab.yml 文件，和shell script 脚本，用来完成ci,实现监听分支 发布到测试的流程。 
* - 一个 nodejs runner 服务器1
* - 一个存放 打包后文件的 服务器(构建好的包通过 rsync同步到 nginx 或Apache做发布目录中)1
* - 不少于两天的发布客户端服务器2（每个环境）
* - ansible 接口支持，hasan 上已有playbook接口 调用基于playbook.yml 封装使用。

* 1）升级gitlab，支持gitlabci(已实现)；
* 2）安装gitlab-runner ，执行器是gitlab-ci.yml实际执行者，需安装gitlab-ci.yml定义的相关构建环境，并想gitlab服务器注册；（以实现）
* 3）编写gitlab-ci.yml 及相关shell脚本，gitlab-ci.yml 是监听 触发工作的核心。在gitlab-ci.yml可定义 不通的job, 如 build、deploy_test等；将所需的手动触发的操作，编写为相应的job。（以实现
* 4）Python hasan 生产环境发布 构建好的项目包（已实现部分 还需权限矩阵模块 应用及其他季节API，版本升级）
# hasan（哈桑）——deploy 前端页面


![image](https://github.com/xiaofangl/hasan/blob/master/tupian/index.jpeg?raw=true)
![image](https://github.com/xiaofangl/hasan/blob/master/tupian/add.jpeg?raw=true)
![image](https://github.com/xiaofangl/hasan/blob/master/tupian/manage.jpeg?raw=true)

![image](https://github.com/xiaofangl/hasan/blob/master/tupian/deploy.jpeg?raw=true?)
![image](https://github.com/xiaofangl/hasan/blob/master/tupian/choose_branch.jpeg?raw=true)
![image](https://github.com/xiaofangl/hasan/blob/master/tupian/deploy_end.jpeg?raw=true)
