from django.shortcuts import render
from django.http import HttpResponse
import json
from django.shortcuts import render_to_response
from django.template import Template, RequestContext
from django import template
from django.template import Context
from django.http import QueryDict
import requests
from supernode.models import UserData
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

class MyCustomBackend:
	def authenticate(self, username=None, password=None,tempmac=None):
		print "in authenticate"
		print username,password,tempmac
		try:
			temp=UserData.objects.get(username=username)
			print temp.password
			if str(temp.password)==str(password):
				if str(tempmac)==str(temp.mac_id):
					temp.is_active=True
					temp.save()
					return temp
				else:
					print tempmac
					print temp.mac_id
					return None
			else:
				return None
		except User.DoesNotExist:
			return None
		def get_user(self, Username):
			try:
				return UserData.objects.get(username=Username)
			except User.DoesNotExist:
				return None 

mac_id_hashtable={}

def user_registration(request):
	print 'here'
	data = json.loads(request.body)
	ip_address=get_client_ip(request)
	print ip_address
	print data['mac_address']
	print data['username']
	print data['password']
	u=UserData.objects.create(username=data['username'],email=data['email'],password=data['password'],mac_id=data['mac_address'],ip_address=ip_address,roll_no= data['roll_no'],college_name=data['college_name'],onlineinfo=False)
	print "done1"
	#tempuserdata=UserData.objects.create(mac_id=data['mac_address'],ip_address=ip_address,roll_no= ['roll_no'],college_name=data['college_name'],onlineinfo=0)
	print 'done2'
	#print User.objects.all()
	print u.mac_id
	return HttpResponse("SUCCESS")



def make_hash():
	all_entries = Entry.objects.all()
	global mac_id_hashtable
	
	for user in all_entries:
		mac_id=user.mac_id
		mac_id_hashtable[mac_id]=1

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def checkvalidusername(request):
	print "request to check valid email recieved"
	data=json.loads(request.body)
	print data
	if data.has_key('username'):
		Username=data['username']
		num_results = UserData.objects.filter(username=Username).count()
		print num_results
		if num_results==0:
			datasend={'value':'True'}
			return HttpResponse(json.dumps(datasend))
		else:
			datasend={'value':'False'}
			return HttpResponse(json.dumps(datasend))
	else:
		datasend={'value':'no username recieved'}
		return HttpResponse(json.dumps(datasend))

def logincheck(request):
	print 'In login check'
	data=json.loads(request.body)
	username = data['username']
	password = data['password']
	mac_address=data['mac_address']
	user = authenticate(username=username, password=password,tempmac=mac_address)
	print user
	if user is not None:
		if user.is_active:
			login(request, user)
			print user.is_active
			user.onlineinfo=True
			user.save()
			print user.onlineinfo
			tempdata=getonlinelist()
			return HttpResponse(json.dumps(tempdata))
		else:
			tempdata={'value':'disabled account'}
			return HttpResponse(json.dumps(tempdata))
	else:
		tempdata={'value':'invalid login'}
		return HttpResponse(json.dumps(tempdata))
def getonlinelist():
	u=UserData.objects.filter(onlineinfo=True)
	print u.count()
	data={'value':'logged in'}
	#data['usersonline']={}
	data['onlinelist']=list()
	print data
	for item in u:
		tempname=item.username
		tempip=item.ip_address
		data['onlinelist'].append({'username':tempname,
									'ip_address':tempip
								  })
		print tempname
	print data
	return data

def logoutServer(request):
	print "in logout"
	data=json.loads(request.body)
	username=data['username']
	print username
	u=UserData.objects.get(username=username)
	u.onlineinfo=False
	u.is_active=False
	u.save()
	print u
	#logout(username)
	return HttpResponse("done logging out")
"""
def clientToServerPolling(request):
	print "request to poll recieved"
	data=json.loads(request.body)
	tempusername=data['username']
	tempip=get_client_ip(request)
	response={}
	n=UserData.objects.filter(username=tempusername).count()
	if n!=0:
		u=UserData.objects.get(username=tempusername)
		u.onlineinfo=True
		u.ip_address=tempip
		response['value']="updated"
		return HttpResponse(json.dumps(response))
	else:
		response['value']="not updated"
		return HttpResponse(json.dumps(response))
"""