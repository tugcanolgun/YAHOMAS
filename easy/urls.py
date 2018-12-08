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
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]