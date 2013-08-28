from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from jsonfield import JSONField

# Create your models here.
class Item(models.Model):
	#variables

	#title
	title = models.CharField(max_length = 100)
	#author
	author = models.CharField(max_length = 30)
	#url
	url = models.URLField()
	#publish date
	date = models.CharField(max_length = 50)
	#vector/dictionary/text jsonField
	vector = JSONField(null = True,blank = True)

	def __unicode__(self):
		return self.title

#extend User model to save default filter
class UserProfile(models.Model):
	user = models.OneToOneField(User,related_name='profile')
	default_filter = models.ForeignKey('UserFilter',null=True, on_delete=models.SET_NULL)

	@property
	def num_filter(self):
		return UserFilter.objects.filter(user = user).count()

#link each filter to user, when user delete, all filter linked to this user will delete
class UserFilter(models.Model):
	user = models.ForeignKey(User)

	def __unicode__(self):
		return str(self.id)

#create userRecord when user was created
def create_user_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user, default_filter = None)
        up.save()

post_save.connect(create_user_profile, sender=User)




