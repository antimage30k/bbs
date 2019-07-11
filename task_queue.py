from celery import Celery

from models.message import mailer

celery = Celery('tasks', backend='redis://localhost', broker='redis://localhost')


# 消息队列保证邮件投递
@celery.task(bind=True)
def send_mail_async(self, subject, author, to, content):
    # 有了 bind 才能去拿到 self 参数
    # 这样才能去通过 self 调用当前 task 的一些功能
    # 比如重试
    try:
        m = mailer.new(
            subject=subject,
            author=author,
            to=to,
        )
        m.plain = content
        mailer.send(m)
    except Exception as exc:
        # 3秒重试一次 最多重试5次
        raise self.retry(exc=exc, countdown=3, max_retries=5)
    # m = mailer.new(
    #     subject=subject,
    #     author=author,
    #     to=to,
    # )
    # m.plain = content
    #
    # mailer.send(m)
    