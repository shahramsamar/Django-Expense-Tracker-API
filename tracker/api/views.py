from .models import ExpenseIncome
from .api.serializers import ExpenseIncomeSerializer
from .api.permissions import IsOwnerOrSuperuser
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics, status
from .models import ExpenseIncome
from .api.serializers import UserRegisterSerializer, ExpenseIncomeSerializer
from .api.permissions import IsOwnerOrSuperuser
from rest_framework_simplejwt.tokens import RefreshToken




class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate tokens for the new user
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)



class ExpenseIncomeViewSet(viewsets.ModelViewSet):
    queryset = ExpenseIncome.objects.all()
    serializer_class = ExpenseIncomeSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrSuperuser]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return ExpenseIncome.objects.all()
        return ExpenseIncome.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


