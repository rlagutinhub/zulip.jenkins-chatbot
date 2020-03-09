#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import ssl
import sys
import json
import time
import base64
import math
import random 
# import psutil
import subprocess


from urllib.request import Request, urlopen
from urllib.error import URLError


INSECURE_CONTEXT = ssl._create_unverified_context()


class Libraries(object):

    @staticmethod
    def run_job(url, method=None, data=None, token=None, username=None, password=None):

        if data:
            params = json.dumps(data).encode('utf8')
            req = Request(url, data=params, headers={'Content-Type': 'application/json; charset=utf-8','Cache-Control': 'no-cache'})

        else:
            req = Request(url, headers={'Cache-Control': 'no-cache'})

        if method:
            req.get_method = lambda: method

        else:
            req.get_method = lambda: 'GET'

        if token:
            req.add_header("Authorization", "Bearer %s" % token)

        else:
            if username and password:
                credentials = ('%s:%s' % (username, password))
                encoded_credentials = base64.b64encode(credentials.encode('utf8'))
                req.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("utf8"))

        try:
            with urlopen(req, timeout=10, context=INSECURE_CONTEXT) as response:
                res = response.read()

            if not res:
                return True

            else:
                return json.loads(res.decode("utf-8"))

        except:

            return False

    @staticmethod
    def run_cmd(cmd, verbose=False):

        process = subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)

        (output, error) = process.communicate()

        if verbose:
            if output:
                # print(output.decode('utf-8').splitlines()) # stdout one line
                print('stdout:\n', output.decode('utf-8'))

            if error:
                # print(error.decode('utf-8').splitlines()) # stderr one line
                print('stderr:\n\n', error.decode('utf-8'))

        # return process.returncode

        return {
            'stdout': output.decode('utf-8').splitlines(),
            'stderr': error.decode('utf-8').splitlines(),
            'errcode': process.returncode
        }

    @staticmethod
    def gen_passwd():

        # https://en.wikipedia.org/wiki/Password_strength
        # digits = '0123456789'
        string = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        passwd_len = 14
        passwd = ''

        # length = len(digits)
        length = len(string)

        for x in range(passwd_len):
            # passwd += digits[math.floor(random.random() * length)]
            passwd += string[math.floor(random.random() * length)]

        return passwd


def main():

    pass


if __name__ == '__main__':

    sys.exit(main())
