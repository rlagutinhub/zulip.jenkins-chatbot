# Zulip bot for run jenkins job via trigger url
```
```
In this tutorial you'll learn how to deploy and configure this bot.

FYI https://zulipchat.com/api/

***

## Installing

> Required packages python3x, python3x-pip and virtualenv (pypi).

#### Clone git repo
```bash
cd /opt
git clone https://github.com/rlagutinhub/zulip.jenkins-chatbot.git
cd zulip.jenkins-chatbot
```
#### Create python virtualenv
```bash
virtualenv env
```
#### Activate python virtualenv
```bash
source env/bin/activate
```
#### Install latest zulip package into virtualenv
```bash
pip3 install -U zulip
```
#### List installed packages into virtualenv
```bash
pip3 list

Package       Version
------------- ----------
certifi       2019.11.28
cffi          1.14.0
chardet       3.0.4
cryptography  2.8
distro        1.4.0
idna          2.8
matrix-client 0.3.2
pip           19.1.1
pycparser     2.20
pyOpenSSL     19.1.0
requests      2.21.0
setuptools    43.0.0
six           1.14.0
typing        3.7.4.1
urllib3       1.24.3
wheel         0.33.6
zulip         0.6.3
```
#### Deactivate python virtualenv
```bash
deactivate
```

## Properties

```vim zulip.jenkins-chatbot/bot.properties```

#### Main settings

> All settings are required.

* `zuliprc_file` - full path to zuliprc file (if zulip with self-signed certificate then add `insecure=true`).
* `welcome_file` - full path to welcome screen file at startup.
* `logging_file` - full path to log file.
* `logging_format` - format log message (see python3 logging).
* `bot_name` - list of names for this bot (not case sensitive).
* `bot_email` - email address for this bot into zulip (not case sensitive). Message from sender with this email address ignored.
* `streams` - list of subscribed zulip steams (not case sensitive). Bot only listens from subscribed stream (for private stream required manual subscribe).
* `help_cmd` - list of command names for get main help (not case sensitive).
* `help_url` - url to wiki with main help.
* `deploy_cmd` - list of command names for run job (not case sensitive).
* `artifacts_cmd` - list of command names for get exist artifacts job (not case sensitive).
* `passwords_cmd` - list of command names for get one-time password (not case sensitive).
* `passwords_arg` - list of arguments names for use one-time password at run job (not case sensitive). Run job required one-time password.
* `passwords_access` - list email addresses (not case sensitive) of zulip users who are allowed to receive one-time password (token).

```console
"zuliprc_file": "/opt/zulip.jenkins-chatbot/bot.zuliprc",
"welcome_file": "/opt/zulip.jenkins-chatbot/bot.welcome",
"logging_file": "/opt/zulip.jenkins-chatbot/bot.log",
"logging_format": "%(asctime)s - %(levelname)s - %(message)s",
"bot_name": ["jenkins", "evgeny", "евгений", "@**jenkins bot**"],
"bot_email": "jenkins-bot@msg.dev.mta4.ru",
"streams": ["DevOps", "core team", "general", "test"],
"help_cmd": ["help", "man", "manual", "readme", "помощь", "хелп", "мануал", "ман"],
"help_url": "https://zulipchat.com/",
"deploy_cmd": ["deploy", "build", "start", "run", "билд", "пуск", "запуск", "запустить", "старт", "сборка", "собрать"],
"artifacts_cmd": ["artifacts", "artifact", "components", "component", "артефакты", "артефакт", "компоненты", "компонент"],
"passwords_cmd": ["token", "токен"],
"passwords_arg": ["token", "токен"],
"passwords_access": [
    "user1@mta4.ru",
    "user2@mta4.ru",
    "user3@mta4.ru"
]
```

#### Settings for Jenkins job without build parameters

> All settings are required.

* `server_url` - Jenkins URL.
* `job_name` - job name (not case sensitive and support whitespaces).
* `url_token` - token from job setting "trigger builds remotely".
* `user_name` - user name for auth when starting job.
* `user_pass` - user pass (API Token) for auth when starting job.
* `streams` - list of subscribed zulip steams (not case sensitive) that are allowed to access this job.
* `artifacts` - full path to script file for getting the list of artifacts this job (place into addons). 
* `help_url` - url to wiki with job help.
* `param_list` - this list empty for Jenkins job without build parameters!

