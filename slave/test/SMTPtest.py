import smtplib
from email.mime.text import MIMEText
from email.header import Header

msg = MIMEText('hello, send by Python. Again!', 'plain', 'utf-8')
msg['Subject'] = Header("Python Email Test", 'utf-8')

from_addr = "meiriqjfq@163.com"
password = "jfqmeiriq"
# 输入收件人地址:
to_addr = "380084818@qq.com"
# 输入SMTP服务器地址:
smtp_server = "smtp.163.com"


server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
