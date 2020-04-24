#! /usr/bin/python
# coding:UTF-8
import urllib2,json,sys
import re
def get_access_token(corpid,corpsecret):
        url='https://oapi.dingtalk.com/gettoken?corpid=%s&corpsecret=%s' %(corpid,corpsecret)
        req=urllib2.Request(url)
        resp=urllib2.urlopen(req)
        respon_str=resp.read()
        return json.loads(respon_str)['access_token']
def send_text_chat(access_token,chat_id,subject,msg):
        url="https://oapi.dingtalk.com/chat/send?access_token=%s" %(access_token)
        headers={'Content-Type':'application/json'}
        data_list={
                        'chatid':chat_id,
                        'msgtype':'text',
                        'text':{
                                'content':subject+'\n'+msg
                        }
                }
        data_json=json.dumps(data_list)
        req=urllib2.Request(url=url,headers=headers,data=data_json)
        resp=urllib2.urlopen(req)
        respon_str=resp.read()
        return respon_str
def send_bot_chat(access_token,subject,dict_msg):
        url="https://oapi.dingtalk.com/robot/send?access_token=%s" %(access_token)
        headers={'Content-Type':'application/json'}
        data_list={
                        'msgtype':'text',
                        'text':{
				'content':subject+'\n'+dict_msg
                        }
                }
       	data_json=json.dumps(data_list)
	print data_json
       	req=urllib2.Request(url=url,headers=headers,data=data_json)
       	resp=urllib2.urlopen(req)
       	respon_str=resp.read()
	return respon_str
if __name__=='__main__':
        corpid='dingcf233b8a6f0ae77935c2f4657eb6378f'
        corpsecret='mJ2_Y56Ia7jU0yVZVXOPe_Ll_cSrcx7XkvAQlZYMMOKniRZbCOLN6wKuiWfyqp44'
        access_token=get_access_token(corpid,corpsecret)
	#https://oapi.dingtalk.com/robot/send?access_token=7648ff1a459f793386096b4d232e526fc4f8a310822d40bc0a472d68cf306270
#       create_chat_group(access_token)
#	print access_token
	#access_token='b55dfc5505752bb4a45b111ce5b91fe46cfad9654fbe7d77328bdccc6d7c2bf3'
	access_token=sys.argv[1]
	subject=sys.argv[2]
	msg=sys.argv[3]
#	msg_new=format_markdown(msg)
	msg_new=msg
	print send_bot_chat(access_token,subject,msg_new)
#        chat_id="chat70d5b2b13d49679483b93546f281d887"
#        send_text_chat(access_token,chat_id,subject,msg)
