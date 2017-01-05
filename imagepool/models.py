from django.db import models

from django.contrib.auth.models import User

class ImagePool(models.Model):
    user = models.ForeignKey(User)
    uploaded = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name="Загружен")
    image = models.ImageField(upload_to='imagepool/%Y/%m', verbose_name='Изображение')

    class Meta:
        ordering = ['user', '-uploaded']
        verbose_name = 'изображение'

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super(ImagePool, self).delete(*args, **kwargs)
