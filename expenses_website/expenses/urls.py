from django.conf.urls import url

from . import views

urlpatterns = [
    #  name used when calling reverse
    url(r'^$', views.ExpenseListView.as_view(), name='list'),
    url(r'^expense_form/$', views.ExpenseCreate.as_view(), name='create'),
    url(r'^category_form/$',
        views.CategoryCreate.as_view(),
        name='create_category'),
    url(r'^(?P<pk>[0-9]+)/category/$',
        views.CategoryView.as_view(),
        name='category'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^logged_out/$', views.LoggedOutView.as_view(), name='logged_out'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultView.as_view(), name='result')
]
