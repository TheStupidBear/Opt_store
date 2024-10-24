from rest_framework import serializers
from .models import Basket, BasketItem


class BasketSerializer(serializers.Serializer):
    user = serializers.CharField()
    number_phone = serializers.CharField(source="user.number_phone")
    basketitem = serializers.StringRelatedField(many=True)


class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ["product", "quantity"]
