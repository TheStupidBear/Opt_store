import os

os.environ["DJANGO_SETTINGS_MODULE"] = "opt_store.settings"

from rest_framework import serializers, renderers
from serializers import BasketSerializer


class BasketItem:
    def __init__(self, username, product, quantity, basket_id):
        self.username = username
        self.product = product
        self.quantity = quantity
        self.basket_id = basket_id


basket1 = BasketItem("Dimas", "Zerix", 4, 2)
basket2 = BasketItem("Serega", "Master", 2, 3)

queryset = [basket1, basket2]

serializer_obj = BasketSerializer(instance=queryset, many=True)


json_render = renderers.JSONRenderer()
data_in_json = json_render.render(serializer_obj.data)
print(data_in_json)
