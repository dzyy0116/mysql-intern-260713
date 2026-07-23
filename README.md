# 实习项目
## 第一周：MySQL+Python交互
### 运行环境
MacOS + MySQL 8.0 + Python3 + pymysql
### 文件说明
1. sql/init.sql：完整初始化脚本，包含创建数据库、学生表、全套增删改查SQL
2. db_helper.py：封装通用MySqlHelper工具类，自动管理连接、事务、异常，使用者仅需传入SQL和参数
3. requirements.txt：项目依赖包列表
### 运行步骤
1. 本地启动MySQL服务，在mysql命令行执行sql/init.sql初始化数据表
2. 修改db_helper.py中MySQL root登录密码
3. 终端进入项目目录，执行 python3 db_helper.py 测试全部CRUD功能
## 第三周：豆瓣电影TOP100爬虫
### 字段设计依据（可视化图表需求）
1. movie_rank：用于榜单排行图表
2. release_year / region：柱状图统计不同年份、地区电影数量
3. movie_type：饼图展示各影片类型占比
4. score、vote_count：散点图分析评分与评价人数的热度关系
### 运行脚本
python3 douban_movie_spider.py
### 实现逻辑
复用第一周封装的MySqlHelper数据库工具类，分页爬取豆瓣TOP250前100条电影，做数据容错清洗后存入可视化专用数据表。
## 第四周：React + Flask 前后端基础联调
1. 后端：flask搭建接口，flask-cors解决跨域，提供GET、POST两个测试接口
2. 前端：create-react-app构建页面，3个输入框、2个功能按钮
   - GET接口：读取输入框1作为URL查询参数，后端返回拼接字符串
   - POST接口：输入框2存入请求Body JSON，输入框3作为URL参数，后端同时接收两类参数并返回
3. 启动方式
   后端：cd flask_backend && python3 app.py
   前端：cd react_frontend && npm start
## 第五周：Ant Design侧边菜单 + ECharts数据库可视化，Flask提供电影统计查询接口
### 任务目标
1. 后端新增数据库统计接口，查询豆瓣电影数据表并转换成ECharts可直接使用的数据格式返回前端；
2. 前端引入 echarts-for-react 完成数据库数据可视化图表渲染；
3. 集成 Ant Design 侧边菜单组件，实现点击菜单切换不同统计图表。

### 后端实现说明（flask_backend/app.py）
1. 引入 pymysql 连接 MySQL 数据库，封装统一数据库连接函数；
2. 保留第四周GET/POST测试接口，新增4套电影统计可视化接口：
   - `/api/chart/year_count`：按上映年份分组统计电影数量，用于年份柱状图
   - `/api/chart/region_count`：按制片地区分组统计电影数量，用于地区柱状图
   - `/api/chart/type_count`：拆分多类型标签并统计各影片类型总数，用于类型饼图
   - `/api/chart/score_vote`：读取电影评分、评价人数，用于热度散点图
3. 接口内部对原始SQL查询结果做数据清洗、格式转换，统一返回 `{code:200, data:[]}` 标准结构。

### 前端实现说明（react_frontend/src/App.js）
1. 安装依赖：`echarts`、`echarts-for-react`、`antd`；
2. 使用 Ant Design Layout + Menu 搭建左侧侧边导航菜单；
3. 通过 `useState` 记录当前选中菜单标识，`useEffect` 监听菜单切换并自动请求对应后端图表接口；
4. 根据选中菜单匹配不同 ECharts 配置项，分别渲染柱状图、饼图、散点图；
5. axios 请求后端可视化接口，接收数据库统计数据完成图表渲染展示。

### 项目启动方式
#### 1. 启动Flask后端（新开终端）
```zsh
cd flask_backend
python3 app.py

## 第六周：数据可视化平台登录注册模块
### 任务目标
搭建系统身份验证模块，实现用户注册、登录、登出功能；增加访问权限控制，未登录用户无法进入可视化图表页面。

### 后端实现说明（flask_backend/app.py）
1. MySQL新建`user`用户表，存储用户名与加密密码；
2. 使用`werkzeug`实现密码哈希加密，数据库不存放明文密码，提升安全性；
3. 新增接口清单：
   - `/api/register`：用户注册接口，校验用户名是否重复；
   - `/api/login`：登录接口，校验账号密码，登录成功写入Session；
   - `/api/logout`：清空Session，实现退出登录；
   - `/api/check_login`：登录状态校验接口，供前端路由鉴权使用；
4. 开启跨域支持Cookie传递，保证Session会话正常维持。

### 前端实现说明（react_frontend/src/App.js）
1. 引入`react-router-dom`实现页面路由跳转；
2. 划分三个页面：登录页、注册页、可视化图表主页；
3. 实现路由守卫：访问图表页面时先请求后端校验登录状态，未登录自动重定向登录页面；
4. 页面功能：账号注册、账号登录、登出系统。

### 项目启动方式
#### 1. 启动Flask后端（新开终端）
```zsh
cd flask_backend
python3 app.py