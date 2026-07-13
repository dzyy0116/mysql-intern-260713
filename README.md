# MySQL+Python交互
## 运行环境
MacOS + MySQL 8.0 + Python3 + pymysql
## 文件说明
1. sql/init.sql：完整初始化脚本，包含创建数据库、学生表、全套增删改查SQL
2. db_helper.py：封装通用MySqlHelper工具类，自动管理连接、事务、异常，使用者仅需传入SQL和参数
3. requirements.txt：项目依赖包列表
## 运行步骤
1. 本地启动MySQL服务，在mysql命令行执行sql/init.sql初始化数据表
2. 修改db_helper.py中MySQL root登录密码
3. 终端进入项目目录，执行 python3 db_helper.py 测试全部CRUD功能