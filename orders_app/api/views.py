from rest_framework.response import Response
from rest_framework import viewsets
from orders_app.models import Order
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, CreateOrderSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from .permissions import IsOwnerOrAdmin, IsCustomerProfile
from django.db import models


class OrderListView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [IsAuthenticated, IsCustomerProfile]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Order.objects.filter(
            models.Q(customer_user=user_profile) | models.Q(
                business_user=user_profile)
        )

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        response_serializer = self.get_serializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        instance.delete()


class OrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            count = Order.objects.filter(
                business_user=business_user_id, status="in_progress").count()
            return Response({"order_count": count}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)


class CompletedOrderCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, business_user_id):
        try:
            count = Order.objects.filter(
                business_user=business_user_id, status="completed").count()
            return Response({"completed_order_count": count}, status=status.HTTP_200_OK)
        except NotFound:
            return Response({
                "message": "Order not found"
            }, status=status.HTTP_404_NOT_FOUND)
