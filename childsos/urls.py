"""childsos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from service import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)
router.register(r'api/cases',views.CasesViewSet)
router.register(r'api/responses',views.ResponseViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.HomeView.as_view(),name='home'),
    url(r'^thankyou/$', views.ThankYouView.as_view(),name='thankyou'),
    url(r'^login/$', views.LoginView.as_view(),name='login'),
    url(r'^logout/$', views.LogoutView.as_view(),name='logout'),
    url(r'^dashboard/$', views.DashboardView.as_view(),name='dashboard'),
    url(r'^invitations/$', views.InvitationsView.as_view(),name='invitations'),
    url(r'^case/all/$', views.CaseAllView.as_view(),name='case-all'),
    url(r'^case/(?P<case_id>\d+)/detail/$', views.CaseDetailView.as_view(case_id=None),name='case-detail'),

    url(r'^api/case-all/$', views.CaseListApi.as_view(),name='api-case-all'),
    url(r'^api/case-detail/(?P<pk>[0-9]+)/$', views.CaseDetailApi.as_view(),name='api-case-detail'),

]
