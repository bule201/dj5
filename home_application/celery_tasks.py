# -*- coding: utf-8 -*-
"""
celery 任务示例

本地启动celery命令: python  manage.py  celery  worker  --settings=settings
周期性任务还需要启动celery调度命令：python  manage.py  celerybeat --settings=settings
"""
import datetime

from celery import task
from celery.schedules import crontab
from celery.task import periodic_task

from common.log import logger
import smtplib
from email.mime.text import MIMEText
from email.header import Header

@periodic_task(run_every=crontab(minute='55', hour='13',day_of_month='31', month_of_year='3'))
def time_task():
    """
    定义一个 celery 定时任务
    """
    now = datetime.datetime.now()
    logger.error(u"celery 定时任务执行成功，当前时间：{}".format(now))
    time_send_mail()



@periodic_task(run_every=crontab(minute='*/5', hour='*', day_of_week="*"))
def get_time():
    """
    celery 周期任务示例

    run_every=crontab(minute='*/5', hour='*', day_of_week="*")：每 5 分钟执行一次任务
    periodic_task：程序运行时自动触发周期任务
    """
    periodic_send_mail()
    now = datetime.datetime.now()
    logger.error(u"celery 周期任务调用成功，当前时间：{}".format(now))



def periodic_send_mail():
    sender = 'from@runoob.com'
    receivers = ['bule201@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('辛苦了，继续加油！', 'plain', 'utf-8')
    message['From'] = Header("郁蓝", 'utf-8')
    message['To'] = Header("郁蓝", 'utf-8')

    subject = 'djcelery 周期任务'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"

def time_send_mail():
    sender = 'from@runoob.com'
    receivers = ['bule201@126.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText('半小时后将开始蓝鲸直播课程。', 'plain', 'utf-8')
    message['From'] = Header("郁蓝", 'utf-8')
    message['To'] = Header("郁蓝", 'utf-8')

    subject = 'djcelery 定时任务'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print "邮件发送成功"
    except smtplib.SMTPException:
        print "Error: 无法发送邮件"