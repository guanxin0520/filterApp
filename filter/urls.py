from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login as django_login, logout as django_logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'filterApp.views.home', name='home'),
    url(r'^filter/home/$','filterApp.views.home',name ='filterApp_home'),
    url(r'^filter/register/$', 'filterApp.views.register', name ='register'),
    url(r'^filter/login/$','filterApp.views.login', name = 'login'),
    url(r'^filter/logout/$','filterApp.views.logout', name = 'logout'),
    url(r'^filter/loggedin/$','filterApp.views.loggedin',name = 'loggedin'),
    url(r'^filter/loggedin/train/(?P<num>\d+)/$','filterApp.views.train', name = 'train_num'),
    url(r'^filter/loggedin/train/$','filterApp.views.train', name = 'train'),
    url(r'^filter/loggedin/show/$','filterApp.views.show', name = 'show'),
	url(r'^filter/loggedin/show/(\d+)/$','filterApp.views.show', name = 'show_id'),

    # url(r'^filter/', include('filter.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
