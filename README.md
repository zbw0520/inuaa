# i南航自动打卡小工具

----

## 快速上手

1. 安装python3
2. `sudo pip3 install requests`
3. 修改`sign.py`中的密码和id
4. 修改`sign.py`，配置邮箱账号和密码，用于发送提醒（注意要使用smtp的密码，需要登陆邮箱进行设置，如果不需要可以不设置）
5. `screen -S inuaa`，并且运行`python3 sign.py`
