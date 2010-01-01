from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from mousedb.data.models import Study

@login_required
def limited_object_list(*args, **kwargs):
	return object_list(*args, **kwargs)

@login_required
def limited_object_detail(*args, **kwargs):
	return object_detail(*args, **kwargs)

@permission_required('data.add_study')
def create_study(*args, **kwargs):
	return django.views.generic.create_update.create_object(*args, **kwargs)

@permission_required('data.change_study')
def change_study(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)

@permission_required('data.delete_study')
def delete_study(*args, **kwargs):
	return django.views.generic.create_update.update_object(*args, **kwargs)

urlpatterns = patterns('',
	(r'^$', limited_object_list, {
		'queryset': Study.objects.all(),
		'template_name': 'study_list.html',
		'template_object_name': 'study',
		}),
	(r'^(?P<object_id>\d*)/$', limited_object_detail, {
		'queryset': Study.objects.all(),
		'template_name': 'study_detail.html',
		'template_object_name': 'study',
		}),
	(r'^(?P<study_id>\d*)/experiment/new/$', 'mousedb.data.views.study_experiment'),
)
