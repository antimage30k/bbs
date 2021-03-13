import uuid
from enum import Enum

import config
from flask import Blueprint, request, render_template, abort, redirect, url_for

from task_queue import send_mail_async
from models.user import User
import redis


reset_token = redis.StrictRedis()


# 枚举错误类型
class Error(Enum):
        invalid_username = '用户名不存在'
        invalid_token = '密码重置链接错误或已失效'


main = Blueprint('reset', __name__)


# 发送密码重置链接邮件
@main.route('/send', methods=['POST'])
def send():
    username = request.form['username']
    u = User.one(username=username)
    # 用户名不存在则返回一个错误，存在则发送邮件
    if u is None:
        return render_template('error.html', message=Error.invalid_username.value)
    else:
        send_reset_mail(u)
    return redirect(url_for("index.index"))


# 存储随机生成的token 和 user id
# 发送密码重置邮件
def send_reset_mail(u):
    token = str(uuid.uuid4())
    reset_token.set(token, u.id)
    # 10 min 过期
    reset_token.expire(token, 600)
    content = 'https://www.{}/reset/view?token={}'.format(config.host, token)
    # 发送邮件
    send_mail_async.delay(
        subject='Reset Password',
        author=config.admin_mail,
        to=u.email,
        content=content
    )


@main.route('/forget/password')
def forget_pw():
    return render_template('forget_pw.html')


# 点击重置链接之后访问的路由
@main.route('/view')
def view():
    token = request.args['token']
    # token 有效，则重置密码
    if reset_token.exists(token):
        return render_template('reset_pw.html', token=token)
    else:
        # token 无效则返回一个错误页面
        return render_template('error.html', message=Error.invalid_token.value)


# 重置密码的路由
@main.route('/update')
def update_password():
    # 从url 里拿到token 和password，交给update_pw 函数去处理
    args = request.args
    token = args['token']
    new_password = args['password']
    if reset_token.exists(token):
        update_pw(token, new_password)
        return redirect(url_for("index.index"))
    else:
        # token 无效则返回一个错误页面
        return render_template('error.html', message=Error.invalid_token.value)


# 更新密码
def update_pw(token, new_password):
    user_id = int(reset_token.get(token))
    # 密码加盐
    new_password = User.salted_password(new_password)
    User.update(user_id, password=new_password)
    # 从reset_token 字典里删除已经用过的token
    reset_token.delete(token)
