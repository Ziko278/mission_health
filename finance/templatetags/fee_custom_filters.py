from django import template
from student.models import StudentsModel
from datetime import date, timedelta
from finance.models import *
from django.db.models import Sum

register = template.Library()


@register.filter
def get_amount_paid(enrollment, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    cohort = student.cohort

    payments = TrainingPaymentModel.objects.filter(enrollment=enrollment, student=student, cohort=cohort,
                                                   status='confirmed')
    amount_paid = payments.aggregate(total_sum=Sum('amount_paid'))['total_sum']

    if not amount_paid:
        return 0.0
    return amount_paid

