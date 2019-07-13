import json
import uuid
from functools import wraps

from flask import session, request, abort, render_template

from models.user import User

# 导入redis
import redis

# 初始化 csrf_token 数据库
csrf_tokens = redis.StrictRedis()
cache = redis.StrictRedis()


def current_user():
    # 使用 redis 缓存高频使用的 current_user
    uid = session.get('user_id', -1)
    k = 'current_user_{}'.format(uid)
    if cache.exists(k):
        v = cache.get(k)
        u_data = json.loads(v)
        # 转化成对象再返回
        u = User()
        u.__dict__.update(u_data)
        return u
    else:
        u = User.one(id=uid)
        if u is None:
            return None
        else:
            v = json.dumps(u.json())
            cache.set(k, v)
            return u
    # session_id = request.cookies.get('session_id')
    # print('session_id', session_id)
    # if session_id is not None:
    #     # 注意要转换成int
    #     # 其实可以不转换，one方法用sql语句的时候会自动转换bytes到str
    #     # 但应该转换，数据应该是我们想要的数据，而不是等着别的地方去处理
    #     # 这样，换了api也能用
    #     uid = int(session_redis.get(session_id))
    #     u = User.one(id=uid)
    #     return u
    # else:
    #     return None


def login_required(f):
    @wraps(f)
    def func():
        u = current_user()
        if u is None:
            return render_template('login.html')
        else:
            return f()
    return func


def admin_required(route_function):
    @wraps(route_function)
    def func():
        u = current_user()
        if u.username == 'admin':
            return route_function()
        else:
            return render_template('login.html')
    return func


def csrf_required(f):
    # @wraps(f)
    # def wrapper(*args, **kwargs):
    #     token = request.args['token']
    #     u = current_user()
    #     if token in csrf_tokens and csrf_tokens[token] == u.id:
    #         csrf_tokens.pop(token)
    #         return f(*args, **kwargs)
    #     else:
    #         abort(401)
    #
    # return wrapper

    # redis version
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        # get 得到的会是一个bytes类型，转化成整形
        if csrf_tokens.exists(token) and int(csrf_tokens.get(token)) == u.id:
            csrf_tokens.delete(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    # u = current_user()
    # token = str(uuid.uuid4())
    # csrf_tokens[token] = u.id
    # return token

    # redis version
    u = current_user()
    # 以uuid随机字符串为key，以user id为value
    token = str(uuid.uuid4())
    csrf_tokens.set(token, u.id)
    # 设置10小时后失效
    csrf_tokens.expire(token, 36000)
    # print('new_csrf_token', type(csrf_tokens.get(token)), csrf_tokens.get(token))
    return token
