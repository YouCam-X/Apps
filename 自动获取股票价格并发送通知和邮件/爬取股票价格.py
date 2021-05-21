import os
from bs4 import BeautifulSoup
import requests
import time
from urllib.request import quote, unquote
from win10toast import ToastNotifier
import smtplib
from email.mime.text import MIMEText
import keyboard


def edit_data():

    global from_addr
    global to_addr
    global password
    global user_agent

    from_addr = input('请输入发送邮件的邮箱地址')
    to_addr = input('请输入接收邮件的邮箱地址')
    password = input('请输入授权码')
    user_agent = input('请在浏览器中复制User-Agent参数，贴到这里')

    data = [from_addr,to_addr,password,user_agent]

    file = open('config.txt','w')

    for i in data:
        file.write(i)
        file.write('\n')

    file.close()

def load_previous():

    global from_addr
    global to_addr
    global password
    global user_agent

    if os.path.isfile('config.txt'):
        file = open('config.txt','r')
        data = file.readlines()
    
        for i in data:
            from_addr = data[0].strip('\n')
            to_addr = data[1].strip('\n')
            password = data[2].strip('\n')
            user_agent = data[3].strip('\n')

        file.close()

    else:
        print('没有已存在的信息，请现在输入')

        from_addr = input('请输入发送邮件的邮箱地址')
        to_addr = input('请输入接收邮件的邮箱地址')
        password = input('请输入授权码')
        user_agent = input('请在浏览器中复制User-Agent参数，贴到这里')

        data = [from_addr,to_addr,password,user_agent]

        file = open('config.txt','w')
        for i in data:
            file.write(i)
            file.write('\n')

        file.close()

def sendemail():

    message = name + '\n' + str(price.text)
    msg = MIMEText(message)
    msg['Subject'] = '股票价格预警'
    msg['From'] = from_addr
    msg['To'] = to_addr
    stmp_server = 'smtp.qq.com'


    server = smtplib.SMTP_SSL(stmp_server,465,timeout = 2)
    server.login(from_addr,password)
    server.sendmail(from_addr,[to_addr],msg.as_string())
    server.quit()


def main():

    global name
    global price
    loop_number = 0

    print('''           欢迎来到股票通知系统''')
    name = input('请输入需要跟踪的股票名称\n')
    expectation = input('请输入此股票的预警价格，如>100，<50\n')

    number = expectation[1:]
    number_without_period = ''

    for i in number:

        if i == '.':
            continue

        else:
            number_without_period = number_without_period + i

    while not str.isdigit(number_without_period):

        print('价格输入有误，请重新输入')
        expectation = input('请输入预警价格，如>100，<50\n')
        number = expectation[1:]
        number_without_period = ''

        for i in number:

            if i == '.':
                continue

            else:
                number_without_period = number_without_period + i

    print('是否沿用上一次的邮箱地址和密码？是请按Enter键，重新设置请按Esc键。')

    while True:

        if keyboard.is_pressed('enter'):
            buffer = input('')
            load_previous()
            break

        elif keyboard.is_pressed('esc'):
            keyboard.wait('esc',True,True)
            edit_data()
            break

        else:
            continue

    encodedname = quote(name)

    url = 'https://www.baidu.com/s?wd='+ encodedname + '&rsv_spt=1&rsv_iqid=0xc84846ff00069f4b&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=10&rsv_sug1=10&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=4866&rsv_sug4=4866'

    headers = {
            'referer':'https://www.baidu.com/s?wd='+ encodedname + '&rsv_spt=1&rsv_iqid=0xc84846ff00069f4b&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=10&rsv_sug1=10&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=4866&rsv_sug4=4866',
            'user-agent':user_agent}


    while True:

        try:
            toaster = ToastNotifier()
            searchpage = requests.get(url,headers=headers)

            loop_number += 1

            soup = BeautifulSoup(searchpage.text,'html.parser')
            price = soup.find(srcid = '5432').find(class_= 'price_2jYb9')

            toaster.show_toast(name,price.text,icon_path = 'icon.ico')

            print('第%s次请求成功！'%(str(loop_number)))

            if expectation[0] == '>':
                if float(price.text) >= float(number):
            
                    try:
                        sendemail()
                        print('通知邮件已发送！')
                        break

                    except:
                        print('发送邮件失败')
                        break

            elif expectation[0] == '<':
                if float(price.text) <= float(number):

                    try:
                        sendemail()
                        print('通知邮件已发送！')
                        break

                    except:
                        print('发送邮件失败')
                        break

            time.sleep(60)

        except:
            loop_number += 1
            print('第%s次请求失败'%(str(loop_number)))
            continue

main()
press_enter = input('程序已执行完毕，按Enter键退出')