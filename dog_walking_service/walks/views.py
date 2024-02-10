from django.http import JsonResponse
from .models import WalkOrder, APICall
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from .serializers import WalkOrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import time, timedelta


@swagger_auto_schema(method='get', responses={200: WalkOrderSerializer(many=True)})
@api_view(['GET'])
def get_orders(request, date):
    orders = WalkOrder.objects.filter(walk_datetime__date=date)
    serializer = WalkOrderSerializer(orders, many=True)
    APICall.objects.create(method='get_orders', data={'request': date, 'response': serializer.data})
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=WalkOrderSerializer, responses={201: WalkOrderSerializer})
@api_view(['POST'])
def create_order(request):
    data = request.data
    try:
        walk_datetime = parse_datetime(data['walk_datetime'])
        
        if walk_datetime.time() < time(7, 0) or walk_datetime.time() >= time(23, 0):
            return Response({'error': 'Прогулка может начинаться с 7 утра до 11 вечера.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if walk_datetime.minute not in [0, 30]:
            return Response({'error': 'Прогулка может начинаться только в начале или в половине часа.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if walk_datetime.minute == 30 and walk_datetime.time() >= time(22, 30):
            return Response({'error': 'Прогулка не может закончиться позже 11 вечера.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if WalkOrder.objects.filter(walk_datetime__range=(walk_datetime, walk_datetime + timedelta(minutes=30))).exists():
            return Response({'error': 'На это время уже назначена прогулка.'}, status=status.HTTP_400_BAD_REQUEST)
        
        walker = data.get('walker')
        if walker and WalkOrder.objects.filter(walk_datetime__range=(walk_datetime, walk_datetime + timedelta(minutes=30)), walker=walker).exists():
            return Response({'error': 'Этот выгульщик уже назначен на прогулку в это время.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = WalkOrder.objects.create(
            apartment_number=data['apartment_number'],
            pet_name=data['pet_name'],
            pet_breed=data['pet_breed'],
            walk_datetime=walk_datetime,
            walker=walker
        )
        APICall.objects.create(method='create_order', data={'request': data, 'response': {'id': order.id}})
        serializer = WalkOrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Если исключение возникло до определения data, используем пустой словарь
        APICall.objects.create(method='create_order', data={'request': data or {}, 'response': {'error': str(e)}})
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)