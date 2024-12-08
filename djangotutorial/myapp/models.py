from django.db import models

class Expense(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    amount = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.category}) - ${self.amount:.2f} on {self.date}"