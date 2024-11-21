from rest_framework import serializers
from .models import *


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('joined_users',)


class DepositOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositOption
        fields = '__all__'
        read_only_fields = ('deposit',)


class DepositFullListSerializer(serializers.ModelSerializer):
    option = DepositOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = '__all__'
        read_only_fields = ('joined_users',)




class SavingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('joined_users',)


class SavingOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingOption
        fields = '__all__'
        read_only_fields = ('saving',)


class SavingFullListSerializer(serializers.ModelSerializer):
    option = SavingOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Saving
        fields = '__all__'
        read_only_fields = ('joined_users',)