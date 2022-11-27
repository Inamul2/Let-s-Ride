import datetime
import re
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RequesterData
from rider.models import RiderData
from .serializers import RequesterSerializer


class Request(APIView):
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

            if "asset_type" not in request.data:
                return Response({'Status': 'Failed', "Error": "'asset_type' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['asset_type'].lower() not in [ 'laptop', 'travel bag', 'package']:
                    return Response({'Status': 'Failed', "Error": "asset_type should be any of these - 'laptop', 'travel bag', 'package'"}, status=status.HTTP_404_NOT_FOUND)
                    
            if "asset_sensitivity" not in request.data:
                return Response({'Status': 'Failed', "Error": "'asset_sensitivity' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['asset_sensitivity'].upper() not in [ 'HIGHLY SENSITIVE', 'SENSITIVE', 'NORMAL']:
                    return Response({'Status': 'Failed', "Error": "asset_sensitivity should be any of these - 'HIGHLY SENSITIVE', 'SENSITIVE', 'NORMAL'"}, status=status.HTTP_404_NOT_FOUND)
            
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

            asset_sensitivity = request.data['asset_sensitivity'].lower()
            asset_type = request.data['asset_type'].lower()
            assets = request.data['assets']
            if datetime.datetime.now() > datetime.datetime.strptime(request.data['dateandtime'],'%Y-%m-%d %H:%M:%S'):
                RequesterData.objects.create(From=From, To=To, dateandtime=dateandtime, asset_type=asset_type, assets=int(assets), asset_sensitivity = asset_sensitivity, status="expired")
            else:    
                RequesterData.objects.create(From=From, To=To, dateandtime=dateandtime, asset_type=asset_type, assets=int(assets), asset_sensitivity = asset_sensitivity)
            serialize = RequesterSerializer(request.data)
            return Response({'Status': 'Success', "Message": "Your Request has been added successfully",
                             "Request": serialize.data}, status=status.HTTP_200_OK)

        except Exception:
            return Response({'Status': 'Failed', "Error": "Some Internal Error Occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class GetRequests(APIView):
    def post(self, request):
        try:
            data = list(RequesterData.objects.all().values_list())
            for da in data:
                if datetime.datetime.now() > datetime.datetime.strptime(da[3],'%Y-%m-%d %H:%M:%S'):
                    RequesterData.objects.filter(dateandtime__icontains=str(datetime.datetime.strptime(da[3],'%Y-%m-%d %H:%M:%S'))).update(status='expired')
        except:
            print(traceback.format_exc())

        try:
            if "status" in request.data:
                if "sort" in request.data:
                    if request.data['sort'] == "ASC" and request.data['status'].lower() == "pending":
                        data = RequesterData.objects.filter(status__icontains="pending").order_by('dateandtime')
                    elif request.data['sort'] == "ASC" and request.data['status'].lower() == "expired":
                        data = RequesterData.objects.filter(status__icontains="expired").order_by('dateandtime')
                    elif request.data['sort'] == "DESC" and request.data['status'].lower() == "pending":
                        data = RequesterData.objects.filter(status__icontains="pending").order_by('-dateandtime')
                    else:
                        data = RequesterData.objects.filter(status__icontains="expired").order_by('-dateandtime')


                else:
                    if request.data['status'].lower() == "pending":
                        data = RequesterData.objects.filter(status__icontains="pending")
                    else:
                        data = RequesterData.objects.filter(status__icontains="expired")
            else:
                if "sort" in request.data:
                    if request.data['sort'] == "ASC":
                        data = RequesterData.objects.all().order_by('dateandtime')
                    else:
                        data = RequesterData.objects.all().order_by('-dateandtime')


                else:
                    data = RequesterData.objects.all()


            serialize = RequesterSerializer(data, many=True)
            return Response({'Status': 'Success', "Message": "List of Requests retrieved Successfully",
                                "Requests": serialize.data}, status=status.HTTP_200_OK)
        except:
            return Response({'Status': 'Failed', "Message": "Some internal error occured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetMatchedRequests(APIView):
    def post(self, request):
        try:
            rider_data = list(RiderData.objects.all().values_list())
            request_data = list(RequesterData.objects.all().values_list())
            output = []
            for rider in rider_data:
                for req in request_data:
                    
                    if rider[1].lower() == req[1].lower() and rider[2].lower() == req[2].lower() and rider[3] == req[3]:
                        serialize = RequesterSerializer(RequesterData.objects.get(ID=req[0]))
                        output.append(serialize.data)
            return Response({'Status': 'Success', "Message": "List of all Matched Requests retrieved Successfully",
                                    "Requests": output}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'Status': 'Failed', "Message": "Some internal error occured" + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Apply(APIView):
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

            if "asset_type" not in request.data:
                return Response({'Status': 'Failed', "Error": "'asset_type' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['asset_type'].lower() not in [ 'laptop', 'travel bag', 'package']:
                    return Response({'Status': 'Failed', "Error": "asset_type should be any of these - 'laptop', 'travel bag', 'package'"}, status=status.HTTP_404_NOT_FOUND)
                    
            if "asset_sensitivity" not in request.data:
                return Response({'Status': 'Failed', "Error": "'asset_sensitivity' key is missing in the request"}, status=status.HTTP_404_NOT_FOUND)
            else:
                if request.data['asset_sensitivity'].upper() not in [ 'HIGHLY SENSITIVE', 'SENSITIVE', 'NORMAL']:
                    return Response({'Status': 'Failed', "Error": "asset_sensitivity should be any of these - 'HIGHLY SENSITIVE', 'SENSITIVE', 'NORMAL'"}, status=status.HTTP_404_NOT_FOUND)
            
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

            asset_sensitivity = request.data['asset_sensitivity'].lower()
            asset_type = request.data['asset_type'].lower()
            assets = request.data['assets']
            data = RequesterData.objects.filter(From=From, To=To, dateandtime=dateandtime, asset_type=asset_type, assets=int(assets), asset_sensitivity = asset_sensitivity).update(applied="Applied")
            serialize = RequesterSerializer(RequesterData.objects.get(From=From, To=To, dateandtime=dateandtime, asset_type=asset_type, assets=int(assets), asset_sensitivity = asset_sensitivity))
            return Response({'Status': 'Success', "Message": "You have applied for your request successfully",
                             "Request": serialize.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'Status': 'Failed', "Error": "Some Internal Error Occured" + str(e) + traceback.format_exc()}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        