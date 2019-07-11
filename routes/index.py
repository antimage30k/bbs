import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    abort,
    send_from_directory
)
from werkzeug.datastructures import FileStorage

from models.reply import Reply
from models.topic import Topic
from models.user import User
from routes import current_user, login_required


# import redis
#
# cache = redis.StrictRedis()


from utils import log

main = Blueprint('index', __name__)

"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""


@main.route("/")
@login_required
def index():
    u = current_user()
    # ts = Topic.all()
    # 按 updated_time 降序排列
    ts = Topic.query.order_by(Topic.updated_time.desc()).all()
    latest_topics = Topic.all_creat_time_desc()
    return render_template("index.html", current_user=u, topics=ts, latest_topics=latest_topics)


@main.route("/register", methods=['POST'])
def register():
    form = request.form.to_dict()
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('index.login_page'))


@main.route('/login/view')
def login_page():
    return render_template('login.html')


@main.route('/register/view')
def register_page():
    return render_template('register.html')


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return render_template('login.html')
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 转到 topic.index 页面
        return redirect(url_for('index.index'))
    # form = request.form
    # u = User.validate_login(form)
    # if u is None:
    #     return redirect(url_for('.index'))
    # else:
    #     # session_id 设置为随机字符串，并在redis 中保存session_id 和user id 的映射关系
    #     session_id = str(uuid.uuid4())
    #     session_redis.set(session_id, u.id)
    #     # 登录成功，返回一个欢迎页面
    #     r = make_response(render_template('welcome.html', username=u.username))
    #     # 设置response 的headers ，添加Set-Cookie 字段
    #     r.headers.set('Set-Cookie', 'session_id={}'.format(session_id))
    #     return r

        # redirect_to_index = redirect('/user/login/view?result={}'.format(result))
        # response = current_app.make_response(redirect_to_index)
        # response.set_cookie('session_id', value=session_id)
        # return response


def not_found(e):
    return render_template('404.html')


# profile 路由用来看自己， user_detail 路由用来看别的用户
@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return redirect(url_for('.user_detail', id=u.id))


def recent_topic(user_id):
    ts = Topic.all_creat_time_desc(user_id=user_id)
    return ts


def recent_reply(user_id):
    # sqlalchemy join 解决 N+1 问题
    tsp = Topic.query.join(Reply, Reply.topic_id == Topic.id).\
        filter(Reply.user_id == user_id).order_by(Reply.id.desc()).all()
    return tsp

    # rs = Reply.all_creat_time_desc(user_id=user_id)
    # # 再由reply 拿到对应的topics_participated,
    # tsp = []
    # for r in rs:
    #     t = Topic.one(id=r.topic_id)
    #     # 防止tsp 含有重复的topic
    #     if t not in tsp:
    #         tsp.append(t)
    # return tsp
    # k = 'replied_topic_{}'.format(user_id)
    # if cache.exists(k):
    #     v = cache.get(k)
    #     ts = json.loads(v)
    #     return ts
    # else:
    #     rs = Reply.all_creat_time_desc(user_id=user_id)
    #     ts = []
    #     for r in rs:
    #         t = Topic.one(id=r.topic_id)
    #         ts.append(t)
    #     # json
    #     v = json.dumps([t.json() for t in ts])
    #     cache.set(k, v)
    #
    #     return ts


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        # 先通过 id ，查询到该id 所有发布的topic 和reply
        user_id = u.id
        ts = recent_topic(user_id)
        tsp = recent_reply(user_id)

        return render_template('profile.html', user=u, created=ts, replied=tsp)


# @main.route('/profile')
# def profile():
#     print('running profile route')
#     u = current_user()
#     if u is None:
#         return redirect(url_for('.index'))
#     else:
#         created = created_topic(u.id)
#         replied = replied_topic(u.id)
#         return render_template(
#             'profile.html',
#             user=u,
#             created=created,
#             replied=replied
#         )
#
#
# @main.route('/user/<int:id>')
# def user_detail(id):
#     u = User.one(id=id)
#     if u is None:
#         abort(404)
#     else:
#         return render_template('profile.html', user=u)


@main.route('/image/add', methods=['POST'])
def avatar_add():
    file: FileStorage = request.files['avatar']
    suffix = file.filename.split('.')[-1]
    filename = str(uuid.uuid4())
    path = os.path.join('images', filename) + '.' + suffix
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}.{}'.format(filename, suffix))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # 防范目录遍历攻击
    return send_from_directory('images', filename)


