# Zulip bot for run jenkins job via trigger url
```
```
In this tutorial you'll learn how to deploy and configure this bot.

FYI https://zulipchat.com/api/

***

## Installing

#### Clone git repo
```bash
cd /opt
git clone https://github.com/rlagutinhub/zulip.jenkins-chatbot.git
cd zulip.jenkins-chatbot
```
#### Create python virtualenv
```bash
virtualenv --version
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

* zuliprc_file - full path to zuliprc file (if zulip with self-signed certificate then add ```insecure=true```).
* welcome_file - full path to welcome screen file at startup.
* logging_file - full path to log file.
* logging_format - format log message (see python3 logging).
* bot_name - list of names for this bot (not case sensitive).
* bot_email - email address for this bot into zulip (not case sensitive). Message from sender with this email address ignored.
* streams - list of subscribed zulip steams (not case sensitive). Bot only listens from subscribed stream (for private stream required manual subscribe).
* help_cmd - list of command names for get main help (not case sensitive).
* help_url - url to wiki with main help.
* deploy_cmd - list of command names for run job (not case sensitive).
* artifacts_cmd - list of command names for get exist artifacts job (not case sensitive).
* passwords_cmd - list of command names for get one-time password (not case sensitive).
* passwords_arg - list of arguments names for use one-time password at run job (not case sensitive). Run job required one-time password.
* passwords_access - list email addresses (not case sensitive) of zulip users who are allowed to receive one-time password (token).

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

#### Settings for Jenkins job without build parameters

> All settings are required.

* server_url - Jenkins URL.
* job_name - job name (not case sensitive and support whitespaces).
* url_token - token from job setting "trigger builds remotely".
* user_name - user name for auth when starting job.
* user_pass - user pass (API Token) for auth when starting job.
* streams - list of subscribed zulip steams (not case sensitive) that are allowed to access this job.
* artifacts - full path to script file for getting the list of artifacts this job (place into addons). 
* help_url - url to wiki with job help.
* param_list - this list empty for Jenkins job without build parameters!

```console
"server_url": "https://jenkins.dev.mta4.ru",
"job_name": "Test",
"url_token": "WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D8U",
"user_name": "admin",
"user_pass": "1198e32cfd40eb03a6ce993739d47d3774",
"streams": ["DevOps"],
"artifacts": "/opt/jenkins-chatbot/addons/test.sh",
"help_url": "https://github.com/zulip/zulip/",
"param_list": []
```
example generated url:
```
https://admin:11d6580708ab66c517577edc6d0319dee1@jenkins.dev.mta4.ru/job/test/build?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U
```

#### Settings for Jenkins job with build parameters

> All settings are required.

* server_url - Jenkins URL.
* job_name - job name (not case sensitive and support whitespaces).
* url_token - token from job setting "trigger builds remotely".
* user_name - user name for auth when starting job.
* user_pass - user pass (API Token) for auth when starting job.
* streams - list of subscribed zulip steams (not case sensitive) that are allowed to access this job.
* artifacts - full path to script file for getting the list of artifacts this job (place into addons). 
* help_url - url to wiki with job help.
* param_list - list of all paramers name (not case sensitive) for Jenkins job with build parameters!

```console
"server_url": "https://jenkins.dev.mta4.ru",
"job_name": "Test",
"url_token": "WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D8U",
"user_name": "admin",
"user_pass": "1198e32cfd40eb03a6ce993739d47d3774",
"streams": ["DevOps"],
"artifacts": "/opt/jenkins-chatbot/addons/test.sh",
"help_url": "https://github.com/zulip/zulip/",
"param_list": [
    "var1",
    "var2",
    "var3",
    "var4",
    "var5"
]
```
example generated url:
```
https://admin:11d6580708ab66c517577edc6d0319dee1@jenkins.dev.mta4.ru/job/test/buildWithParameters?token=WXL4VdN4hmIDScrPoYZnEJ2w5bdW0D7U&var1=1&var2=2&var3=3&var4=text&var5=true
```

## Manual start

```
/opt/zulip.jenkins-chatbot/env/bin/python3 /opt/zulip.jenkins-chatbot/bot.py --properties /opt/zulip.jenkins-chatbot/bot.properties
```

## Auto start (systemd)







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
