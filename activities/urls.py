from django.urls import path
from activities import views

urlpatterns = [
        path('', views.activity_list, name='activity_list'),
        path('list', views.activity_list, name='activity_list'),
        path('<int:pk>/', views.activity_detail, name='activity_detail'),
        path('solution/<int:pk>', views.activity_detail_solution, name='activity_detail_solution'),
        path('handout/<int:pk>', views.activity_detail_handout, name='activity_detail_handout'),
        path('title/<int:pk>', views.activity_title, name='activity_title'),
        path('<int:pk>/title', views.activity_title, name='activity_title'),
        path('edit/<int:pk>', views.activity_edit, name='activity_edit'),
        path('new/', views.activity_new, name='activity_new'),

        # url(r'^homework/keyword/(?P<searchterm>\w+)/$', views.HomeworkKeywordView, name='homework_keyword'),
        # #path('<int:pk>/', views.activity_detail, name='activity_detail'),
        # path('edit/<int:pk>', views.activity_edit, name='activity_edit_preview'),
        # path('edit_preview/<int:pk>', views.activity_edit_preview, name='activity_edit_preview'),
        # path('solution/<int:pk>', views.activity_display_html_solution, name='activity_display_html_solution'),
        # path('render/html', views.activity_render_raw_html, name='activity_render_raw_html'),
        # path('render/html/<int:pk>', views.activity_render_html, name='activity_render_html'),
        # # path('/pdf/<int:pk>/', views.activity_render_pdf, name='activity_render_pdf'),
        # #path('<int:pk>/html/', views.activity_display_html, name='activity_display_html'),
        # #
]