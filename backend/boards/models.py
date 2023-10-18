from django.db import models
import datetime
# Create your models here.

class Board(models.Model):
    board_name = models.CharField(max_length=50,unique=True)
    board_desc = models.CharField(max_length=1000,blank=True)
    
    def __str__(self) -> str:
        return self.board_name