from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board

main = Blueprint('topic', __name__)


@main.route("/")
@admin_required
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)
    token = new_csrf_token()
    bs = Board.all()
    return render_template("topic/index.html", ms=ms, bs=bs, bid=board_id, token=token)


@main.route('/<int:id>')
def detail(id):
    u = current_user()
    # Topic.get 增加一次点击阅读计数
    m = Topic.get(id)
    latest = Topic.all_creat_time_desc()
    # 传递 topic 的所有 reply 到 页面中
    return render_template("topic/detail.html", topic=m, current_user=u, latest_topics=latest)


@main.route("/delete")
@csrf_required
def delete():
    id = int(request.args.get('id'))
    u = current_user()
    # print('删除 topic 用户是', u, id)
    Topic.delete(id)
    return redirect(url_for('.index'))


@main.route("/new")
def new():
    board_id = int(request.args.get('board_id'))
    bs = Board.all()
    # return render_template("topic/new.html", bs=bs, bid=board_id)
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, bid=board_id, token=token)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    t = Topic.new(form, user_id=u.id)
    return redirect(url_for('topic.detail', id=t.id))


@main.route("/edit/<int:id>", methods=['GET', 'POST'])
@admin_required
@csrf_required
def edit(id):
    # GET方法访问则返回修改文章的页面
    if request.method == 'GET':
        token = new_csrf_token()
        topic = Topic.one(id=id)
        return render_template("topic/edit.html", topic=topic, token=token)
    # POST方法访问则根据发送的form更新topic内容
    if request.method == 'POST':
        content = request.form['content']
        Topic.update(id, content=content)
        return redirect(url_for("topic.detail", id=id))
