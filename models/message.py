from time import sleep

from marrow.mailer import Mailer
from sqlalchemy import Column, Unicode, UnicodeText, Integer

from config import admin_mail
import secret
from models.base_model import SQLMixin, db
from models.user import User
# from tasks import send_async, mailer

def configured_mailer():
    config = {
        # 'manager.use': 'futures',
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    m = Mailer(config)
    m.start()
    return m


mailer = configured_mailer()


def send_mail(subject, author, to, content):
    m = mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content

    mailer.send(m)
    # sleep(30)


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Messages.new(form)

        receiver: User = User.one(id=receiver_id)
        send_mail(
            subject=title,
            author=admin_mail,
            to=receiver.email,
            content='站内信通知：\n {}'.format(content),
        )
        import threading
        # form = dict(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content'],
        # )
        # t = threading.Thread(target=_send_mail, kwargs=form)
        # t.start()
        #
        # m = mailer.new(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        # )
        # m.plain = form['content']
        #
        # mailer.send(m)
        # sleep(30)
        # send_async.delay(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content']
        # )

    def sender(self):
        s = User.one(id=self.sender_id)
        return s

    def receiver(self):
        r = User.one(id=self.receiver_id)
        return r
