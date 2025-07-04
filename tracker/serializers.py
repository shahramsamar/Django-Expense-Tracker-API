from rest_framework import serializers
from .models import ExpenseIncome

class ExpenseIncomeSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = ExpenseIncome
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def get_total(self, obj):
        return obj.total