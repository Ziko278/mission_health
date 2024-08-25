from django.urls import path
from finance.views import *

urlpatterns = [
    path('currency/create', CurrencyCreateView.as_view(), name='currency_create'),
    path('currency/index', CurrencyListView.as_view(), name='currency_index'),
    path('currency/<int:pk>/edit', CurrencyUpdateView.as_view(), name='currency_edit'),
    path('currency/<int:pk>/delete', CurrencyDeleteView.as_view(), name='currency_delete'),
    
    path('finance-setting/create', FinanceSettingCreateView.as_view(), name='finance_setting_create'),
    path('finance-setting/<int:pk>/detail', FinanceSettingDetailView.as_view(), name='finance_setting_detail'),
    path('finance-setting/<int:pk>/edit', FinanceSettingUpdateView.as_view(), name='finance_setting_edit'),

    path('bank-account/create', BankAccountCreateView.as_view(), name='bank_account_create'),
    path('bank-account/index', BankAccountListView.as_view(), name='bank_account_index'),
    path('bank-account/<int:pk>/edit', BankAccountUpdateView.as_view(), name='bank_account_edit'),
    path('bank-account/<int:pk>/delete', BankAccountDeleteView.as_view(), name='bank_account_delete'),

    path('online-payment-method/create', OnlinePaymentPlatformCreateView.as_view(), name='online_payment_create'),
    path('online-payment-method/index', OnlinePaymentPlatformListView.as_view(), name='online_payment_index'),
    path('online-payment-method/<int:pk>/detail', OnlinePaymentPlatformDetailView.as_view(), name='online_payment_detail'),
    path('online-payment-method/<int:pk>/edit', OnlinePaymentPlatformUpdateView.as_view(), name='online_payment_edit'),
    path('online-payment-method/<int:pk>/delete', OnlinePaymentPlatformDeleteView.as_view(), name='online_payment_delete'),

    path('training/payment/select-student', TrainingPaymentSelectStudentView.as_view(), name='training_select_student'),
    path('training/payment/<int:student_pk>/create', TrainingPaymentCreateView.as_view(), name='training_payment_create'),
    path('training/payment/index', TrainingPaymentListView.as_view(), name='training_payment_index'),
    path('training/payment/<int:pk>/detail', TrainingPaymentDetailView.as_view(), name='training_payment_detail'),

    path('fee/payment/get-student-by-reg-number', fee_get_class_students_by_reg_number,
         name='fee_get_class_students_by_reg_number'),
]

