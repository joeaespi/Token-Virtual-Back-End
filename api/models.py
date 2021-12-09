from django.db import models

# Create your models here.
class Usuario(models.Model):
    usuario = models.CharField(
        unique=True, max_length=50, blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    tokena = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'
        
class TokenLog(models.Model):
    usuario = models.ForeignKey(
        'Usuario', models.DO_NOTHING, db_column='usuario', blank=True, null=True)
    anteriortoken = models.CharField(max_length=500, blank=True, null=True)
    actualtoken = models.CharField(max_length=500, blank=True, null=True)
    mensaje = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tokenlog'