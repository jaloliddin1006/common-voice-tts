from django.urls import path
from . import views


app_name = 'voice'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('voice/', views.VoiceRecordPageView.as_view(), name='voice'),
    path('save-voice/', views.SaveVoiceView.as_view(), name='save-voice'),
    path('save-voice2/', views.VoiceRecordView, name='save-voice'),
    path('get_next_sentence/', views.GetNextSentenceAPIView.as_view(), name='sentence'),
    path('sentence-error-comment/', views.ErrorCommentView.as_view(), name='sentence-error-comment'),
    ]
