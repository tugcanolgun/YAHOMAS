from django.urls import path

from . import views

app_name = 'easy'

urlpatterns = [
    path('', views.index, name='index'),
    path('guest/add', views.guest_add, name='guest_add'),
    path('guest/', views.guest, name='guest'),
    path('guest/delete/<uuid:guest_id>', views.guest_delete, name='guest_delete'),
    path('booking/', views.booking, name='booking'),
    path('booking/add', views.booking_add, name='booking_add'),
    path('booking/delete/<uuid:booking_id>', views.booking_delete, name='booking_delete'),
    path('booking/search', views.booking_search, name='booking_search'),
    # path('room_type/', views.room_type, name='room_type'),
    # path('room_type/add', views.room_type_add, name='room_type_add'),
    # path('room_type/delete/<uuid:room_type_id>', views.room_type_delete, name='room_type_delete'),
    path('room/', views.room, name='room'),
    path('room/<uuid:room_id>', views.room, name='room'),
    path('room/add', views.room_add, name='room_add'),
    path('room/delete/<uuid:room_id>', views.room_delete, name='room_delete'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]