from django.shortcuts import render
from rest_framework.views import APIView
from v1.models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.permissions import IsManager,IsStaff
from v1.services.trans import TransService as ts


class TransactionCreateList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff]

    def post(self,request):
        data = request.data
        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Data Uploaded Successfully!!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        tranasctions = TransactionAPI.objects.all()
        serializer = TransactionSerializer(tranasctions,many=True)
        return Response(serializer.data, status = status.HTTP_200_OK)



class TransactionAction(APIView):
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            self.permission_classes = [IsManager]
        else:
            self.permission_classes = [IsStaff]
        return super().get_permissions()


    def get(self,request,txn_id):
        trans = ts.get_obj(txn_id)
        if trans:
            serializer = TransactionSerializer(trans)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message':'Data Not Found!!'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self,request,txn_id):
        trans = ts.get_obj(txn_id)
        if trans:
            serializer = TransactionSerializer(trans, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Data Not Found!!'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self,request,txn_id):
        trans = ts.get_obj(txn_id)
        if trans:
            serializer = TransactionSerializer(trans, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'Data Not Found!!'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,txn_id,*args,**kwargs):
        trans = ts.get_obj(txn_id)
        if trans:
            trans.delete()
            return Response({'message':'Data Deleted!!'}, status=status.HTTP_200_OK)
        return Response({'message':'Data Not Found!!'}, status=status.HTTP_404_NOT_FOUND)
