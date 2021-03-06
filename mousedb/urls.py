"""Generic base url directives.

These directives will redirect requests to app specific pages, and provide redundancy in possible names."""

from django.conf.urls import *
from django.contrib import admin

from tastypie.api import Api

from mousedb.data.api import MeasurementResource, AssayResource, ExperimentResource, StudyResource
from mousedb.animal.api import AnimalResource, StrainResource
from mousedb.views import APIKeyView

v1_api = Api(api_name='v1')
v1_api.register(AnimalResource())

v1_api.register(MeasurementResource())
v1_api.register(AssayResource())
v1_api.register(ExperimentResource())
v1_api.register(StudyResource())

admin.autodiscover()

urlpatterns = patterns('',
	#(r'^', 'django.views.generic.simple.direct_to_template', {'template': 'maintenance.html'}),
	(r'^ajax_select/', include('ajax_select.urls')),	
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
    (r'^api/',include(v1_api.urls)),
    url(r'^api_key/', APIKeyView.as_view(), name="api-keys"),	
	url(r'^accounts/login/', 'django.contrib.auth.views.login', name="login"),
	url(r'^accounts/logout/', 'mousedb.views.logout_view', name="logout"),

	url(r'^mouse/', include('mousedb.animal.urls.mouse')),
	url(r'^mice/', include('mousedb.animal.urls.mouse')),
	url(r'^animals?/', include('mousedb.animal.urls.mouse')),
	url(r'^strains?/', include('mousedb.animal.urls.strain')),
	url(r'^dates?/', include('mousedb.animal.urls.date')),
	url(r'^breedings?/', include('mousedb.animal.urls.breeding')),
	url(r'^breeding_cages?/', include('mousedb.animal.urls.breeding')),
	url(r'^todo/', include('mousedb.animal.urls.todo')),
	url(r'^cages?/', include('mousedb.animal.urls.cage')),
	
	url(r'^experiments?/', include('mousedb.data.urls.experiment')),
	url(r'^study/', include('mousedb.data.urls.study')),
	url(r'^studies/', include('mousedb.data.urls.study')),
	url(r'^treatments?/', include('mousedb.data.urls.treatment')),
	url(r'^parameters?/', include('mousedb.data.urls.parameter')),
    url(r'^cohorts?/', include('mousedb.data.urls.cohort')),

	url(r'^plugs?/', include('mousedb.timed_mating.urls')),
	url(r'^plugevents?/', include('mousedb.timed_mating.urls')),
	url(r'^plug_events?/', include('mousedb.timed_mating.urls')),
	url(r'^timedmatings?/', include('mousedb.timed_mating.urls')),
	url(r'^timed_matings?/', include('mousedb.timed_mating.urls')),
	
	url(r'^veterinary/', include('mousedb.veterinary.urls')),
	
	url(r'^index/$', 'mousedb.views.home', name="home"),
	url(r'^/?$', 'mousedb.views.home')
)

