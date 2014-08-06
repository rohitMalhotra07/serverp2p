from django.db import models
from django.contrib.auth.models import User, UserManager

class UserData(User):
	mac_id=models.CharField(max_length=17)
	ip_address=models.CharField(max_length=39)
	roll_no=models.CharField(max_length=20)
	college_name=models.CharField(max_length=30)
	onlineinfo=models.BooleanField(default=1)
	objects=UserManager()
	
	def __str__(self):
		return "roll_no:{0} mac_id:{1} status:{2} email:{3} ".format(self.roll_no,self.mac_id,self.onlineinfo,self.email)
	