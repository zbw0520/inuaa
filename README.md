# i南航自动打卡小工具

## Description

自动进行每天i南航校内打卡，并且邮件通知，可以多人打卡鸭

**免责声明: 此项目只可以用于技术学习讨论，请勿用于实际用于打卡，如果出现信息错误等后果概不负责**

有问题欢迎提出issue~

如果感觉有用请给个⭐吧，秋梨膏

## Usage

### Step 0

安装Python3、Python3-pip、git、vim和screen，安装requests库

如果没有安装，请及时下载安装

如使用Yum安装包管理器，可以使用如下命令
``` sh
sudo yum install python3 python3-pip git screen vim -y
```
然后使用pip3安装requests库
``` sh
sudo pip3 install requests
```

### Step 1

下载本项目，可以git clone或Download Zip

例如
``` sh
git clone https://github.com/zombie12138/inuaa --depth=1
```

### Step 2

配置`config.json`

``` sh
cd inuaa
vim config.json
```

然后使用vim编辑`config.json`

|  KEY   | 作用  |
|  ----  | ----  |
| mail_username  | 使用该邮件地址发送邮件提醒，如果不需要发邮件无则填空 |
| mail_password  | 邮件smtp的密码，不同于邮箱密码，请登录邮箱进行设置 |
|  users  |  收件人列表，可以一人或多人  |
|  name  |  收件人名称，可以写昵称，随便写  |
|  student_id  |  打卡学生的学生id  |
|  student_password  | 打卡学生教务密码  |
|  receiver_mail  | 打卡学生的收信箱，用于接收打卡提示  |

建议使用QQ邮箱向QQ邮箱发送。

**举个🌰**

``` json
{
    "mail_username": "123456@qq.com",
    "mail_password": "qwertyuiopasdfgh",
    "smtp_host": "smtp.qq.com",
    "users": [
        {
            "name": "张三",
            "student_id": "011710101",
            "student_password": "St123456",
            "receiver_mail": "wuzii@qq.com"
        },
        {
            "name": "Tony",
            "student_id": "011710102",
            "student_password": "St123456",
            "receiver_mail": "jackeylove@qq.com"
        }
    ]
}
```

## Step 3

新建screen，后台运行程序

``` bash
screen -S inuaa
python3 sign.py
```

之后只要主机一直开机就会每天打卡辣。

如果想要查看输出信息可以 `screen -r inuaa`查看，快捷键`Ctrl+A+D`退出Screen(仍在后台运行)
