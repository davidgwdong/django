from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from sharemanager import views
from django.conf.urls import include
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    url(r'^sharemanager/$', views.ShareList.as_view()),
    url(r'^sharemanager/(?P<pk>[0-9]+)/$', views.ShareDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
]

urlpatterns += [
    url(r'^facebook-signup/$', csrf_exempt(views.FacebookLoginOrSignup.as_view()), name='facebook-login-signup'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

