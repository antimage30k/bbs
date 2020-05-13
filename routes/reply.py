import time

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    Request)

from models.base_model import current_time
from models.message import Messages
from models.topic import Topic
from routes import *

from models.reply import Reply


main = Blueprint('reply', __name__)


def users_from_content(content):
    # 内容 @123 内容
    # 如果用户名含有空格 就不行了 @name 123
    # 'a b c' -> ['a', 'b', 'c']
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            print('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, reply_link, reply_content):
    print('send_mail', sender, receivers, reply_content)
    content = '链接：<a href="{}">{}</a>\n内容：{}'.format(
        reply_link,
        reply_link,
        reply_content,
    )
    for r in receivers:
        title = '{}在回复中at了你，快来看看吧。'.format(sender.username)
        Messages.send(
            title=title,
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )


@main.route("/add", methods=["POST"])
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, request.referrer, content)

    form = form.to_dict()
    m = Reply.new(form, user_id=u.id)
    # 回复顶帖功能
    t_id = form['topic_id']
    reply_time = current_time()
    Topic.update(t_id, updated_time=reply_time)
    return redirect(url_for('topic.detail', id=m.topic_id))

