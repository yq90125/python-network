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
def create_chat_group(access_token):
        ct='application/json'
        url="https://oapi.dingtalk.com/chat/create?access_token=%s" %(access_token)
        headers={'Content-Type':'application/json'}
        data_list={'name':'ismewtf_sub_C','owner':'manager5829','useridlist':['manager5829']}
        data_json=json.dumps(data_list)
        req=urllib2.Request(url=url,headers=headers,data=data_json)
        resp=urllib2.urlopen(req)
        respon_str=resp.read()
        print respon_str
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
	#dict_msg['ITEM_KEY1']
	list_msg=dict_msg['ITEM_NAME1'].split('_')
#报警类型Traffic
	IN0=list_msg[0]
#报警方向
	IN1=list_msg[1]
#用户名称
	IN2=list_msg[2]
#接口
	ILast=list_msg[-1]
        data_list={
                        'msgtype':'markdown',
                        'markdown':{
                                'title':subject+'\n',
                               # 'text':'#[报警状态]%s\n- [所在位置]%s\n- [客户名称]%s\n- [触发条目]%s\n- [当前数值]%s' %(subject,dict_msg['HOST_NAME1'],dict_msg['ITEM_NAME1'],dict_msg['ITEM_KEY1'],dict_msg['ITEM_VALUE1'])
				'text':'#[所属设备]%s\n- [客户名称]%s\n- [当前状态]%s\n- [报警类型]%s\n- [方向]%s\n- [接口]%s\n- [当前值]%s\n- [触发条件]%s' %(dict_msg['HOST_NAME1'],IN2,dict_msg['STATUS'],IN0,IN1,IN2,dict_msg['ITEM_VALUE1'],dict_msg['TRIGGER_NAME'])
                        }
                }
	#if re.search('ABC|CCB',dict_msg['ITEM_NAME1']) and 'SNMP' not in dict_msg['ITEM_KEY1']:
	if re.search('Traffic|ABC|CCB',dict_msg['ITEM_NAME1']):
        	data_json=json.dumps(data_list)
        	req=urllib2.Request(url=url,headers=headers,data=data_json)
        	resp=urllib2.urlopen(req)
        	respon_str=resp.read()
        	return respon_str
def format_markdown(msg):
	dict_msg={}
        list_msg=msg.split(':')
	KEY_NAME=('ITEM_NAME1','HOST_NAME1','ITEM_KEY1','ITEM_VALUE1','TRIGGER_NAME','STATUS')
	for key in KEY_NAME:
		for value in list_msg:
			dict_msg.setdefault(key,value)
			list_msg.pop(0)
			break
	return dict_msg
if __name__=='__main__':
        corpid='dingcf233b8a6f0ae77935c2f4657eb6378f'
        corpsecret='mJ2_Y56Ia7jU0yVZVXOPe_Ll_cSrcx7XkvAQlZYMMOKniRZbCOLN6wKuiWfyqp44'
        access_token=get_access_token(corpid,corpsecret)
	#https://oapi.dingtalk.com/robot/send?access_token=7648ff1a459f793386096b4d232e526fc4f8a310822d40bc0a472d68cf306270
######	access_token='2895244b9c641d24218ad31925f1ea8db3b4d0864d52f750b20c49071d18b794'
#       create_chat_group(access_token)
	access_token='7648ff1a459f793386096b4d232e526fc4f8a310822d40bc0a472d68cf306270'
	print access_token
	chat_id=sys.argv[1]
	subject=sys.argv[2]
	msg=sys.argv[3]
	msg_new=format_markdown(msg)
	send_bot_chat(access_token,subject,msg_new)
#        chat_id="chat70d5b2b13d49679483b93546f281d887"
#        send_text_chat(access_token,chat_id,subject,msg)
