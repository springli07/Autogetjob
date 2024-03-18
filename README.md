# -
高校人才网自动爬取最新院校招聘信息并推送到企业微信机器人
## windows
### 任务计划程序定时运行

## linux 
### crontab 定时运行


```python
url = '*********'# 企业微信机器人webhookurl 获取教程 https://open.work.weixin.qq.com/help2/pc/14931?person_id=1&is_tencent=
majorId=59# 专业代码 可以从高校人才网页面获取 https://www.gaoxiaojob.com/job?majorId=59&educationType=3&isFresh=1
num_pages = 20# 爬取页码数量 一般20左右即可
cookies=*** # 登陆后以从高校人才网页面获取 https://www.gaoxiaojob.com/job?majorId=59&educationType=3&isFresh=1
```



## 实现功能
### 1.对同一企业或高校的不同岗位信息进行了合并展示在csv文件中。
### 2.运行代码结束后会筛选出过去一天的招聘信息并推送到企业微信。

## 请勿滥用 


