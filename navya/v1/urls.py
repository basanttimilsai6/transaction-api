from django.urls import path
from v1.views import *
from v1.generate_pdf import *


urlpatterns = [
    path('transactions', TransactionCreateList.as_view(), name='transaction'),
    path('transactions/<str:txn_id>', TransactionAction.as_view(), name='transaction-update-get'),
]


urlpatterns += [
    path('pdf/transactions', AllTransactionPDF.as_view(), name='transaction-all-pdf'),
    path('pdf/transactions/<str:txn_id>', TransactionPDF.as_view(), name='transaction-pdf-view'),
]