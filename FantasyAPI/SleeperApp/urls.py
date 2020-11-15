from django.conf.urls import url
from SleeperApp import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^department/$',views.departmentApi),
    url(r'^department/([0-9]+)$',views.departmentApi),  
    
    url(r'^employee/$',views.employeeApi),
    url(r'^employee/([0-9]+)$',views.employeeApi),
    
    url(r'^SaveFile$', views.SaveFile),
    
    url(r'^gamelogs/$', views.gamelogAPI),
    
    # Sleeper Calls
    url(r'^sleeper/([0-9]+)$', views.sleeperAPI)
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)