# 基于 Flask 的论坛
———— ———— ———— ———— ———— ————

**地址：** 
- https://www.rieruuuu.xyz

**测试账号：** 
- 用户名：`test` 
- 密码：`123`


**简介**
-
- 实现主题创建、浏览与回复，用户个人资料管理，站内信和邮件通知等功能；
- 基于 `SQLAlchemy` 实现 `ORM` ；
- 基于 `redis` 实现 `CSRF` 防御和密码重置功能；
- 应用 `Jinja2` 模板继承技术，复用 `HTML` 通用元素提高开发效率；
- `nginx` 反向代理静态资源，提升服务器效率；`Supervisor` + `gunicorn` 做进程管理；
- `gevent` 实现协程提高并发性能， `Celery` + `redis` 实现消息队列均衡负载；
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
- 将文件拷贝到 `/var/www/bbs` 文件夹下作为根目录

- 您需要在根目录下自行添加 `secret.py` 文件和 `config.py` 文件

- `secret.py` 内容为
>mail_password = '您的企业邮箱密码'

>secret_key = '您的 Flask 密钥'

>database_password = '您的 MYSQL Server 密码'

- `config.py` 内容为
>test_mail = '您的测试邮箱（同时也是 admin 用户 和 test 用户的默认邮箱）'

>admin_mail = '您的企业邮箱地址（您也可以使用我提供的邮箱： `RieRuuuu@rieruuuu.xyz` ）'

- 执行 `bash deploy.sh` 命令