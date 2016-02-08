from django.conf.urls import url

from . import views

urlpatterns = [
    #  name used in reverse
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^expense_form/$', views.ExpenseCreate.as_view(),  name="create"),
    url(r'^add_expense/$', views.add_expense, name='add_expense'),
    url(r'^(?P<pk>[0-9]+)/result/$', views.ResultView.as_view(), name='result')
]
