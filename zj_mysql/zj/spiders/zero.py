# -*- coding: utf-8 -*-
# 登入zerojudge，讀取其他使用者AC的題數儲存到Mysql
import scrapy
from zj.items import ZjItem
import os

class ZeroSpider(scrapy.Spider):
    name = 'zero'
    allowed_domains = ['zerojudge.tw']
    login_url = 'https://zerojudge.tw/Login'
    start_urls = [login_url]    
    logout_url = 'https://zerojudge.tw/Logout'
    user_url = 'https://zerojudge.tw/UserStatistic?account=%s'
    
    def parse(self, response):   #使用FormRequest登入帳號
        data = {
            'account' : '您的zerojudge帳號',  #登入zerojudge帳號
            'passwd' : '您的zerojudge密碼',  #登入zerojudge密碼
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=data, callback=self.parse_user)  #登入zerojudge取出指定的使用者AC題數
             
    def parse_user(self, response):   #瀏覽使用者狀態網頁
        userlist=['stu1','stu2']  #學生帳號名稱串列
        for user in userlist:
            yield scrapy.Request(url=self.user_url % user , callback = self.parse_user_process)  #呼叫https://zerojudge.tw/UserStatistic?account=%s抓出使用者AC題數
            
    def parse_user_process(self, response):    #找出帳號與AC題數
        item = ZjItem()
        account = response.xpath('//button/@data-receiver').extract_first()  #取出button的屬性data-receiver值為zerojudge帳號
        ac = response.xpath('//p[@align="left"]/a/text()').extract_first()  #取出p的屬性align為left的標籤a所包夾的文字為AC題數
        item['acc'] = account
        item['ac'] = ac
        return item
