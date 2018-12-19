from django.urls import path

from . import views

app_name = 'easy'

urlpatterns = [
    path('', views.index, name='index'),
    path('guest/', views.guest, name='guest'),
    path('guest/delete/<uuid:guest_id>', views.guest_delete, name='guest_delete'),
    path('guest/search', views.GuestAutocomplete.as_view(), name='guest_search'),

    path('booking/', views.booking, name='booking'),
    path('booking/add/<uuid:room_id>/<str:start_date>/<str:end_date>', views.booking_add, name='booking_add'),
    path('booking/delete/<uuid:booking_id>', views.booking_delete, name='booking_delete'),
    path('booking/update/<uuid:booking_id>', views.booking_update, name='booking_update'),
    path('booking/user/add/<uuid:booking_id>', views.booking_user_add, name='booking_user_add'),
    path('booking/user/delete/<uuid:guest_booking_id>', views.booking_user_delete, name='booking_user_delete'),

    path('room_service/', views.room_service, name='room_service'),
    path('room_service/delete/<uuid:room_service_id>', views.room_service_delete, name='room_service_delete'),

    path('room/', views.room, name='room'),
    path('room/<uuid:room_id>', views.room, name='room'),
    path('room/delete/<uuid:room_id>', views.room_delete, name='room_delete'),

    path('users/', views.users, name='users'),
    path('users/delete/<uuid:user_id>', views.user_delete, name='user_delete'),

    path('api/login', views.login),
    path('api/bookings', views.booking_list),
    path('api/rooms', views.room_list),
    path('api/items', views.items_list),
    path('api/items/<uuid:booking_id>', views.items),
    path('api/cleaning', views.cleaning),
    path('api/cleaning/<uuid:booking_id>', views.cleaning),
    # path('api/rooms', views.room_list)
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]