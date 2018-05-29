# python + vue project

this project use python api process the data, with the separation of web page file;


# run it
should run respectively python and web page; 
**install**
install python depend， run it
install Vuejs depend， run it
# hasan
# deploy desciption
# 原理
自动部署涉及了若干个角色，主要介绍如下：

GitLab-CI

GitLab自带的持续集成系统，你装的GitLab的那台服务器上就有，无需自行安装。GitLab-CI负责解析.gitlab-ci.yml

.gitlab-ci.yml

GitLab-CI使用YAML文件来管理项目配置，在git项目的根目录下创建此文件，文件中包含一系列的阶段和执行规则。GitLab-CI在push后解析它，根据里面的内容调用runner来执行。YAML配置语法

GitLab-Runner

这个是脚本执行的承载者， .gitlab-ci.yml的script部分就是由runner来负责的。GitLab-CI解析项目里的.gitlab-ci.yml文件之后，根据里面的规则，分配到各个Runner来运行相应的脚本script

# 搭建步骤：

1）升级gitlab，支持gitlabci(已实现)；

2）安装gitlab-runner ，执行器是gitlab-ci.yml实际执行者，需安装gitlab-ci.yml定义的相关构建环境，并想gitlab服务器注册；（以实现）
3）编写gitlab-ci.yml 及相关shell脚本，gitlab-ci.yml 是监听 触发工作的核心。在gitlab-ci.yml可定义 不通的job, 如 build、deploy_test等；将所需的手动触发的操作，编写为相应的job。（以实现
4）Python hasan 生产环境发布 构建好的项目包（已实现部分 还需权限矩阵模块 应用及其他季节API，版本升级）
# hasan（哈桑）——deploy 前端页面



