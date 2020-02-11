from django.urls import path
from public_app import views

urlpatterns = [
        path('', views.problem_list, name='problem_list'),
        path('list', views.problem_list, name='problem_list'),
        #path('<int:pk>/', views.problem_detail, name='problem_detail'),
        path('<int:pk>/', views.problem_display_html, name='problem_display_html'),
        path('new/', views.problem_new, name='problem_new'),
        path('edit/<int:pk>', views.problem_edit, name='problem_edit_preview'),
        path('edit_preview/<int:pk>', views.problem_edit_preview, name='problem_edit_preview'),
        path('solution/<int:pk>', views.problem_display_html_solution, name='problem_display_html_solution'),
        path('render/html', views.problem_render_raw_html, name='problem_render_raw_html'),
        path('render/html/<int:pk>', views.problem_render_html, name='problem_render_html'),
        # path('/pdf/<int:pk>/', views.problem_render_pdf, name='problem_render_pdf'),
        #path('<int:pk>/html/', views.problem_display_html, name='problem_display_html'),
]
