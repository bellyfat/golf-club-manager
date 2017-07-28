from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from handicaps import urls as handicaps_urls


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(handicaps_urls)),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
]
