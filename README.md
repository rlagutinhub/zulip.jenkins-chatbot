# Zulip bot for run jenkins job via trigger url
```
```
In this tutorial you'll learn how to deploy and configure this bot.

FYI https://zulipchat.com/api/

***

## Install

### Clone git repo
```bash
cd /opt
git clone https://github.com/rlagutinhub/zulip.jenkins-chatbot.git
cd zulip.jenkins-chatbot
```
### Create python virtualenv
```bash
virtualenv --version
virtualenv env
```
### Activate python virtualenv
```bash
source env/bin/activate
```
### Install latest zulip package into virtualenv
```bash
pip3 install -U zulip
```
### List installed packages into virtualenv
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
### Deactivate python virtualenv
```bash
deactivate
```

## Properties

```vim zulip.jenkins-chatbot/bot.properties```

* Main settings

> zuliprc_file - full path to zuliprc file (if zulip with self-signed certificate then add ```insecure=true```)
> welcome_file - full path to welcome screen file at startup
> logging_file - full path to log file
> logging_format - format log message (see python3 logging)
> bot_name - list bot names

```console
"zuliprc_file": "/opt/jenkins-chatbot/bot.zuliprc",
"welcome_file": "/opt/jenkins-chatbot/bot.welcome",
"logging_file": "/opt/jenkins-chatbot/bot.log",
"logging_format": "%(asctime)s - %(levelname)s - %(message)s",
"bot_name": ["jenkins", "evgeny", "евгений", "@**jenkins bot**"],
"bot_email": "jenkins-bot@msg.dev.mta4.ru",
"streams": ["DevOps", "core team", "general", "test"],
"help_cmd": ["help", "man", "manual", "помощь", "хелп", "мануал", "ман"],
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

* Job settings

> Use only strong password 12-14 symbols [wiki](https://en.wikipedia.org/wiki/Password_strength)

```console
[Security]
keys=sec
sec.username=weblogic
sec.password=welcome1
```

***

https://zulipchat.com/api/deploying-bots

yum install python34 python34-devel python34-pip
yum install libffi-devel # resolve err pip install - error: command 'gcc' failed with exit status 1
pip3 install -U virtualenv
cd /opt/jenkins-chatbot/
virtualenv env
source env/bin/activate # <<<
pip3 install -U zulip

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
pycparser     2.19
pyOpenSSL     19.1.0
requests      2.21.0
setuptools    43.0.0
six           1.14.0
typing        3.7.4.1
urllib3       1.24.3
wheel         0.33.6
zulip         0.6.3

deactivate # <<<

# Zulip bot start auto
apt update supervisor
apt install supervisor

vim /etc/supervisor/conf.d/jenkins-chatbot.conf
[program:jenkins-chatbot]
command=/opt/jenkins-chatbot/env/bin/python3 /opt/jenkins-chatbot/bot.py --properties /opt/jenkins-chatbot/bot.properties
startsecs=3
stdout_logfile=/var/log/jenkins-chatbot.log
redirect_stderr=true

supervisorctl update all
supervisorctl reread all
supervisorctl status all
supervisorctl start all
supervisorctl stop all
supervisorctl restart all

# Zulip bot start manual
/opt/jenkins-chatbot/env/bin/python3 /opt/jenkins-chatbot/bot.py --properties /opt/jenkins-chatbot/bot.properties

# Run job Jenkins via curl
curl -k https://admin:11d6580708ab66c517577edc6d0319dee1@jenkins.dev.mta4.ru/job/test1/build?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U
curl -k -X POST "https://admin:11d6580708ab66c517577edc6d0319dee1@jenkins.dev.mta4.ru/job/test1/buildWithParameters?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U&test_var=test"

# Run job Jenkins via bot
evgeny
evgeny help
evgeny token
evgeny test1 artifacts
evgeny test1 deploy token=2u4FTEY0uhUZ79 var1="1" var2="2" var3="3" var4="1" var5="true"
evgeny token
evgeny test2 artifacts
evgeny test2 deploy token=2u4FTEY0uhUZ70
