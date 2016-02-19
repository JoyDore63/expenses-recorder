from django.conf.urls import url

from . import views

urlpatterns = [
    #  name used when calling reverse
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^list/$', views.ExpenseListView.as_view(), name='list'),
    url(r'^expense_form/$', views.ExpenseCreate.as_view(), name='create'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^logged_out/$', views.LoggedOutView.as_view(), name='logged_out'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultView.as_view(), name='result')
]
