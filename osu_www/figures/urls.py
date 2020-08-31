from django.urls import path
from public_app import views
from django.conf.urls import url
from figures import views

urlpatterns = [
    # A list of figures for a given problem
    # path('<int:pk>/', views.problem_display_html, name='problem_display_html'),

    # Upload figures for a given problem
    path('upload/<int:problem_id>/', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),

    # Delete all figures for a given problem
    path('delete_problem_figures/<int:problem_id>/', views.delete_figures_for_problem, name='delete_figures_for_problem'),

    # Dissassociate a figure and delete the file.
    path('delete_figure/<int:figure_id>/', views.delete_figure, name='delete_figure'),
    url(r'^clear/$', views.delete_all_figures, name='delete_all_figures'),

    path('categorize_media/<int:figure_id>/<media_category>', views.categorize_media, name='categorize_media'),

    # NOT USED. REMOVE AFTER TESTING AND BEFORE PRODUCTION
    # url(r'^upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # url(r'^upload/(?P<problem_id>[0-9]{1,9})/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # Upload figures without assigning them to a problem
    path('upload/', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # path('upload/', views.ProgressBarUploadView, name='progress_bar_upload'),
    # path('upload/<int:problem_id>/', views.ProgressBarUploadView, name='progress_bar_upload'),
    # Not used
    url(r'^basic-upload/$', views.BasicUploadView.as_view(), name='basic_upload'),
    # path('basic-upload/', views.BasicUploadView, name='basic_upload'),
    # Not used
    path('basic-upload/', views.BasicUploadView.as_view(), name='basic_upload'),
    # url(r'^progress-bar-upload/$', views.ProgressBarUploadView, name='progress_bar_upload'),
    # Not used
    url(r'^progress-bar-upload/$', views.ProgressBarUploadView.as_view(), name='progress_bar_upload'),
    # url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView, name='drag_and_drop_upload'),
    # Not used
    url(r'^drag-and-drop-upload/$', views.DragAndDropUploadView.as_view(), name='drag_and_drop_upload'),
]
