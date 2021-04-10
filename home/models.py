from django.db import models

# Create your models here.


from django.contrib.auth import get_user_model


User=get_user_model()


class Notification(models.Model):
    user =  models.ForeignKey(User , on_delete=models.CASCADE)
    message = models.TextField(max_length=30,default="")
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-time']


