#!/bin/bash

curl -k -s -u "username":"password" --get https://nexus.dev.mta4.ru/service/rest/v1/components?repository=app_distrib_1 | \
 python3 -c "import sys, json; [print('{0}, {1}, ({2})'.format(str(item['format']), str(item['name']), str(item['version']))) for item in json.load(sys.stdin)['items'] if 'app_distrib_1' in item['name']]"

curl -k -s -u "username":"password" --get https://nexus.dev.mta4.ru/service/rest/v1/components?repository=app_distrib_2 | \
 python3 -c "import sys, json; [print('{0}, {1}, ({2})'.format(str(item['format']), str(item['name']), str(item['version']))) for item in json.load(sys.stdin)['items'] if 'app_distrib_2' in item['name']]"

