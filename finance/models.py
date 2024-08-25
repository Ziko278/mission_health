from datetime import date

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from admin_site.models import CountryModel
from cryptography.fernet import Fernet
from student.models import CohortModel, StudentsModel
from training.models import CourseModel, EnrollmentModel


class CurrencyModel(models.Model):
    """"""
    name = models.CharField(max_length=100, unique=True)
    symbol = models.TextField(blank=True, null=True)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)
    exchange_rate = models.FloatField()
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=10, choices=STATUS, default='active')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def is_default(self):
        finance_setting = FinanceSettingModel.objects.first()
        if finance_setting:
            if finance_setting.default_currency.id == self.id:
                return True
        return False


class FinanceSettingModel(models.Model):
    default_currency = models.ForeignKey(CurrencyModel, on_delete=models.SET_NULL, null=True)
    auto_confirm_online_payment = models.BooleanField(blank=True, default=True)
    allow_part_payment = models.BooleanField(blank=True, default=True)
    minimum_payment = models.FloatField(default=10)
    current_access_payment = models.FloatField(default=50)


class BankAccountModel(models.Model):
    currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True, blank=True)
    bank_name = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    use_global = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return "{} - {}".format(self.bank_name.title(), self.account_name.title())

    def save(self, *args, **kwargs):
        if not self.country:
            self.country = self.currency.country
        super(BankAccountModel, self).save(*args, **kwargs)


class OnlinePaymentPlatformModel(models.Model):
    currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE)
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True, blank=True)
    PLATFORM = (
        ('paypal', 'PAYPAL'), ('paystack', 'PAYSTACK')
    )
    platform = models.CharField(max_length=50, choices=PLATFORM)
    name = models.CharField(max_length=250)
    public_key = models.CharField(max_length=250)
    private_key = models.CharField(max_length=250)
    email = models.EmailField()
    vat = models.FloatField(default=0.0)
    callback_url = models.URLField(blank=True, null=True)
    webhook_url = models.URLField(blank=True, null=True)
    key = models.CharField(max_length=250, blank=True, null=True)
    STATUS = (
        ('active', 'ACTIVE'), ('inactive', 'INACTIVE')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='active', blank=True)
    use_global = models.BooleanField(default=False, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name.upper()

    def save(self, *args, **kwargs):
        if not self.country:
            self.country = self.currency.country

        key = Fernet.generate_key().decode()
        fernet = Fernet(key)
        self.key = key
        self.public_key = fernet.encrypt(self.public_key.encode()).decode()
        self.private_key = fernet.encrypt(self.private_key.encode()).decode()
        super(OnlinePaymentPlatformModel, self).save(*args, **kwargs)


class PaymentIDGeneratorModel(models.Model):
    last_id = models.IntegerField()
    last_payment_id = models.CharField(max_length=100, null=True, blank=True)
    STATUS = (
        ('s', 'SUCCESS'), ('f', 'FAIL')
    )
    status = models.CharField(max_length=10, choices=STATUS, blank=True, default='f')


class TrainingPaymentModel(models.Model):
    enrollment = models.ForeignKey(EnrollmentModel, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey(CourseModel, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(StudentsModel, on_delete=models.SET_NULL, null=True, blank=True)
    cohort = models.ForeignKey(CohortModel, on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.FloatField()
    currency = models.ForeignKey(CurrencyModel, on_delete=models.CASCADE, related_name='currency')
    default_currency = models.ForeignKey(CurrencyModel, on_delete=models.SET_NULL, blank=True, null=True)
    value_in_currency = models.FloatField(blank=True, null=True)
    PAYMENT_METHOD = (('online', 'ONLINE'), ('offline', 'OFFLINE'))
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    payment_proof = models.FileField(blank=True, null=True, upload_to='finance/fee_payment')
    payment_date = models.DateField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True, null=True)
    platform_reference = models.CharField(max_length=100, blank=True, null=True)
    account = models.ForeignKey(BankAccountModel, on_delete=models.SET_NULL, blank=True, null=True)

    STATUS = (
        ('pending', 'PENDING'), ('confirmed', 'CONFIRMED'), ('declined', 'DECLINED')
    )
    status = models.CharField(max_length=20, choices=STATUS, default='pending', blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self.generate_payment_id()
        self.cohort = self.student.cohort
        if not self.enrollment:
            try:
                enrollment = EnrollmentModel.objects.get(student=self.student, course=self.course, status='active')
            except ObjectDoesNotExist:
                enrollment = EnrollmentModel.objects.create(student=self.student, course=self.course,
                                                            cohort=self.student.cohort)
                enrollment.save()
        if self.enrollment and not self.course:
            self.course = self.enrollment.course
        if not self.payment_date:
            self.payment_date = date.today()
        super(TrainingPaymentModel, self).save(*args, **kwargs)

    def generate_payment_id(self):
        last_payment = PaymentIDGeneratorModel.objects.filter().last()
        if last_payment:
            payment_id = str(int(last_payment.last_id) + 1)
        else:
            payment_id = str(1)
        while True:
            gen_id = payment_id
            payment_id = 'trn' + '/' + self.student.cohort.cohort_id + '/' + payment_id.rjust(4, '0')
            payment_exist = TrainingPaymentModel.objects.filter(reference=payment_id).first()
            if not payment_exist:
                break
            else:
                payment_id = str(int(gen_id) + 1)

        generate_id = PaymentIDGeneratorModel.objects.create(last_id=gen_id, last_payment_id=payment_id,
                                                             status='f')
        generate_id.save()

        return payment_id

