from reportlab.lib import colors 
from reportlab.lib.pagesizes import letter 
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Image,Spacer
from v1.models import *
from rest_framework.views import APIView
from v1.services.trans import PdfService as ps
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from core.permissions import IsManager,IsStaff
from django.templatetags.static import static
from django.contrib.staticfiles import finders



class AllTransactionPDF(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager]


    def get(self,request,*args,**kwargs):
        transactions = TransactionAPI.objects.filter(status = 'Approved')
        if transactions:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="transactions_report.pdf"' 
            doc = SimpleDocTemplate(response, pagesize=letter) 
            elements = []
            logo_path = finders.find('unnamed.png')
            if not logo_path: 
                return Response({'error': 'Logo not found in static files.'}, status=status.HTTP_404_NOT_FOUND) 
            logo = Image(logo_path, width=100, height=50)
            elements.append(logo) 
            elements.append(Spacer(1, 20))
            data = [['Transaction ID', 'Name', 'Phone', 'Email', 'Amount', 'Transaction Date']] 
            for transaction in transactions: 
                data.append([ 
                    transaction.transaction_id, 
                    transaction.name, 
                    transaction.phone, 
                    transaction.email, 
                    f"{transaction.amount:.2f}", 
                    transaction.transaction_date.strftime('%Y-%m-%d') 
                ])
            table = Table(data) 
            style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]) 
            table.setStyle(style) 
            elements.append(table) 
            doc.build(elements) 
            return response
        return Response({'error':'Transactions not found!!'},status=status.HTTP_404_NOT_FOUND)



class TransactionPDF(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsManager]


    def get(self,request,txn_id):
        transaction = ps.get_obj_pdf(txn_id)
        if transaction:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="transactions_report_view.pdf"' 
            doc = SimpleDocTemplate(response, pagesize=letter) 
            elements = []

            logo_path = finders.find('unnamed.png')
            if not logo_path: 
                return Response({'error': 'Logo not found in static files.'}, status=status.HTTP_404_NOT_FOUND) 
            logo = Image(logo_path, width=100, height=50)
            elements.append(logo) 
            elements.append(Spacer(1, 20))

            
            data = [ 
                ['Transaction ID', transaction.transaction_id], 
                ['Name', transaction.name], 
                ['Phone', transaction.phone], 
                ['Email', transaction.email], 
                ['Amount', f"{transaction.amount:.2f}"], 
                ['Transaction Date', transaction.transaction_date.strftime('%Y-%m-%d')] 
            ]
            table = Table(data) 
            style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]) 
            table.setStyle(style) 
            elements.append(table) 
            doc.build(elements) 
            return response
        return Response({'error':'Transaction not found!!'},status=status.HTTP_404_NOT_FOUND)