import requests
import json
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
# URL from the curl command
url = '******'
majorId=59
num_pages = 20

headers = {
    "authority": "www.gaoxiaojob.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "referer": "https://www.gaoxiaojob.com/job?majorId=59&educationType=3&isFresh=1",
    "sec-ch-ua": "^\\^Microsoft",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
}
cookies = {
    "gr_user_id": "55cd9630-9868-4503-9747-f3051a55c5fb",
    "_identity-frontendPc": "f3727ff8aa976c49913e6fd4a30e101c72fd451ef7abca4b7160c5b7d18bd085a^%^3A2^%^3A^%^7Bi^%^3A0^%^3Bs^%^3A20^%^3A^%^22_identity-frontendPc^%^22^%^3Bi^%^3A1^%^3Bs^%^3A21^%^3A^%^22^%^5B573200^%^2Ctrue^%^2C2592000^%^5D^%^22^%^3B^%^7D",
    "Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE3MDg5MTU0MzAuNDE5MTQ5LCJqdGkiOiJnYW9jYWl0ZXN0IiwiZXhwIjoxNzA5Nzc5NDMwLjQxOTE0OSwidWlkIjoiNTczMjAwIiwiZW52aXJvbm1lbnQiOiJwcm9kIn0.8TT2ihZc7L8o6p2zqZj_8zDPBepf_mf1zaeTTDcwnl8",
    "8e5e4b80a514d362_gr_session_id": "18227a40-42fa-4bba-acb8-1b31783750ed",
    "8e5e4b80a514d362_gr_session_id_sent_vst": "18227a40-42fa-4bba-acb8-1b31783750ed",
    "gaoxiaojob": "10863713426706667358351856757163",
    "Hm_lvt_4300f9187d3b607ec69ea844e79f3dae": "1708915292,1709448632,1710654734,1710684460",
    "advanced-frontendPc": "2frdqa8d2lg15dkh0s7g3g55a6",
    "gaoxiaojobPositionToken": "gcjobprod",
    "Hm_lpvt_4300f9187d3b607ec69ea844e79f3dae": "1710685317"
}
url = "https://www.gaoxiaojob.com/job/home-list"
def request_page(url, headers, cookies, Page_Num):
    params = {
        "majorId": majorId,
        "educationType": "3",
        "isFresh": "1",
        "currentPage": Page_Num
    }
    response = requests.get(url, headers=headers, cookies=cookies, params=params)
    return response.text
# res_list=[]
# for page in tqdm(range(1, 100)):
#     try:
#         # time.sleep(1)
#         res=request_page(url, headers, cookies, page)
#         res_list.append(res)
#     except:
#         break
def fetch_page(page):
    """
    Attempts to fetch a page and return its content.
    If an error occurs, it returns None.
    """
    try:
        # Your request_page function presumably sends a request and returns the response
        response = request_page(url, headers, cookies, page)
        return response
    except Exception as e:
        print(f"Failed to fetch page {page}: {e}")
        return None

res_list = []



# Using ThreadPoolExecutor to fetch pages in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    # Prepare a list of futures
    future_to_page = {executor.submit(fetch_page, page): page for page in range(1, num_pages + 1)}
    
    # Process the completed futures as they complete
    for future in tqdm(as_completed(future_to_page), total=len(future_to_page)):
        page = future_to_page[future]
        try:
            res = future.result()
            # Only append non-None results
            if res is not None:
                res_list.append(res)
        except Exception as exc:
            print(f'Page fetch generated an exception: {exc}')
refreshTime_list=[]
companyName_list=[]
jobName_list=[]
experience_list=[]
education_list=[]
companyNatureName_list=[]
jobCategory_list=[]
areaName_list=[]
announcementUrl_list=[]


for res in res_list:
    for list in json.loads(res)['data']['list']:
        # print(list)
        refreshTime_list.append(list['refreshTime'])
        companyName_list.append(list['companyName'])
        jobName_list.append(list['jobName'])
        experience_list.append(list['experience'])
        education_list.append(list['education'])
        companyNatureName_list.append(list['companyNatureName'])
        jobCategory_list.append(list['jobCategory'])
        areaName_list.append(list['areaName'])
        announcementUrl_list.append('https://www.gaoxiaojob.com'+list['announcementUrl'])
import pandas as pd
df2 = pd.DataFrame({
    'refreshTime': refreshTime_list,
    'companyName': companyName_list,
    'jobName': jobName_list,
    'experience': experience_list,
    'education': education_list,
    'companyNatureName': companyNatureName_list,
    'jobCategory': jobCategory_list,
    'areaName': areaName_list,
    'announcementUrl': announcementUrl_list
})

