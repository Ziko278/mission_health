from django.urls import path
from student_portal.views import *

urlpatterns = [
    path('register', student_signup_view, name='student_signup'),
    path('register/complete', student_signup_done_view, name='register_done'),
    path('register/<int:pk>/send-activation-mail', send_activation_mail, name='activation_mail'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate_account_view, name='activate_account'),
    path('login', student_signin_view, name='student_login'),
    path('logout', student_sign_out_view, name='student_logout'),
    path('', StudentDashboardView.as_view(), name='student_dashboard'),
    path('courses', StudentCourseDashboardView.as_view(), name='student_course_dashboard'),
    path('courses/select-enrollment', StudentEnrollDashboardView.as_view(), name='student_enroll_dashboard'),
    path('courses/<int:pk>/enroll', StudentEnrollmentCreateView.as_view(), name='student_enroll'),
    path('courses/enrollment/<int:pk>', StudentEnrollmentDetailView.as_view(), name='student_enroll_detail'),
    path('courses/lesson/<int:pk>', StudentLessonDetailView.as_view(), name='student_lesson_detail'),
    path('courses/lesson-material/<int:pk>', StudentLessonMaterialDetailView.as_view(), name='student_lesson_material_detail'),

    path('fees', StudentFeeDashboardView.as_view(), name='student_fee_dashboard'),
    path('fees/select-payment-method', StudentSelectPaymentMethodView.as_view(), name='select_payment_method'),
    path('fees/<int:pk>/payment-amount', student_payment_amount, name='student_payment_amount'),
    path('fees/paystack-payment-done', paystack_payment_done, name='paystack_payment_done'),
    path('fees/<int:pk>/paystack/<int:paystack_pk>', PayWithPaystackView.as_view(), name='pay_with_paystack'),
    
    path('fees/paypal-payment-done', paypal_payment_done, name='paypal_payment_done'),
    path('fees/<int:pk>/paypal/<int:paypal_pk>', PayWithPaypalView.as_view(), name='pay_with_paypal'),

]

