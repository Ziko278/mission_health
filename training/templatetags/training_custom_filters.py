from django import template
from student.models import StudentsModel
from datetime import date, timedelta
from finance.models import *
from django.db.models import Sum

register = template.Library()


@register.filter
def can_view_course(course, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    cohort = student.cohort

    enrollment = EnrollmentModel.objects.filter(student=student, course=course, status='active').first()
    #
    payments = TrainingPaymentModel.objects.filter(enrollment=enrollment, student=student, cohort=cohort,status='confirmed')
    amount_paid = payments.aggregate(total_sum=Sum('amount_paid'))['total_sum']

    if not amount_paid:
        amount_paid = 0

    finance_setting = FinanceSettingModel.objects.first()
    if finance_setting.allow_part_payment:
        if amount_paid >= round(course.amount * finance_setting.current_access_payment/100):
            return True
    else:
        if amount_paid >= course.amount:
            return True

    return False
