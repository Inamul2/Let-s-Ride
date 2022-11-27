import datetime
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RiderData
from .serializers import RiderSerializer


class Create(APIView):
    def post(self, request):
        try:
            if not request.data:
                return Response({'Status': 'Failed', "Error": "Request have no keys"}, status=status.HTTP_204_NO_CONTENT)


            if "From" not in request.data:
                return Response({'Status': 'Failed', "Error": "'From' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)

            if "To" not in request.data:
                return Response({'Status': 'Failed', "Error": "'To' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)

            if "dateandtime" not in request.data:
                return Response({'Status': 'Failed', "Error": "'dateandtime' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)

            if "medium" not in request.data:
                return Response({'Status': 'Failed', "Error": "'medium' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['medium'].lower() not in ['car', 'bus', 'train']:
                    return Response({'Status': 'Failed', "Error": "medium should be any of these - 'bus', 'car', 'train'"}, status=status.HTTP_404_NOT_FOUND)
                    
            if "assets" not in request.data:
                return Response({'Status': 'Failed', "Error": "'assets' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if not re.search('^[0-9]+$', request.data['assets']):
                    return Response({'Status': 'Failed', "Error": "assets should be a number"}, status=status.HTTP_404_NOT_FOUND)

            From = request.data['From']
            To = request.data['To']
            try:
                dateandtime = str(datetime.datetime.strptime(request.data['dateandtime'],'%Y-%m-%d %H:%M:%S'))
            except:
                return Response({'Status': 'Failed', "Message": "date and time not given in correct format"}, status=status.HTTP_400_BAD_REQUEST)


            medium = request.data['medium'].lower()
            assets = request.data['assets']
            RiderData.objects.create(From=From, To=To, dateandtime=dateandtime, medium=medium, assets=int(assets))
            serialize = RiderSerializer(request.data)
            return Response({'Status': 'Success', "Message": "Rider data has been added successfully",
                             "Rider Data": serialize.data}, status=status.HTTP_200_OK)

        except Exception:
            return Response({'Status': 'Failed', "Error": "Some Internal Error Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)