```console
"server_url": "https://jenkins.dev.mta4.ru",
"job_name": "Test",
"url_token": "WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U",
"user_name": "admin",
"user_pass": "1198e32cfd40eb03a6ce993739d47d3774",
"streams": ["DevOps"],
"artifacts": "/opt/zulip.jenkins-chatbot/addons/test.sh",
"help_url": "https://github.com/zulip/zulip/",
"param_list": []
```
example generated trigger url for run job:
```console
https://admin:1198e32cfd40eb03a6ce993739d47d3774@jenkins.dev.mta4.ru/job/test/build?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U
```

#### Settings for Jenkins job with build parameters

> All settings are required.

* `server_url` - Jenkins URL.
* `job_name` - job name (not case sensitive and support whitespaces).
* `url_token` - token from job setting "trigger builds remotely".
* `user_name` - user name for auth when starting job.
* `user_pass` - user pass (API Token) for auth when starting job.
* `streams` - list of subscribed zulip steams (not case sensitive) that are allowed to access this job.
* `artifacts` - full path to script file for getting the list of artifacts this job (place into addons). 
* `help_url` - url to wiki with job help.
* `param_list` - list of all paramers name (not case sensitive) for Jenkins job with build parameters!

```console
"server_url": "https://jenkins.dev.mta4.ru",
"job_name": "Test",
"url_token": "WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U",
"user_name": "admin",
"user_pass": "1198e32cfd40eb03a6ce993739d47d3774",
"streams": ["DevOps"],
"artifacts": "/opt/zulip.jenkins-chatbot/addons/test.sh",
"help_url": "https://github.com/zulip/zulip/",
"param_list": [
    "var1",
    "var2",
    "var3",
    "var4",
    "var5"
]
```
example generated trigger url for run job:
```console
https://admin:1198e32cfd40eb03a6ce993739d47d3774@jenkins.dev.mta4.ru/job/test/buildWithParameters?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U&var1=1&var2=2&var3=3&var4=text&var5=true
```

## Manual start

```bash
/opt/zulip.jenkins-chatbot/env/bin/python3 /opt/zulip.jenkins-chatbot/bot.py --properties /opt/zulip.jenkins-chatbot/bot.properties
```

## Auto start (systemd)

> Restart every 60 seconds if  failure the service (for example zulip server not running).

```bash
cat <<EOF > /etc/systemd/system/zulip.jenkins-chatbot.service
[Unit]
Description=Zulip Jenkins-chatbot
Documentation=https://zulipchat.com/api/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
Restart=on-failure
RestartSec=60s
ExecStart=/opt/zulip.jenkins-chatbot/env/bin/python3 /opt/zulip.jenkins-chatbot/bot.py --properties /opt/zulip.jenkins-chatbot/bot.properties

[Install]
WantedBy=multi-user.target
EOF
```
```bash
systemctl daemon-reload

systemctl enable zulip.jenkins-chatbot.service
systemctl start zulip.jenkins-chatbot.service
systemctl status zulip.jenkins-chatbot.service

# systemctl start zulip.jenkins-chatbot.service
# systemctl stop zulip.jenkins-chatbot.service
# systemctl restart zulip.jenkins-chatbot.service

journalctl --full -b 0 -u zulip.jenkins-chatbot.service --follow
tail -f /opt/zulip.jenkins-chatbot/bot.log
```
***
## Bot settings

![alt text](https://raw.githubusercontent.com/rlagutinhub/zulip.jenkins-chatbot/master/screen.png)

***
## Result

![alt text](https://raw.githubusercontent.com/rlagutinhub/zulip.jenkins-chatbot/master/screen1.png)
![alt text](https://raw.githubusercontent.com/rlagutinhub/zulip.jenkins-chatbot/master/screen2.png)

## Back answer from jenkins
___
* ZulipChat.com [zulip-plugin](https://zulipchat.com/integrations/doc/jenkins)
* GitHub [zulip-plugin](https://github.com/jenkinsci/zulip-plugin/blob/master/README.markdown)
