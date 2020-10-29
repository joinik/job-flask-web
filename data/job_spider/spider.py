#!/usr/bin/env python
# -*- coding: utf-8 -*-
import parsel
import requests
import time
import re
import json
import random
import logging
from lxml import etree
from html import unescape
from job_spider.dbop import SqlOperator, Dupefilter
from job_spider.config import UA


# 获取cookies值
def get_cookie():
	# 原始网页的URL
	url = "https://www.lagou.com/gongsi/"
	s = requests.Session ()
	s.get (url, headers=UA, timeout=3)  # 请求首页获取cookies
	cookie = s.cookies  # 为此次获取的cookies
	# print ((cookie["X_HTTP_TOKEN"]))
	return cookie


class LaGouSpider (object):
	"""拉勾网"""

	def __init__(self):
		# 需要指定cookie，否则会出错
		self.headers = UA.copy ()
		self.cookies = get_cookie()
		self.logger = logging.getLogger ('root')
		# 同一爬虫连续请求的最短间隔
		self.request_sleep = 7
		# 用于记录最近一次请求的时间戳
		self._time_recode = 0
		self._redis = Dupefilter ()
		self._sql = SqlOperator ()

	def crawl(self):
		page = 1
		while True:
			companies = self.parsel_com()
			# companies = self._get_company_data (page)
			# if not companies:
			# 	return True
			for c in companies:
				result, company_id = self._parse_company_data (c)
				print(" 1--------",company_id)
				yield result if result else {'type': 'company', 'company_id': company_id}
				job_page = 1
				counter = 0
				# 每个公司的职位只随机爬前N个
				total = random.randint (5, 30)
				while counter < total:
					print("  职位循环 ----- --- ")
					jobs = self._get_job_data (c['companyId'], job_page)
					if not jobs:
						break
					for j in jobs:
						job_result = self._parse_job_data (j)
						counter += 1
						if not job_result:
							counter = total
							break
						yield job_result
					job_page += 1
			# page += 1


	def _get_company_data(self, page):
		url = 'https://www.lagou.com/gongsi/0-0-0.json'
		params = {'first': 'false', 'pn': page, 'sortField': 0, 'havemark': 0}
		resp = self._request ('post', url, data=params)
		# 解析详情页的编号，进一步分析详情页
		resp_data = json.loads (resp.text)
		return resp_data['result']

	def _get_job_data(self, company_id, page):
		print(' 进行公司职位位爬取 ----' )
		job_url = 'https://www.lagou.com/gongsi/searchPosition.json'
		job_params = {'companyId': company_id, 'pageNo': page,
		              'positionFirstType': '全部', 'pageSize': 10, 'schoolJob': 'false'}
		job_resp = self._request ('post', job_url, data=job_params, headers=UA, cookies=get_cookie(), timeout=5)
		job_resp_data = json.loads (job_resp.text)
		print("job 解析开始--------》》》")
		return job_resp_data['content']['data']['page']['result']

	def _parse_company_data(self, data):
		result = dict ()
		# detail_url = 'https://www.lagou.com/gongsi/%s.html' % data['companyId']
		detail_url = 'https://www.lagou.com/gongsi/%s.html' % data['companyId']
		company_id = self._sql.get_company_id (data['companyShortName'])
		print("公司解析开始---。。。。。")
		if not company_id:
			result = {
				'type': 'company',
				'name': data['companyShortName'],
				'description': data['companyFeatures'],
				'field': data['industryField'],
				'finance_stage': data['financeStage'],
				'address': data['city'],
				'logo': data['companyLogo']
			}
			result.update (self._parse_company_detail (detail_url))
		return result, company_id

	def _parse_job_data(self, data):
		detail_url = 'https://www.lagou.com/jobs/%s.html' % data['positionId']
		if not self._redis.add (detail_url):
			return None
		job_result = {
			'type': 'job',
			'name': data['positionName'],
			'salary': data['salary'],
			'city': data['city'],
			'exp': data['workYear'],
			'education': data['education'],
			'treatment': '，'.join (data['companyLabelList']),
			'tags': re.sub (r'[\s、;]', ',', data['positionAdvantage']),
		}
		job_result.update (self._parse_job_detail (detail_url))
		print("job 全部职位 ----解析结束--------》》》")

		return job_result

	def _parse_company_detail(self, detail_url):
		resp = self._request ('get', detail_url)
		resp.encoding = resp.apparent_encoding
		html = etree.HTML (resp.text)
		print(html," -------- 解析公司详情页")
		name = html.xpath ('//div[@class="company_main"]/h1/a/text()')
		# 这里最好先判断一下，以免没提取到出现异常
		if not name:
			self.logger.debug ('请求到错误页面')
			time.sleep (30)
			return self._parse_company_detail (detail_url)
		# 返回的键必须包含这些，否则写入会报错
		supply = {
			'details': unescape (str (etree.tostring (html.xpath (
				'//span[@class="company_content"]')[0]), encoding='utf8')).replace (
				'<span class="company_content">', '').replace ('\n', '').replace ('\xa0', ''),
			'website': html.xpath ('//div[@class="company_main"]/a[1]/@href')[0].split ('?')[0],
		}
		return supply

	def _parse_job_detail(self, url):
		resp = self._request ('get', url)
		resp.encoding = resp.apparent_encoding
		html = etree.HTML (resp.text)
		title = html.xpath ('//span[@class="name"]/text()')
		if not title:
			self.logger.debug ('请求到错误页面')
			time.sleep (30)
			return self._parse_job_detail (url)
		supply = {
			'description': unescape (str (etree.tostring (
				html.xpath ('//*[@id="job_detail"]/dd[2]/div')[0]), encoding='utf8')).replace (
				'<span class="company_content">', '').replace ('\n', '').replace ('\xa0', '')
		}
		return supply

	def _request(self, method='get', url=None, encoding=None, **kwargs):
		while True:
			# 没有指定头部则使用默认头部
			if not kwargs.get ('headers'):
				kwargs['headers'] = self.headers
			# 随机生成系数对间隔产生变化
			rand_multi = random.uniform (0.8, 1.2)
			# 距离上次请求的间隔
			interval = time.time () - self._time_recode
			# 如间隔小于最短间隔，则进行等待
			if interval < self.request_sleep:
				time.sleep ((self.request_sleep - interval) * rand_multi)
			resp = getattr (requests, method) (url, **kwargs)
			# 请求完重新记录时间戳
			self._time_recode = time.time ()
			if encoding:
				resp.encoding = encoding
			if '频繁' in resp.text:
				self.logger.debug ('请求频繁重试')
				time.sleep (20)
				print ('时间', time.time ())
				print ('请求频繁重试')
			else:
				break
		return resp

	def parsel_com(self):
		url = "https://www.lagou.com/gongsi/2-0-0-0"
		res = requests.get (url)
		res = res.text
		selector = parsel.Selector (res)
		li_list = selector.xpath ("//ul[@class='item_con_list']/li")

		data_list = []
		for i in li_list:
			#   公司数据
			print("第 %s次 爬取 数据-------"%str(i))
			data = {}
			com_id = i.xpath ("div//h3/a/@data-lg-tj-cid").get ()
			name = i.xpath ("div//h3/a/text()").get ()
			desc = i.xpath ("div//h4[@class='advantage wordCut']/text()").get ()
			field_data = i.xpath ("div//h4[@class='indus-stage wordCut']/text()").get ()
			logo = i.xpath ("div/p//img/@src").get ()
			field_list = field_data.split ('/')

			data = {
				# 公司id
				"companyId": com_id,
				# 公司名字
				"companyShortName": name,
				# 公司简介
				"companyFeatures": desc,
				# 领域
				"industryField": field_list[0],
				# 融资
				"financeStage": field_list[1],
				# 地址 城市
				"city": "北京",
				# logo 图片
				"companyLogo": logo
			}
			data_list.append(data)

		return data_list

if __name__ == '__main__':
	gs_id = input("公司id----")
	gs_name = input("公司名字----")
	data = {
		"companyId" : gs_id,
		"companyShortName": gs_name
	}

