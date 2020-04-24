#! /usr/bin/python
from paramiko import SSHClient,util,Transport,SFTPClient,AutoAddPolicy
from scp import SCPClient
from ftplib import FTP
import threading,re
def read_txt():
	global line
	with open('/root/download_config/net-device.txt','r') as f:
		line=''.join(f.readlines()).split('\n')
		line.pop()
def add_val(re_v):
	global dict_key
	global dict_dev
	global num_thread
	if re.match('[a-z]',re_v):
		dict_key=re_v
		dict_dev.setdefault(dict_key,[])
	else:
		dict_dev[dict_key].append(re_v)
def sftp_client(ip,uname,pw,r_path,l_path):
#	util.log_to_file('/root/download_config/paramiko.log')
	try:
		t=Transport((ip,22))
		t.connect(username=uname,password=pw)
		sftp=SFTPClient.from_transport(t)
		sftp.get(r_path,l_path)
		t.close()
#	ssh = SSHClient()
#	ssh.set_missing_host_key_policy(AutoAddPolicy())
#	ssh.connect(ip,22,uname,pw,look_for_keys=False,allow_agent=False)
#	t=ssh.get_transport()
#	sftp=SFTPClient.from_transport(t)
#	sftp.get(r_path,l_path)
#	t.close()
	except:
		print 'sftp %s failed' % (ip)
def scp_client(ip,uname,pw,r_path,l_path):
	try:
		ssh=SSHClient()
#		ssh.load_system_host_keys()
		ssh.set_missing_host_key_policy(AutoAddPolicy())
		ssh.connect(ip,22,uname,pw,look_for_keys=False)
		scp=SCPClient(ssh.get_transport())
		scp.get(r_path,l_path)
		scp.close()
	except:
		print 'scp %s failed' % (ip)
def ftp_client(ip,uname,pw,r_path,l_path):
	try:
		ftp=FTP(ip)
		ftp.login(uname,pw)
		ftp.retrbinary('RETR '+r_path,open(l_path,'wb').write)
		ftp.quit()
	except:
		print 'ftp %s failed' % (ip)
def type_input_dev(dev):
	print '=====%s=====' %(dev)
	input_uname=raw_input("uname:")
	input_pw=raw_input("pw:")
	input_filename=raw_input("filename:")
	return (input_uname,input_pw,input_filename)
if __name__=="__main__":
        dict_key=''
        dict_dev={}
	list_thread=[]
	line=''
	read_txt()
	print '********\njuniper:ns_sys_config\nhuawei:vrpcfg.zip\ncisco:running-config\n********'
	try:
		for i in line:
			add_val(i)	
		for key in dict_dev:
			dev=type_input_dev(key)
			for ip in dict_dev[key]:
				if re.search('sftp',key):
					list_thread.append(threading.Thread(target=sftp_client,args=(ip,dev[0],dev[1],dev[2],'/root/download_config/sftp-config/'+ip+'_'+dev[0]+'_'+dev[2])))	
				elif re.search('ftp',key):
					list_thread.append(threading.Thread(target=ftp_client,args=(ip,dev[0],dev[1],dev[2],'/root/download_config/ftp-config/'+ip+'_'+dev[0]+'_'+dev[2])))
				elif re.search('scp',key):
					list_thread.append(threading.Thread(target=scp_client,args=(ip,dev[0],dev[1],dev[2],'/root/download_config/scp-config/'+ip+'_'+dev[0]+'_'+dev[2])))	
		for t in list_thread:
			t.start()
		for t1 in list_thread:
			t1.join()
	except:
		print "\nEND"
