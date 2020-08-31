from django.urls import path
from public_app import views
from django.conf.urls import url
from activity_media import views

urlpatterns = [
    # A list of medias for a given activity
    # path('<int:pk>/', views.activity_display_html, name='activity_display_html'),

    # Upload medias for a given activity
    path('upload/<int:activity_id>/', views.ProgressBarUploadViewMedia.as_view(), name='progress_bar_upload_media'),

    # Delete all medias for a given activity
    path('delete_activity_media/<int:activity_id>/', views.delete_media_for_activity, name='delete_media_for_activity'),

    # Dissassociate a media and delete the file.
    path('delete_media/<int:media_id>/', views.delete_media, name='delete_media'),

    path('categorize_media/<int:media_id>/<media_category>', views.categorize_media, name='categorize_media'),

    # url(r'^categorize_media/<int:media_id>/(?P<media_category>[\w\-]+)/$', views.categorize_media, name='categorize_media'),

    url(r'^clear/$', views.delete_all_media, name='delete_all_media'),

    # NOT USED. REMOVE AFTER TESTING AND BEFORE PRODUCTION
    # url(r'^upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # url(r'^upload/(?P<activity_id>[0-9]{1,9})/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # Upload medias without assigning them to a activity
    path('upload/', views.ProgressBarUploadViewMedia.as_view(), name='progress_bar_upload'),
    # path('upload/', views.ProgressBarUploadView, name='progress_bar_upload'),
    # path('upload/<int:activity_id>/', views.ProgressBarUploadView, name='progress_bar_upload'),
    # Not used
    url(r'^basic-upload/$', views.BasicUploadViewMedia.as_view(), name='basic_upload'),
    # path('basic-upload/', views.BasicUploadView, name='basic_upload'),
    # Not used
    path('basic-upload/', views.BasicUploadViewMedia.as_view(), name='basic_upload'),
    # url(r'^progress-bar-upload/$', views.ProgressBarUploadView, name='progress_bar_upload'),
    # Not used
    url(r'^progress-bar-upload/$', views.ProgressBarUploadViewMedia.as_view(), name='progress_bar_upload'),
    # url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView, name='drag_and_drop_upload'),
    # Not used
    url(r'^drag-and-drop-upload/$', views.DragAndDropUploadViewMedia.as_view(), name='drag_and_drop_upload'),
]
