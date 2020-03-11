#-*- coding: utf-8 -*-

from django.conf.urls import url
from dashboard import views, zbx

urlpatterns = [

    url(r'^cus/$', views.index, name='cus_dashboard_index'),
    url(r'^cus/index/$', views.index_data, name='cus_index_data'),
    url(r'^cus/select/$', views.select_data, name='cus_select_data'),

    url(r'^zbx/$', zbx.index, name='zbx_dashboard_index'),
    
    url(r'^zbx/data/line/$', zbx.zbx_data_line, name='zbx_data_line'),
    url(r'^zbx/data/bar/$', zbx.zbx_data_bar, name='zbx_data_bar'),
    
    url(r'^zbx/line/$', zbx.zbx_line, name='zbx_line'),
    url(r'^zbx/bar/$', zbx.zbx_bar, name='zbx_bar'),
    
    # url(r'^zbx/select/$', zbx.select_data, name='zbx_select_data'), zbx_data_line
]
