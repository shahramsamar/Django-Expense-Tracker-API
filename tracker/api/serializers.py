from rest_framework import serializers
from ..models import ExpenseIncome
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'] 
        )
        return user






class ExpenseIncomeSerializer(serializers.ModelSerializer):
    
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = ['id', 'user', 'title', 'description', 'amount', 
                 'transaction_type', 'tax', 'tax_type', 'total',
                 'created_at', 'updated_at']
        read_only_fields = ('id','total','user', 'created_at', 'updated_at')
        
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
    
    def validate_tax(self, value):
        if value < 0:
            raise serializers.ValidationError("Tax cannot be negative.")
        return value
    def get_total(self, obj):
        return obj.total