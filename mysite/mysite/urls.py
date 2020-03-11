from django.conf.urls import url, include
from django.contrib import admin
from content import urls, views
from django.conf.urls.static import static
from django.conf import settings
from content import views as content_views
from dashboard import views as dashboard_views

urlpatterns = [
    url(r'^$', dashboard_views.index, name="index"),
    url(r'^admin/', admin.site.urls),
    url(r'accounts/', include('accounts.urls')),
    url(r'fms/', include('content.urls')),

    url(r'^type/add/$', views.type_add, name='type_add'),
    #url(r'^type/del/(?P<id>[a-zA-Z0-9]{32,32})/$', views.type_del, name='type_del'),
    url(r'^type/del/(?P<id>\d+)/$', views.type_del, name='type_del'),
    
    url(r'^get/email/$', views.get_email, name='get_email'),
    url(r'^send/emails/$', views.send_mails, name='send_mails'),
    url(r'^dashboard/', include('dashboard.urls')),
    url(r'^images/upload/$', content_views.upload_images, name='upload_images'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


'''
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^admin/', admin.site.urls),
    
    url(r'^', include('account.urls')),
    #url(r'^$', RedirectView.as_view(url='/account/index/', query_string=True)),
    #url(r'^$', RedirectView.as_view(url='/login/', query_string=True)),
]
'''