#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: sample
    Desc : 电子邮件
    简单邮件传输协议：SMTP 端口25
    一些已经实现了SMTP的著名MTA（消息传输代理）包括：
    1，Sendmail
    2，Postfix
    3，Exim
    4，qmail
    商业的有：
    1，Microsoft Exchange
    2，Lotus Notes Domino Mail Server

    用于下载邮局的协议：
    1，邮局协议POP3
    2，交互式邮件访问协议IMAP，Exchange使用的就是这个

    MUA，邮件用户代理，利用SMTP发送邮局，利用POP3或IMAP4下载邮局
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio

__author__ = 'Xiong Neng'

def multipart():
    sender = 'jon@nodgg.network'
    receiver = 'dave@gmail.com'
    subject = 'Faders up'
    body = 'I never should have moved out of Texsa. -J.\n'
    audio = 'kiss.mp3'

    m = MIMEMultipart()
    m['from'] = sender
    m['to'] = receiver
    m['subject'] = subject

    m.attach(MIMEText(body))
    apart = MIMEAudio(open(audio, 'rb').read(), 'mpeg')
    apart.add_header('Content-Disposition', 'attachment', filename=audio)
    m.attach(apart)

    s = smtplib.SMTP()
    s.connect(sender, [receiver], m.as_string())
    s.close()



if __name__ == '__main__':
    print('aaa\nbbb')


