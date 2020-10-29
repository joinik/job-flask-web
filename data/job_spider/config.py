#!/usr/bin/env python
# -*- coding: utf-8 -*-

MYSQL_URL = 'mysql+mysqldb://root:mysql@localhost:3306/job_web_2020?charset=utf8'

# 去重所用的Redis
HOST = 'localhost'
PORT = 6379
KEY_NAME = 'job'

UA = {
	'Accept': "application/json, text/javascript, */*; q=0.01",
	'Accept-Encoding': 'gzip, deflate, br',
	'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
	'Connection': 'keep-alive',
	'Referer': 'https://www.lagou.com/gongsi/',
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
	              "(KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
	# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
	# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
	#               'AppleWebKit/537.36 (KHTML, like Gecko) '
	#               'Chrome/64.0.3282.119 Safari/537.36',
# 	'Upgrade-Insecure-Requests': '1'
# # 是一个请求首部，用来向服务器端发送信号，表示客户端优先选择加密及带有身份验证的响应，并且它可以成功处理
}

LOGGING_CONF = {'version': 1,
                'disable_existing_loggers': False,
                'formatters': {'fh_format': {'format': '%(asctime)s [%(levelname)s] %(message)s'},
                               'sh_format': {'format': '%(asctime)s [%(levelname)s] %(message)s',
                                             'datefmt': '%H:%M:%S'
                                             }
                               },
                'handlers': {'fh': {'level': 'DEBUG',
                                    'formatter': 'fh_format',
                                    'class': 'logging.FileHandler',
                                    'filename': './log.txt'
                                    },
                             'sh': {'level': 'INFO',
                                    'formatter': 'sh_format',
                                    'class': 'logging.StreamHandler'
                                    }
                             },
                'loggers': {'root': {'handlers': ['fh', 'sh'],
                                     'level': 'DEBUG',
                                     'encoding': 'utf8'
                                     }
                            }
                }
