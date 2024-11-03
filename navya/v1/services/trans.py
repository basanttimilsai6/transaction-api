from v1.models import *

class TransService:
    @staticmethod
    def get_obj(txn_id):
        try:
            return TransactionAPI.objects.get(transaction_id=txn_id)
        except TransactionAPI.DoesNotExist:
            return None
        

class PdfService:
    @staticmethod
    def get_obj_pdf(txn_id):
        try:
            return TransactionAPI.objects.get(transaction_id=txn_id,status = 'Approved')
        except TransactionAPI.DoesNotExist:
            return None