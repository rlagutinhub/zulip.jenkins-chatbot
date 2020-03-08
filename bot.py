#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# NAME:   JENKINS-CHATBOT/BOT.PY
# DESC:   ZULIP BOT FOR RUN JENKINS JOB VIA TRIGGER URL
# DATE:   08-03-2020
# LANG:   PYTHON 3
# AUTHOR: LAGUTIN R.A.
# EMAIL:  RLAGUTIN@MTA4.RU

# Examples:
#     /usr/bin/python3 bot.py -p <path-to-properties-file>

import os
import re
import sys
import json
import time
import zulip
import getopt
import logging


from libraries import Libraries as lib


properties = False
passwords = list()


class ZulipBot(object):

    def __init__(self):

        self.lib = lib()

        try:
            with open(properties, 'rt') as f:
                self.properties_load = f.read()

            self.properties_data = json.loads(self.properties_load)

        except:
            print('Error:', properties)
            sys.exit(1)

        try:
            with open(self.properties_data['welcome_file'], 'rt') as f:
                for welcome in f:
                    print(welcome, end='', flush=True)

        except:
            print('Error:', self.properties_data['welcome_file'])
            sys.exit(1)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        self.handler = logging.FileHandler(self.properties_data['logging_file'])
        self.handler.setLevel(logging.INFO)
        self.formatter = logging.Formatter(self.properties_data['logging_format'])
        self.handler.setFormatter(self.formatter)
        self.log.addHandler(self.handler)

        try:
            self.client = zulip.Client(config_file=self.properties_data['zuliprc_file'])
            self.client.get_server_settings() # check connect

        except:
            self.log.error('Exception:', exc_info=True)
            print('Error:', self.properties_data['zuliprc_file'])
            sys.exit(1)

        self.log.info('__init__({0})'.format(self))

        # self.subscribe_all()
        self.subscribe([x.lower() for x in self.properties_data['streams']])

    def subscribe_all(self):

        json = self.client.get_streams()["streams"]
        streams = [{"name": stream["name"]} for stream in json]
        self.client.add_subscriptions(streams)

    def subscribe(self, streams):

        for stream in streams:
            result = self.client.add_subscriptions(streams=[{'name': stream}])
            if (result['result']).lower() != 'success':
                self.log.error('subscribe({0})'.format(stream))

    def check_stream(self, streams, id_stream):

        json = self.client.get_streams()['streams']
        items = [{'id': stream['stream_id'], 'name': stream['name']} for stream in json if stream['name'].lower() in streams]
        for item in items:
            if item['id'] == id_stream:
                return True

        return False

    def send_msg(self, msg_type, msg_to=None, msg_topic=None, msg_content=None):

        try:
            if msg_type == 'stream': request = {'type': msg_type, 'to': msg_to, 'topic': msg_topic, 'content': msg_content}
            if msg_type == 'private': request = {'type': msg_type, 'to': msg_to, 'content': msg_content}
            if request: result = self.client.send_message(request)
            if result['result'] == 'success': self.log.info('send_msg({0})'.format(request)); return True
            if result['result'] != 'success': self.log.error('send_msg({0})'.format(request)); return False

        except (TypeError, ValueError, IndexError, KeyError):
            self.log.error('Exception:', exc_info=True)
            return False

    def get_content(self, msg, jobs):

        bot = None; job = None; args = None

        try:
            if msg.startswith(' '):
                pass

            elif msg.startswith('@'):

                pattern = re.compile(r'^@\*\*(.*?)\*\*')
                result = pattern.search(msg)

                if result:
                    bot = result.group()
                    msg = msg.replace(bot, '')
                    msg = msg.strip()

                if bot and msg:
                    for item in jobs:
                        if msg.lower().startswith(item) or msg.lower().startswith('\"' + item) or msg.lower().startswith('\'' + item):
                            pattern = re.compile(item, re.IGNORECASE)
                            msg = pattern.sub('', msg)
                            msg = msg.strip()
                            job = item
                            break

                    if not job:
                        job = msg.split()[0]
                        msg = msg.replace(job, '')
                        msg = msg.strip()
                        args = msg.split()

                    else:
                        args = msg.split()

            else:
                bot = str(msg.split()[0])
                msg = msg.replace(bot, '')
                msg = msg.strip()

                if bot and msg:
                    for item in jobs:
                        if msg.lower().startswith(item) or msg.lower().startswith('\"' + item) or msg.lower().startswith('\'' + item):
                            pattern = re.compile(item, re.IGNORECASE)
                            msg = pattern.sub('', msg)
                            msg = msg.strip()
                            job = item
                            break

                    if not job:
                        job = msg.split()[0]
                        msg = msg.replace(job, '')
                        msg = msg.strip()
                        args = msg.split()

                    else:
                        args = msg.split()

            if args:
                args_del = ['\"', '\'', '\'\'', '\"\"', '\"\'', '\'\"']
                args = [x for x in args if x not in args_del] 

        except (TypeError, ValueError, IndexError, KeyError):
            self.log.error('Exception:', exc_info=True)
            return False

        return {
            'bot': bot,
            'job': job,
            'args': args
            }

    def process(self, msg):

        global passwords

        process_head = dict()
        process_body = dict()

        try:
            process_head['type'] = msg['type']

            if type(process_head['type']) == str and process_head['type'].lower() == 'stream':
                process_head['sender_id'] = msg['sender_id']
                process_head['sender_email'] = msg['sender_email']
                process_head['sender_short_name'] = msg['sender_short_name']
                process_head['sender_full_name'] = msg['sender_full_name']
                process_head['stream_id'] = msg['stream_id']
                process_head['stream_name'] = msg['display_recipient']
                process_head['subject'] = msg['subject']

            if type(process_head['type']) == str and process_head['type'].lower() == 'private':
                return

        except (KeyError, ValueError):
            self.log.error('Exception:', exc_info=True)
            return

        if type(process_head['sender_email']) == str and process_head['sender_email'].lower() == self.properties_data['bot_email'].lower():
            return

        if not self.check_stream([x.lower() for x in self.properties_data['streams']], process_head['stream_id']):
            return

        process_body = self.get_content(msg["content"], [x.lower() for x in [job['job_name'] for job in self.properties_data['jobs']]])      

        if not process_body:
            return

        # print(json.dumps(msg, indent=4))
        # print(json.dumps(self.client.get_members(), indent=4))
        # print(json.dumps(self.client.list_subscriptions(), indent=4))

        process_bot = process_body['bot']

        if not process_bot or process_bot.lower() not in [x.lower() for x in self.properties_data['bot_name']]:

            # if list(set(process_body['content']) & set(self.properties_data['bot_name'])):
            #     message = "[" + process_bot + "]" + "(" + self.properties_data['help_url'] + ")" + " : ** Hey there!** :blush:"
            #     self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)
            #     return

            return

        else:
            self.log.info('process({0} {1}))'.format(process_head, process_body))

            job_name = process_body['job']
            process_arg = process_body['args']

            if not job_name or type(job_name) == str and job_name.lower() in [x.lower() for x in self.properties_data['help_cmd']]:

                message = "[" + process_bot + "]" + "(" + self.properties_data['help_url'] + ")" + " : ** Help SUCCESS** :check_mark:"

                message += '\n'
                message += '```bash' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [help] - help' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [token] - get otp token' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [job] [help] - help job' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [job] [artifacts] - get job artifacts' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [job] [deploy] [token=xxxxxxxxxxxxx] - Build job (required token)' + '\n'
                message += '[jenkins|evgeny|евгений|@**jenkins bot**] [job] [deploy] [token=xxxxxxxxxxxxx] [var_1=val_1] [var_2=val_2] [var_N=val_N] - Build job with parameters (required token)' + '\n'
                message += '```'
                message += '\n'
                message += '>'
                message += '*, where job:* '

                jobs_items = [{'job_name': job['job_name'], 'help_url': job['help_url']} for job in self.properties_data['jobs']]

                for job_item in jobs_items:
                    message += '*[' + job_item['job_name'] + ']' + '(' +  job_item['help_url'] + ')*' + ' '

                self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)
                return

            if type(job_name) == str and job_name.lower() in [x.lower() for x in self.properties_data['passwords_cmd']]:

                message_success = "**Token: **" + "[" + process_head['sender_full_name'] + "]" + "(" + process_head['sender_email'] + ")" + " : ** Send PM SUCCESS** :check_mark:"
                message_failure = "**Token: **" + "[" + process_head['sender_full_name'] + "]" + "(" + process_head['sender_email'] + ")" + " : ** Send PM FAILURE** :x:"
                message_aborted = "**Token: **" + "[" + process_head['sender_full_name'] + "]" + "(" + process_head['sender_email'] + ")" + " : ** Not access ABORTED** :x:"

                if process_head['sender_email'].lower() in [x.lower() for x in self.properties_data['passwords_access']]:

                    job_pass = self.lib.gen_passwd()
                    passwords.append(job_pass)

                    message = message_success
                    message_pm = "**Token: **" + job_pass
                    process_type_pm = 'private'

                    self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)
                    self.send_msg(msg_type=process_type_pm, msg_to=process_head['sender_email'], msg_content=message_pm)

                else:
                    message = message_aborted
                    self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)

                return

            job_count = 0

            for properties_item in self.properties_data['jobs']:

                if type(job_name) == str and job_name.lower() == properties_item['job_name'].lower():

                    job_count += 1

                    job_cmd = process_arg[0] if len(process_arg) > 0 else False
                    job_url = properties_item['server_url'] + '/job/' + properties_item['job_name'] + '/'

                    if not self.check_stream([x.lower() for x in properties_item['streams']], process_head['stream_id']):
                        message = "**Project: **" + "[" + job_name + "]" + "(" + job_url + ")" + " : ** Not access ABORTED** :x:"
                        self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)
                        break

                    if job_cmd:
                        job_cmd = job_cmd.replace('\"', '')
                        job_cmd = job_cmd.replace('\'', '')

                    if type(job_cmd) == str and job_cmd.lower() in [x.lower() for x in self.properties_data['deploy_cmd']]:

                        process_url_check = True
                        process_password_check = False

                        process_build = 'buildWithParameters' if properties_item['param_list'] else 'build'
                        process_url = properties_item['server_url'] + '/job/' + properties_item['job_name'] + '/' + process_build + '?token=' + properties_item['url_token']

                        if process_build == 'build':

                            for process_param in process_arg[1:]:

                                try:
                                    process_param = process_param.replace('\"', '')
                                    process_param = process_param.replace('\'', '')

                                    param_var = process_param.split('=')[0]
                                    param_val = process_param.split('=')[1]

                                    if type(param_var) == str and param_var.lower() in [x.lower() for x in self.properties_data['passwords_arg']]:
                                        if param_val in passwords:
                                            passwords.remove(param_val)
                                            process_password_check = True

                                except (IndexError, ValueError):
                                    self.log.error('Exception:', exc_info=True)
                                    break

                        if process_build == 'buildWithParameters':

                            process_param_col = list()

                            for process_param in process_arg[1:]:

                                try:
                                    process_param = process_param.replace('\"', '')
                                    process_param = process_param.replace('\'', '')

                                    param_var = process_param.split('=')[0]
                                    param_val = process_param.split('=')[1]

                                    if type(param_var) == str and param_var.lower() in [x.lower() for x in self.properties_data['passwords_arg']]:
                                        if param_val in passwords:
                                            passwords.remove(param_val)
                                            process_password_check = True

                                    elif type(param_var) == str and param_var.lower() not in [x.lower() for x in self.properties_data['passwords_arg']]:
                                        if param_var.lower() in [x.lower() for x in properties_item['param_list']]:
                                            process_param_col.append(process_param)

                                        else:
                                            break

                                except (IndexError, ValueError):
                                    self.log.error('Exception:', exc_info=True)
                                    break

                            if not process_param_col:
                                process_url_check = False

                            else:
                                if len(process_param_col) == len (properties_item['param_list']) and len(set(process_param_col)) == len(process_param_col):
                                    s = '&'; process_params_arg = s + s.join(process_param_col); process_param_col.clear()
                                    process_url = process_url + process_params_arg

                                else:
                                    process_url_check = False

                        message_success = "**Project: **" + "[" + job_name + "]" + "(" + job_url + ")" + " : ** Start SUCCESS** :check_mark:"
                        message_failure = "**Project: **" + "[" + job_name + "]" + "(" + job_url + ")" + " : ** Start FAILURE** :x:"

                        if process_url_check and process_password_check:
                            message = message_success if self.lib.run_job(url=process_url, method='POST', username=properties_item['user_name'], password=properties_item['user_pass']) else message_failure

                        else:
                            message = message_failure

                        self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)

                    elif type(job_cmd) == str and job_cmd.lower() in [x.lower() for x in self.properties_data['artifacts_cmd']]:

                        message_success = "**Project: **" + "[" + job_name + "]" + "(" + job_url + ")" + " : ** Artifacts SUCCESS** :check_mark:"
                        message_aborted = "**Project: **" + "[" + job_name + "]" + "(" + job_url + ")" + " : ** Artifacts ABORTED** :x:"

                        artifacts_scrpath = properties_item['artifacts']
                        if os.path.exists(artifacts_scrpath) and os.path.isfile(artifacts_scrpath):
                            os.chmod(artifacts_scrpath, 0o755)
                            cmd_str = artifacts_scrpath
                            cmd = cmd_str.split()
                            run_cmd_res = self.lib.run_cmd(cmd, False)
                            message = '\n'.join(run_cmd_res['stdout'])
                            message = message_success + "\n" + message

                        else:
                            message = message_aborted

                        self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)

                    else:
                        message = "**Project: **" + "[" + job_name + "]" + "(" + properties_item['help_url'] + ")" + " : ** Help SUCCESS** :check_mark:"
                        self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)

                    break

            if job_count == 0:
                message = "**Project: **" + "~~" +  job_name + "~~" +  " : ** Not found ABORTED** :x:"
                self.send_msg(msg_type=process_head['type'], msg_to=process_head['stream_name'], msg_topic=process_head['subject'], msg_content=message)


def main():

    global properties

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:', ['properties='])

    except getopt.GetoptError:
        pass

    try:
        for opt, arg in opts:
            if opt in ('-p', '--properties'):
                if os.path.isfile(arg):
                    properties = arg

    except NameError:
        pass

    if not properties:
        print('./bot.py -p <path-to-properties-file>')
        sys.exit(1)

    try:
        bot = ZulipBot()
        bot.client.call_on_each_message(bot.process)

    except OSError as e:
        print('Error:', e)
        sys.exit(1)


if __name__ == '__main__':

    try:
        main()

    except KeyboardInterrupt:
        sys.exit(0)
