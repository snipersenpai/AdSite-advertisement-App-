from django.contrib import admin
from django.urls import include, path
from .views import *
app_name = 'ads'

urlpatterns = [
    path('',MainView.as_view(),name='all'),
    path('create',AdCreate.as_view(), name='ad_create'),
    # path('ad/<int:pk>/edit',AdUpdate.as_view(), name='ad_update'),
    path('ad/<int:pk>/update',AdUpdate.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete',AdDelete.as_view(), name='ad_delete'),
    path('ad/<int:pk>/detail',AdDetail.as_view(), name='ad_detail'),
    path('ad_picture/<int:pk>', stream_file, name='ad_picture'),
    path('ad/<int:pk>/comment',
        CommentCreateView.as_view(), name='ad_comment_create'),
    path('comment/<int:pk>/delete',
        CommentDeleteView.as_view(success_url=reverse_lazy('ads')), name='ad_comment_delete'),
    path('ad/<int:pk>/favorite',
    AddFavoriteView.as_view(), name='ad_favorite'),
    path('ad/<int:pk>/unfavorite',
        DeleteFavoriteView.as_view(), name='ad_unfavorite'),
]
