# -*- coding: utf-8 -*-
# @Time    : 2020/5/20 13:53
# @Author  : huangyl
# @FileName: sendEmail.py
# @Software: PyCharm
# @Blog    ：https://hardelm.com

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from readConfig import ReadConfig


class SendEmail():
    def __init__(self,sender_name,sender_pass):
        localReadConfig = ReadConfig()
        url = localReadConfig.get_url('url')
        self.ip = url.split('/')[2].split(':')[0]
        case_path = localReadConfig.get_path('case_path')
        self.case = case_path.split('/')[-1].split('.')[0]
        self.result_path = localReadConfig.get_path('result_path')
        self.sender_name = sender_name
        self.sender_pass = sender_pass

    def sendMail(self,receiver_name,result_name):

        try:
            result_file = self.result_path + result_name
            # 创建一个带附件的实例
            message = MIMEMultipart()
            message['From'] = formataddr(["Jenkins", self.sender_name])
            message['To'] = receiver_name
            subject = 'Jenkins测试邮件'
            message['Subject'] = subject

            # 邮件正文内容
            message.attach(MIMEText(self.ip + '服务器' + self.case + '模块测试结果,详见附件！', 'plain', 'utf-8'))

            msg_xlsx = MIMEText(open(result_file, 'rb').read(), 'base64', 'utf-8')
            msg_xlsx.add_header('Content-Disposition', 'attachment', filename=result_name)

            message.attach(msg_xlsx)

            server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
            server.login(self.sender_name, self.sender_pass)
            server.sendmail(self.sender_name, receiver_name.split(','), message.as_string())

            server.quit()
            ret = '测试结果发送成功！'
        except Exception as f:
            ret = '测试结果发送失败'
            print(f)
        return ret




