from django import template
from django.shortcuts import get_object_or_404

from student.models import StudentsModel
from datetime import date, timedelta
from finance.models import *
from django.db.models import Sum

from training.models import ProgressModel, LessonMaterialModel, LessonModel

register = template.Library()


@register.filter
def can_view_course(course, student_id):
    student = StudentsModel.objects.get(pk=student_id)
    cohort = student.cohort

    enrollment = EnrollmentModel.objects.filter(student=student, course=course, status='active').first()
    #
    payments = TrainingPaymentModel.objects.filter(student=student, cohort=cohort,status='confirmed')
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


@register.filter
def lesson_progress(lesson, student_id):
    progress = 75
    return "{} %".format(progress)


@register.filter
def lesson_material_progress(material, student_id):
    student = get_object_or_404(StudentsModel, pk=student_id)
    progress = ProgressModel.objects.filter(student=student, cohort=student.cohort).first()
    if progress:
        if str(material.lesson.id) in progress.progress:
            if material.id in progress.progress[str(material.lesson.id)]:
                return True
    return False


@register.filter
def lesson_progress_percent(lesson, student_id):
    student = get_object_or_404(StudentsModel, pk=student_id)
    progress = ProgressModel.objects.filter(student=student, cohort=student.cohort).first()
    if progress:
        if str(lesson.id) in progress.progress:
            completed_lesson = len(progress.progress[str(lesson.id)])
            if completed_lesson > 0:
                material_count = LessonMaterialModel.objects.filter(lesson=lesson).count()
                return round((completed_lesson/material_count) * 100)
    return 0


@register.filter
def lesson_progress_percent_left(lesson, student_id):
    student = get_object_or_404(StudentsModel, pk=student_id)
    progress = ProgressModel.objects.filter(student=student, cohort=student.cohort).first()
    if progress:
        if str(lesson.id) in progress.progress:
            completed_lesson = len(progress.progress[str(lesson.id)])
            if completed_lesson > 0:
                material_count = LessonMaterialModel.objects.filter(lesson=lesson).count()
                return 100 - round((completed_lesson/material_count) * 100)
    return 0


@register.filter
def course_progress_percent(course, student_id):
    student = get_object_or_404(StudentsModel, pk=student_id)
    lesson_list = LessonModel.objects.filter(course=course.id)
    lesson_count = 0

    progress_count = 0
    for lesson in lesson_list:
        current_count = lesson_progress_percent(lesson, student.id)
        progress_count += current_count
        if current_count > 0:
            lesson_count += 1

    if lesson_count > 0:
        return round(progress_count/lesson_count)
    return 0


@register.filter
def course_progress_percent_left(course, student_id):
    student = get_object_or_404(StudentsModel, pk=student_id)
    lesson_list = LessonModel.objects.filter(course=course.id)
    lesson_count = 0

    progress_count = 0
    for lesson in lesson_list:
        current_count = lesson_progress_percent(lesson, student.id)
        progress_count += current_count
        if current_count > 0:
            lesson_count += 1

    if lesson_count > 0:
        return 100 - round(progress_count / lesson_count)
    return 0
