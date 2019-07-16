# 基于 Flask 的论坛


**地址：** 
- https://www.rieruuuu.xyz

**测试账号：** 
- 用户名：`test` 
- 密码：`123`


**简介**
-
- 实现用户注册与登录，重置密码，主题创建、浏览与回复，用户个人资料管理，站内信和邮件通知等功能。
- 使用 `MySQL` 存储数据，基于 `SQLAlchemy` 实现 `ORM` 。
- 基于 `Redis` 实现 `CSRF token` 在多进程下的数据共享。
- 对访问频率高而变动频率低的数据基于 `Redis` 进行了缓存优化。
- 应用 `Jinja2` 模板继承复用 `HTML` 页面通用元素，提高开发效率。
- 使用 `nginx` 反向代理静态资源，提升访问速度；`Supervisor` 做进程管理，`Gunicorn` 实现多进程负载均衡，gevent开启协程提高并发性能。
- 基于 `Celery` 和 `Redis` 实现消息队列，处理高并发请求并保证数据安全；
- 编写 `Shell` 脚本，在 `Linux` 服务器上实现一键部署。


**功能演示**
- 
- 注册与登录
![register-login.gif](https://i.loli.net/2019/07/11/5d26c5dd6176251745.gif)

- 回复主题
![reply-topic.gif](https://i.loli.net/2019/07/11/5d26c710e7a7c86528.gif)

- 发表主题与 `CSRF` 防御
![csrf-defence.gif](https://i.loli.net/2019/07/11/5d26c7320578f36848.gif)

- 修改个人资料
![setting.gif](https://i.loli.net/2019/07/11/5d26c74a5e6b510146.gif)

- 密码重置功能
![reset-password.gif](https://i.loli.net/2019/07/11/5d26c75777bd322474.gif)

- 站内信与邮件通知
![message.gif](https://i.loli.net/2019/07/11/5d26c7509310265855.gif)


**依赖**
-
- Ubuntu 18.04
- Python 3.6


**如何运行**
-
- 将项目文件克隆到 `/var/www` 文件夹下，项目文件夹作为根目录

- 您需要在根目录下自行添加 `config.py` 文件、 `secret.py` 文件和 `dbpassword.sh` 文件

  - `config.py` 内容为
    ```python
    test_mail = '您的测试邮箱（同时也是 admin 用户 和 test 用户的默认邮箱）'
    admin_mail = '您的企业邮箱地址'
    smtp_server = '您的企业邮箱发送邮件服务器地址'
    smtp_port = 您的企业邮箱发送服务器 SSL 端口
    # 以腾讯企业邮箱为例，smtp_server = 'smtp.exmail.qq.com' smtp_port = 465
    ```

  - `secret.py` 内容为
    ```python
    mail_password = '您的企业邮箱密码'
    secret_key = '您的自定义 Flask 密钥'
    database_password = '您的 MYSQL 数据库密码'
    ```
    
  - `dbpassword.sh` 内容为
	>您设置的 MYSQL 数据库密码

- 根据您的部署域名和 `CA` 证书文件地址，修改 `bbs.nginx` 文件
 
- 执行 `bash deploy.sh $(cat dbpassword.sh)` 命令