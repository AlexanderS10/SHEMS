from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.core.validators import MinValueValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password=password, **extra_fields)
    
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('An email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

class Customers(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=30, null=False, blank=False)
    billing_unit_number = models.SmallIntegerField(null=False, blank=False)
    billing_street_number = models.SmallIntegerField(null=False, blank=False)
    billing_street_name = models.CharField(max_length=30, null=False, blank=False)
    billing_city = models.CharField(max_length=30, null=False, blank=False)
    billing_state = models.CharField(max_length=2, null=False, blank=False)
    billing_zipcode = models.CharField(max_length=5, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    # Any other fields or methods you want to include...

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "billing_unit_number", "billing_street_number", "billing_street_name",'billing_city', "billing_state", "billing_zipcode"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class ServiceLocations(models.Model):
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
    unitNumber = models.SmallIntegerField(validators=[MinValueValidator(0)])
    streetNumber = models.SmallIntegerField(validators=[MinValueValidator(1)])
    streetName = models.CharField(max_length=30)
    sstate = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=5)
    serviceStart = models.DateField()
    squareFootage = models.DecimalField(max_digits=10, decimal_places=2)
    noBedrooms = models.SmallIntegerField(validators=[MinValueValidator(0)])
    noOccupants = models.SmallIntegerField(validators=[MinValueValidator(1)])
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(unitNumber__gte=0), name='unitNumber'),
            models.CheckConstraint(check=models.Q(streetNumber__gt=0), name='streetNumber'),
            models.CheckConstraint(check=models.Q(noOccupants__gt=0), name='noOccupants'),
            models.CheckConstraint(check=models.Q(noBedrooms__gte=0), name='noBedrooms'),
        ]

class Models(models.Model):
    modelNumber = models.SmallIntegerField(primary_key=True)
    model_property = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(modelNumber__isnull=False), name='non_null_modelNumber'),
        ]

class Devices(models.Model):
    deviceID = models.AutoField(primary_key=True)
    locationID = models.ForeignKey('ServiceLocations', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=30)
    modelNumber = models.ForeignKey('Models', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(deviceID__isnull=False), name='non_null_deviceID'),
        ]
    
class Events(models.Model):
    eventID = models.AutoField(primary_key=True)
    deviceID = models.ForeignKey('Devices', on_delete=models.CASCADE)
    event_label = models.CharField(max_length=30)
    datetimestamp = models.DateTimeField()
    event_value = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(eventID__isnull=False), name='non_null_eventID'),
        ]

class EnergyUsage(models.Model):
    deviceID = models.ForeignKey('Devices', on_delete=models.CASCADE)
    Energy = models.DecimalField(max_digits=10, decimal_places=2)
    EnergyTimestamp = models.DateTimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['deviceID', 'EnergyTimestamp'], name='unique_device_energy_timestamp'),
        ]

class EnergyPrices(models.Model):
    dateTime = models.DateTimeField()
    zipcode = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=8, decimal_places=4)
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='positive_price'),
            models.UniqueConstraint(fields=['dateTime', 'zipcode'], name='unique_datetime_zipcode'),
        ]
