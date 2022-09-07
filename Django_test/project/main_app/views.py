from django.shortcuts import render
from rest_framework import viewsets, status
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all().order_by('order')
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    # def get_queryset(self):
    #     # return super().get_queryset()
    #     print("1")

    #     subcategory = Category.objects.exclude(parent = 'Null')
    #     subcategoryserializer = CategorySerializer(subcategory, many = True)
    #     print(subcategory)

    #     category = Category.objects.filter(parent = 'Null')
    #     categoryserializer = CategorySerializer(category, many = True)
    #     print(categoryserializer)

        # return Response({
        #     "status": status.HTTP_200_OK,
        #     "message":"None of your products are eligible for coupon",
        #     "cart_items_count": len(category),
        #     "category": categoryserializer.data,
        #     "subcategory": subcategoryserializer.data,
            
        #     })


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        inst_order = instance.order
        objects = Category.objects.filter(order__gt=inst_order)
        
        self.perform_destroy(instance)
        
        for item in objects:
            item.order -= 1
            item.save()
            
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "message": f"Data {instance} deleted Successfully"
        })
        

class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'put','delete']

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": f"Data {instance} deleted Successfully",
            }
        )

class AddProductViewSet(viewsets.ViewSet):

    def update(self, request, product_id, category_id): 

        try:                 
            
            product = Product.objects.get(id = product_id)
            cat = Category.objects.get(id = category_id)
            serializer = ProductSerializer(product, many=False)
            print("product",product)
            print("category",cat)
            product.category.add(cat)
            product.save()

            return Response(serializer.data)
                
        except Exception as e:
            raise ValidationError({"msg": e})
        
