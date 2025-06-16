from django.db import models

class Master(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    client_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    master_id = models.IntegerField()
    service = models.CharField(max_length=100)
    date = models.CharField(max_length=20, blank=True, null=True, default='Не указана')
    time = models.CharField(max_length=20, blank=True, null=True, default='Не указано')
    status = models.CharField(max_length=20, default='новая')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Заявка #{self.id} - {self.client_name}"


