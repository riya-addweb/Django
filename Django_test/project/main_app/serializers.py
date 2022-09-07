from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from .models import *

class CategorySerializer(serializers.ModelSerializer):

    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'title', 'order', 'subcategories']
        
    def get_subcategories(self, obj):         
        data = Category.objects.filter(parent_id = obj.id)        
        return CategorySerializer(data, many = True).data
    
    def get_order_count(self, obj):
        if not hasattr(obj, "order_count"):
            return 0
        return obj.order_count

    def create(self, validated_data):
        try:
            order = validated_data.pop("order")
            highest_order = Category.objects.aggregate(models.Max("order")).get(
                "order__max"
            )
            if order <= highest_order and order > 0:
                validated_data["order"] = order
                order_objects = Category.objects.filter(sequence__gte=order)
                for item in order_objects:
                    item.order += 1
                    item.save()
            else:
                current_count = (
                    Category.objects.aggregate(models.Max("order")).get(
                        "order"
                    )
                    or 0
                )
                validated_data["order"] = current_count + 1


        except:
            # If sequence is not given in response than increment it with the max seq
            current_count = (
                Category.objects.aggregate(models.Max("order")).get("order__max")
                or 0
            )

            validated_data["order"] = current_count + 1

        return super().create(validated_data)

 
class ProductSerializer(serializers.ModelSerializer):
    
    category_data = serializers.SerializerMethodField() 

    class Meta:
        model = Product
        fields = ['id', 'name', 'price','category_data']

    def get_category_data(self, obj):
        return CategorySerializer(obj.category.all(), many=True).data