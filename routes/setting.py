from flask import (
    render_template,
    request,
    Blueprint,
    redirect, url_for)
from models.user import User
from routes import current_user, csrf_required, new_csrf_token

main = Blueprint('setting', __name__)


# setting 路由函数
@main.route("/")
def index():
    # 获取当前用户和form表单，交给change 函数处理
    # 如果是GET请求则不会处理，而是返回setting页面
    u = current_user()
    token = new_csrf_token()
    return render_template('setting.html', user=u, token=token)


@main.route("/update", methods=['POST'])
@csrf_required
def update():
    u = current_user()
    form = request.form.to_dict()
    print('form', form)
    change(u, form)
    return redirect(url_for('.index'))


# 处理setting的函数
def change(u, form):
    # 如果修改密码，需要验证输入的旧密码是否正确
    if form['action'] == 'change_password':
        old_pw = form['old_pass']
        if u.password == User.salted_password(old_pw):
            form['password'] = User.salted_password(form['new_pass'])
            # 移除old_pass 和new_pass 字段
            form.pop('old_pass')
            form.pop('new_pass')
    else:
        # 如果不是修改密码，
        # 需要小心signature如果不输入的话是空的，这种情况下应该去除signature字段
        if form['signature'] == '':
            form.pop('signature')
    # 去除form 表单里的action字段
    form.pop('action')
    # 更新用户信息
    User.update(id=u.id, **form)
