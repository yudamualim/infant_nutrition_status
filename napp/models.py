from django.db import models

class Person(models.Model):
  NIK = models.CharField(max_length=16)
  Nama = models.CharField(max_length=50)
  Berat_Badan = models.FloatField()
  Tinggi_Badan = models.FloatField()
  Usia_Saat_UKur = models.IntegerField()
  Jenis_Kelamin = models.CharField(max_length=1)
  Status_Gizi_Balita = models.CharField(max_length=20)
  