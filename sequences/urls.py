from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import path
from sequences import views

urlpatterns = [
    path('', views.sequence_list, name='sequence_list'),
    path('list', views.sequence_list, name='sequence_list'),

    path('associate_problem/<int:sequence_id>/<int:problem_id>/', views.associate_problem, name='associate_problem'),
    path('unassociate_problem/<int:sequence_id>/<int:problem_id>/', views.unassociate_problem, name='unassociate_problem'),
    path('associate_activity/<int:sequence_id>/<int:activity_id>/', views.associate_activity, name='associate_activity'),
    path('unassociate_activity/<int:sequence_id>/<int:activity_id>/', views.unassociate_activity, name='unassociate_activity'),

    # path('update_sequence_item/<int:sequence_id>/<int:item_id>/', views.update_sequence_item, name='update_sequence_item'),

    path('<int:pk>/', views.sequence_detail, name='sequence_detail'),
    path('solution/<int:pk>', views.sequence_detail_solution, name='sequence_detail_solution'),
    
    path('title/<int:pk>', views.sequence_title, name='sequence_title'),
    path('<int:pk>/title', views.sequence_title, name='sequence_title'),
        
    path('edit/<int:pk>', views.sequence_edit, name='sequence_edit'),

    path('new/', views.sequence_new, name='sequence_new'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
