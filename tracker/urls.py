from django.urls import path, include
from tracker import views



urlpatterns = [
    path('', views.ExposeListView.as_view(), name="expose-list"),
    path('expose/<int:pk>/', views.ExposeDetailView.as_view(), name="expose-detail"),
    path('expose/new/', views.ExposeCreateView.as_view(), name="expose-create"),
    path('expose/<int:pk>/update/', views.ExposeUpdateView.as_view(), name="expose-update"),
    path('expose/<int:pk>/delete/', views.ExposeDeleteView.as_view(), name="expose-delete"),
    path('api/',include('tracker.api.urls')),
]