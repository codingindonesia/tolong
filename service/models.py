from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Invitation(models.Model):
    fullname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

class Case(models.Model):

    class Meta:
        ordering = ['-reported_date']

    # http://study.com/academy/lesson/child-abuse-and-neglect-4-major-types-characteristics-effects.html
    CASE_TYPES = (
        ('Phy', 'Physical Abuse'),
        ('N', 'Neglect'),
        ('Psy', 'Psycological Abuse'),
        ('S', 'Sexual Abuse'),
    )

    SUSPECTS = (
        (1,'Orang tua'),
        (2, 'Bapak'),
        (3, 'Ibu'),
        (4, 'Saudara Kandung'),
        (5, 'Lainnya'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    reported_by = models.CharField(max_length=200, null=True, blank= True)
    reported_date = models.DateTimeField()
    phone = models.CharField(max_length=200, null= True, blank= True)
    email = models.CharField(max_length=200, null= True, blank= True)
    location = models.CharField(max_length=400, null=True, blank= True)
    longitude = models.CharField(max_length=220, null=True, blank=True)
    latitude = models.CharField(max_length=220, null=True, blank=True)
    has_response = models.BooleanField(default= False)
    case_type = models.CharField(max_length=20, null= True, blank= True)
    suspect = models.CharField(max_length=200,null=True, blank=True)
    victim = models.CharField(max_length=200,null=True,blank=True)

class Responder(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null= True, blank= True)
    email = models.CharField(max_length=200, null= True, blank= True)
    cell_phone = models.CharField(max_length=200, null= True, blank= True)
    longitude = models.CharField(max_length=200, null= True, blank= True)
    latitude = models.CharField(max_length=200, null= True, blank=True)
    user = models.ForeignKey(User)

class Response(models.Model):
    case_id = models.ForeignKey(Case, related_name= 'responses')
    response_date = models.DateTimeField(auto_now_add= True)
    responder = models.ForeignKey(Responder)
    response_report = models.TextField()
    validity = models.IntegerField()
    severity_level = models.IntegerField()