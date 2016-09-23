from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from recipes.api import router
from recipes.views import Index, Submit, Show, Edit, List

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^$', Index.as_view(), name='index'),
    url(r'^all/$', List.as_view(), name='list'),
    url(r'^submit/$', login_required(Submit.as_view()), name='submit'),
    url(r'^edit/(?P<pk>\d+)/$', Edit.as_view(), name='edit'),
    url(r'^(?P<pk>\d+)-(?P<slug>.+)/$', Show.as_view(), name='show'),
]
