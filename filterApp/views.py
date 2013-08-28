from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.context_processors import csrf 
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import re
from models import *
from Classifier import *
from operator import itemgetter

# Create your views here.

def home(request):

	if request.user is not None:
		if request.user.is_authenticated():
			return render_to_response('homepage.html', {'username': request.user.username})
		
	return render_to_response('homepage.html', {'username': 'guest'})

def login(request):
	
	errors = []
	c = {}
	c.update(csrf(request))
	if request.method=='POST':

		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()

			user = auth.authenticate(username =request.POST['username'],password = request.POST['password'])
			if user is not None and user.is_active:
				auth.login(request,user)
				return HttpResponseRedirect('/filter/loggedin')
		else:
			errors.append('plase enable cookie and try again')
			c['errors']=errors
			return render_to_response('login.html',c)

	request.session.set_test_cookie()
	return render_to_response('login.html',c)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/filter/home/')


def register(request):
	errors = []
	c = {}
	c.update(csrf(request))
	if request.method == 'POST':
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()

			form = auth.forms.UserCreationForm(request.POST)
			if form.is_valid():
				new_user = form.save()
				return HttpResponseRedirect("/filter/login/")
		else:
			errors.append('plase enable cookie and try again')
			request.session.set_test_cookie()
			return render_to_response('register.html',{'errors':errors})
	else:
		form = auth.forms.UserCreationForm()
	
	request.session.set_test_cookie()
	c['form'] =form
	return render_to_response("register.html",c)

@login_required
def loggedin(request):
	return render_to_response("loggedin.html",{'username':request.user.username})



@login_required
def train(request, num = 0,c ={}):
	"""train a classifier, 5 round active svm training. 'c' contians the training 
	dataset and labels. First show items which contian keywords in title. And then 
	show the item based on the decision value close to 0. The more it close to 0, 
	the more important the label is."""
	errors = []
	items = []
	c.update(csrf(request))
	c['username'] = request.user.username
	if 'dataset' not in c.keys():
		dataset = []
		labelset = []
	else:
		dataset = c['dataset']
		labelset = c['labelset']

	num_ = int(num)

	if 'num' not in request.session.keys():
		session_num = 0
	else:
		session_num = int(request.session['num'])
	#if update, method is post
	if request.method == 'GET':
		#'Get' means user get some ranked item and should make choice
		if num_ == 0 or 'num' not in request.session.keys():

			#input keyword, show items contains keyword
			x = c.pop('times',None)
			if 'keyword' in request.GET.keys():
				keyword = request.GET['keyword']
				items= Item.objects.filter(title__contains = keyword)[:20]
				if len(items) < 3:
					errors.append('too few find, please change a keyword')
					c['errors']=errors
				else:
					c['keyword'] = keyword
					c['items']=items
				return render_to_response('train.html',c)
			else:
			#first show the page with nothing.
				x = c.pop('items',None)

		elif num_ == session_num:
			x = c.pop('keyword',None)
			c['times'] = num_
		else:
			errors.append('wrong actions detected, please restart the process '+str(session_num) + ' : '+str(num_))

	elif request.method =='POST':

		#'post' means the user submit some choice
		choices = request.POST.getlist('choice')
		counter = 0
		for choice in choices:
			item_id,value = choice.split(':')
			if value == 'Yes':
				temp = Item.objects.get(id=int(item_id))
				dataset.append(temp.vector)
				labelset.append(1)
				counter = counter+1

			elif value == 'No':
				temp = Item.objects.get(id=int(item_id))
				dataset.append(temp.vector)
				labelset.append(-1)
				counter = counter+1

		#using counter to decide whether too few choices 
		# were made, please select more(exended in the future)

		#train classifier
		user = auth.get_user(request)
		classifier = Classifier(user)
		classifier.setDataset(dataset,labelset)
		classifier.train()
		items = Item.objects.all()
		p_label,p_acc,p_val=classifier.predict(items)
		
		# ranked by p_val closing to 0
		p_val = map(lambda z: abs(z[0]),p_val)
		tempList = map(lambda x,y:[x,y],items,p_val)
		tempList = sorted(tempList,key = itemgetter(1))
		c['items'] = map(lambda x:x[0],tempList[:20])

		#pass the para to next training round
		c['dataset'] = dataset
		c['labelset'] = labelset
		num_ = num_+1

		#total 5 round, which hava a meaningful classifier in general
		if num_ > 5:
			classifier.save()
			user.profile.default_filter = UserFilter.objects.get(id = classifier.id)
			return HttpResponseRedirect(reverse('filterApp.views.loggedin'))

		#if less than 5 round, continue. Save the times to session to verify whether 
		#user hit back or other button.
		request.session['num'] = num_
		return HttpResponseRedirect('/filter/loggedin/train/'+str(num_)+'/', c)

	c['errors']=errors
	return render_to_response('train.html',c)

@login_required
def show(request,filter_id = 0):
	"""based on the current user's filer, rank the items in source, and show out.
		current one only show the default classifier(last one). Could be extended 
		to show different classifier.
	"""
	errors =[]
	c={}
	c['username'] = request.user.username
	c['filter_id'] = filter_id
	if filter_id == 0:
		user = auth.get_user(request)
		temp = user.profile.default_filter
		if user.profile.default_filter is None:
			errors.append('plase train a filter first!')
			return render_to_response('show.html',{'username':request.user.username, 'errors':errors})
		else:
			classifier = Classifier(user = auth.get_user(request),id = user.profile.default_filter.id)
			classifier.load()
			items = Item.objects.all()
			p_label,p_acc,p_val=classifier.predict(items)
			tempList = map(lambda x,y:[x,y],items,p_val)
			tempList = sorted(tempList,key = itemgetter(1),reverse=True)
			c['items'] = map(lambda x:x[0],tempList[:20])

	return render_to_response('show.html',c)








