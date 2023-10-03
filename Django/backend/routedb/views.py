from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from django.http import JsonResponse
# Create your views here.

class AllRoomView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        
        return Response('lol',status=200)

class RoomAccessibleView(APIView):
    
    def get(self, request, room_id):
        try:
            room = Room.objects.get(id=room_id)            
        except:
            return JsonResponse({'message':'no room?'},status=404)
        serializer = RoomSerializer(room)
        return Response(serializer.data, status=200)
    
    #make better get request
    #post request?
    #get request for all rooms


        