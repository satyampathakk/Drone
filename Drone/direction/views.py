from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status  # Import status codes
from .serializers import LocationSerializer,DestinationSerializer
from .models import *
from geopy.distance import geodesic
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class Monitor(APIView):
    def get(self, request, *args, **kwargs):
        data = LocationUpdate.objects.all()
        serializer = LocationSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        myreq=request.data.dict()
        user=request.user
        da=User.objects.get(username=user)

        myreq['user'] = da.pk
        try:
            # Try to get the existing location for the user
            location = LocationUpdate.objects.get(user=user)
            serializer = LocationSerializer(instance=location, data=myreq)
        except LocationUpdate.DoesNotExist:
            # If the location does not exist, create a new one
            serializer = LocationSerializer(data=myreq)
        if serializer.is_valid():
            serializer.save()
            try:
                data=UserDestination.objects.get(user=request.user)
                dlat = data.desired_lat
                dlong = data.desired_long
            except UserDestination.DoesNotExist:
                dlat = 0.0
                dlong = 0.0
            cdata=LocationUpdate.objects.get(user=user)
            clat=cdata.latitude
            clong=cdata.longitude
            current_location = (clat,clong)
            destination = (dlat,dlong)

        # Calculate distance and direction using geopy
            distance_km = geodesic(current_location, destination).kilometers

        # Determine relative directions
            lat_diff = destination[0] - current_location[0]
            lon_diff = destination[1] - current_location[1]

            if lat_diff > 0:
                lat_direction = "North"
            elif lat_diff < 0:
                lat_direction = "South"
            else:
                lat_direction = ""

            if lon_diff > 0:
                lon_direction = "East"
            elif lon_diff < 0:
                lon_direction = "West"
            else:
                lon_direction = ""

        # You can customize the response based on your needs
            response_data = {
                'distance': distance_km,
                'directions': f"Move {lat_direction} {lon_direction}."
        }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Direct(APIView):
    def get(self, request, *args, **kwargs):
        try:
            location_update = LocationUpdate.objects.get(user=request.user)
            serializer_location = LocationSerializer(location_update)
        except LocationUpdate.DoesNotExist:
            serializer_location = LocationSerializer(data={'latitude': 0.0, 'longitude': 0.0})

        try:
            user_destination = UserDestination.objects.get(user=request.user)
            serializer_destination = DestinationSerializer(user_destination)
            if serializer_destination.is_valid():
                pass
        except UserDestination.DoesNotExist:
            serializer_destination = DestinationSerializer(data={'desired_lat': 0.0, 'desired_long': 0.0})
            if serializer_destination.is_valid():
                pass

        return Response({'current': serializer_location.data, 'destination': serializer_destination.data})


    def post(self, request, *args, **kwargs):
        data=request.data.dict()
        da=User.objects.get(username=request.user)
        data['user']=da.pk
        user=request.user
        try:
            dest=UserDestination.objects.get(user=user)
            serializer=DestinationSerializer(instance=dest,data=data)
        except UserDestination.DoesNotExist :
            serializer = DestinationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Creteuser(APIView):
    authentication_classes = []
    permission_classes=[]
    def post(self, request, *args, **kwargs):
        user = request.data['username']
        password = request.data['password']

        if not User.objects.filter(username=user).exists():
            user = User.objects.create_user(username=user, password=password)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        else:
            existing_user = User.objects.get(username=user)
            existing_token, created = Token.objects.get_or_create(user=existing_user)
            return Response({'message': 'Username already exists, try another', 'token': existing_token.key})

    def get(self, request, *args, **kwargs):
        try:
            user = request.data['username']
            user1 = User.objects.get(username=user)
            token = Token.objects.get(user=user1)
            return Response({'token': token.key})
        except User.DoesNotExist:
            return Response({'error': 'No such user found'}, status=status.HTTP_403_FORBIDDEN)
