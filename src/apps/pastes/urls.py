from django.conf.urls import include, patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^$', views.CreatePasteView.as_view(), name='create_paste'),
    url(r'^(?P<pk>\w+)/', include([
        url(r'^edit/$', views.UpdatePasteView.as_view(), name='update_paste'),
        url(r'^delete/$', views.DeletePasteView.as_view(), name='delete_paste'),
        url(r'^$', views.ShowPasteCreateCommentView.as_view(), name='show_paste'),
    ])),
)
