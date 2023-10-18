from django.db import models
from boards.views import Board
import datetime

# Create your models here.
class Posts(models.Model):
    board_id = models.ForeignKey(Board,on_delete=models.DO_NOTHING)
    post_content = models.TextField(max_length=500)
    post_date = models.DateField(auto_now_add=True,blank=True,null=True)
    post_time = models.TimeField(auto_now_add=True,blank=True,null=True)