df2 = df2.sort_values(by='refreshTime',ascending=False)

# df2.to_csv('rongjob.csv',encoding='gbk',index=False)


aggregations = {
    'refreshTime': 'max',
    'jobName': lambda x: x.str.cat(sep=','),
    'experience':'max',
    'education':'max',
    'companyNatureName':'max',
    'jobCategory':lambda x: x.str.cat(sep=','),
    'areaName':'max',
    'announcementUrl':'max'   
}
# df_unique = df2.drop_duplicates(subset=['companyName'])
aggregated = df2.groupby(['companyName']).agg(aggregations).reset_index()
aggregated = aggregated.sort_values(by='refreshTime',ascending=False)
df1=pd.read_csv('job.csv',encoding='gbk')
# summary = pd.concat([df1,aggregated]).drop_duplicates(keep="first")
# summary = summary.sort_values(by='refreshTime',ascending=False)
# print(aggregated)
aggregated.to_csv('job.csv',encoding='gbk')



aggregated['refreshTime'] = pd.to_datetime(aggregated['refreshTime'])
current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(current_time)

# 取今天的数据
totay_data = aggregated[aggregated['refreshTime'] > pd.to_datetime(current_time) - pd.Timedelta(days=1)]
print(totay_data)

# 取前7天的数据
seven_days_ago = pd.to_datetime(current_time) - pd.Timedelta(days=3)
seven_days_ago_data = aggregated[aggregated['refreshTime'] > seven_days_ago]
# print(seven_days_ago_data)

diff=totay_data
# def df1_df2(df1,df2):
#     result = pd.merge(df1, df2, how='inner')
#     print(len(result))
#     result = pd.merge(result, df1, how='outer', indicator=True)
#     diff = result[result['_merge'] == 'right_only'].drop(columns=['_merge'])
#     return diff
# # 取df2-df1的差集
# print(len(aggregated),len(df1))
# diff = df1_df2(aggregated,df1)
# print(diff)

import requests




def send_message(webhook_url, data):
    """
    Sends a message to a specified webhook URL.

    Parameters:
    - webhook_url (str): The webhook URL to send the message to.
    - message (str): The message content to send.

    Returns:
    - response.text (str): The response text from the server.
    """
    # Data payload as a Python dictionary

    # Specify headers
    headers = {'Content-Type': 'application/json'}

    # Send POST request
    response = requests.post(webhook_url, json=data, headers=headers)

    # Return response text
    return response.text


if len(diff)>0:
    count=0
    data={
    "msgtype":"text",
    "text":{
        "content":"春春有新增岗位请前往企业微信查看"}
    }
    send_message(url,data)
    for item in tqdm(diff.iterrows()):
        # print(item[1]['companyName'])   
        # print(item[1]['jobName'])
        # print
        data={
        "msgtype":"template_card",
        "template_card":{
            "card_type":"text_notice",
            "source":{
                "icon_url":"https://wework.qpic.cn/wwpic/252813_jOfDHtcISzuodLa_1629280209/0",
                "desc":"新增岗位",
                "desc_color":0
            },
            "main_title":{
                "title":item[1]['companyName'],
                "desc":"学历要求:"+item[1]['education']+";发布时间:"+str(item[1]['refreshTime'])
            },
            "emphasis_content":{
                "title":item[1]['areaName'],
                "desc":item[1]['companyNatureName']
            },

            "sub_title_text":"经验"+item[1]['experience']+";学历"+item[1]['education']+'\n'+"岗位类别"+item[1]['jobCategory']+'\n'+item[1]['jobName'],
            "horizontal_content_list":[
                {
                    "keyname":"邀请人",
                    "value":"春春"
                },
            ],
            "jump_list":[
                {
                    "type":1,
                    "url":item[1]['announcementUrl'],
                    "title":"发布时间"+str(item[1]['refreshTime'])
                }
            ],
            "card_action":{
                "type":1,
                "url":item[1]['announcementUrl'],
                # "appid":"APPID",
                # "pagepath":"PAGEPATH"
                }
            }
        }
        print(send_message(url,data))
        count+=1
        if count%20==19:
            time.sleep(20*60)
            # break
else:
    data={
    "msgtype":"text",
    "text":{
        "content":"春春今日暂无新增岗位"}
    }
    send_message(url,data)
    