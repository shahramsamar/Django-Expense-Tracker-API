from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..api.views import ExpenseIncomeViewSet,UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'expenses', ExpenseIncomeViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    # authentication and registration URLs
    path('auth/register/', UserRegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  
]
