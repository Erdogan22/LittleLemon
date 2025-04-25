from django.shortcuts import render
from django.http import HttpResponse
import rest_framework
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from .models import Menu, Booking
from rest_framework.decorators import api_view
from .serializers import MenuItemSerializer, BookingSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet


# Create your views here.
def index(request):
    return render(request, 'index.html', {'title': 'Home Page'})



class MenuItemsView(ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    
    

class SingleMenuItemView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuItemSerializer
    

class BookingViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class UserViewSet(rest_framework.viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer
   permission_classes = [permissions.IsAuthenticated] 