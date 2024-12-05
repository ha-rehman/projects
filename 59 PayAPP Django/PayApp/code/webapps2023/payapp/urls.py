

from django.urls import path, include
from . import views

app_name = "payapp"

urlpatterns = [
    path('transfer', views.transfer, name="transfer"),
    path('request', views.send_request, name="request"),
    path('transactions', views.view_transactions, name="transactions"),
    path('view_users', views.view_users, name="view_users"),
    path('notification', views.notification, name="notification"),
    # path('request_decision', views.request_decision, name="request_decision"),
    path('request_decision/<int:id>/', views.request_decision, name="request_decision_id"),
    path('request_action/<int:id>/<str:decision>/', views.request_action, name="request_action")
]