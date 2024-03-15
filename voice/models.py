from django.db import models
from django.contrib.auth.models import User
# Create your models here.
COMMENT_CHOICES = (
    ('grammar', 'Grammatik yoki imloviy xatolik'),
    ('negative', "Xaqoratli so'zlar yoki gaplar"),
    ('otherlanguage', 'Boshqa tillar yoki sozlar qo\'shilgan'),
    ('difficult', 'Qiyin so\'zlar yoki gaplar'),
    ('other', 'Boshqa'),
)

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        abstract = True
        
        
class Sentence(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sentences', null=True, blank=True, verbose_name='User')
    body = models.CharField(max_length=355, verbose_name='Sentence')
    is_read = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Matn'
        verbose_name_plural = 'Matnlar'
        
    def __str__(self):
        return self.body
    

class Voice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='voices', null=True, blank=True, verbose_name='User')
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='voices')
    file = models.FileField(upload_to='voices', verbose_name='Voice')
    class Meta:
        verbose_name = 'Ovoz'
        verbose_name_plural = 'Ovozlar'
        
    def __str__(self):
        return self.sentence.body
    
    

    
class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True, verbose_name='User')
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name='Comment')
    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        
    def __str__(self):
        return self.body
    
    
class CheckVoice(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='check_voices', null=True, blank=True, verbose_name='User')
    voice = models.ForeignKey(Voice, on_delete=models.CASCADE, related_name='check_voices')
    is_checked = models.BooleanField(default=False)
    class Meta:
        verbose_name = 'Ovozni tekshirish'
        verbose_name_plural = 'Ovozni tekshirishlar'
        
    def __str__(self):
        return self.voice.sentence.body
    


class SavedVoiceGroupId(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='saved_voice_groups', null=True, blank=True, verbose_name='User')
    group = models.CharField(max_length=255, verbose_name='Telegram group id')
    class Meta:
        verbose_name = 'Saqlangan ovozlar guruhi'
        verbose_name_plural = 'Saqlangan ovozlar guruhlari'
        
    def __str__(self):
        return self.user.username