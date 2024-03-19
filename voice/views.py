from django.shortcuts import render, get_object_or_404
from django.views import View, generic
from .models import Sentence, Voice, Comment, CheckVoice, COMMENT_CHOICES, SavedVoiceGroupId
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.db.models import Q
# Create your views here.
from .bot import send_audio
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from .serializers import AudioFileSerializer


class HomeView(generic.TemplateView):
    template_name = 'index.html'
    
    def get(self, request):
        return render(request, self.template_name)
   
    
class VoiceRecordPageView(generic.TemplateView):
    template_name = 'voice.html'
    
    @method_decorator(login_required)
    def get(self, request):
        sentence = Sentence.objects.all().filter(is_read=False).order_by('?').first()
        context = {
            'sentence': sentence,
            'comments': COMMENT_CHOICES,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        return render(request, self.template_name)
    

class SentenceView(APIView):
    pass


# class VoiceRecordView(APIView):
def VoiceRecordView(request):
    print(request)
    print(request.POST)
    print(request.FILES)
    return Response({"msg":"success"}, status=status.HTTP_200_OK)
        

class SaveVoiceView(APIView):
    
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'status': 'unauthorized',
                            "error": "Siz tizimga kirish qilmagansiz",
                             'url': '/accounts/login/'
                             
                             }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            audio_file = serializer.validated_data['audio_file']
            sentence = serializer.validated_data['sentence']
            sentence_id = serializer.validated_data['sentence_id']
        
            voice = Voice()
            voice.user = request.user
            voice.sentence = Sentence.objects.get(id=sentence_id)
            voice.save()
            
            file_name = f"voices/{voice.id}_{request.user.username}.wav"
            
            with open('media/'+file_name, 'wb+') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)
            voice.file = file_name
            voice.save()
                   
            # voice.sentence.is_read = True
            # voice.sentence.save()
            
            group_id = SavedVoiceGroupId.objects.filter(user=request.user).first().group
            
            send_audio(voice.file.url, voice.sentence.body, voice.sentence.id, group_id=group_id)
                    

            sentence = Sentence.objects.all().filter(is_read=False).order_by('?').first()
            data = {
                'status': True,
                "msg": "Audio muvaffaqiyatli saqlandi",
                'sentence': f"{sentence.body}",
                'sentence_id': f"{sentence.id}"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        context = {
            'status': False,
            "error": serializer.errors,
            'url': '/accounts/login/'
            }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        
class GetNextSentenceAPIView(APIView):
    def get(self, request):
        last_sentence_id = request.GET.get('sentence_id')
        print(last_sentence_id)
        if not request.user.is_authenticated:
            return Response({"error": "Siz tizimga kirish qilmagansiz",
                             'url': '/accounts/login/'
                             }, status=status.HTTP_401_UNAUTHORIZED)
        last_sentence_id = request.GET.get('sentence_id')
        
        sentences = Sentence.objects.filter(is_read=False)
        sentences_with_comments_count = sentences.annotate(comments_count=Count('comments'))
        # print(sentences_with_comments_count)
        sentence = sentences_with_comments_count.filter(Q(comments_count=0)).exclude(id=last_sentence_id).order_by('?').first()
        
        if sentence:
            data = {
                'sentence': f"{sentence.body}",
                'sentence_id': f"{sentence.id}"
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Yangi gap topilmadi"}, status=status.HTTP_404_NOT_FOUND)
    
    
    
class ErrorCommentView(APIView):
    def post(self, request):
        sentence_id = request.POST.get('sentence_id')
        comment = request.POST.get('error_type')
        if sentence_id and comment:
            sentence = get_object_or_404(Sentence, id=sentence_id)
            Comment.objects.create(user=request.user, sentence=sentence, body=comment)
            
            sentences = Sentence.objects.filter(is_read=False)
            sentences_with_comments_count = sentences.annotate(comments_count=Count('comments'))
            # print(sentences_with_comments_count)
            sentences_with_no_comments = sentences_with_comments_count.filter(Q(comments_count=0)).exclude(id=sentence_id).order_by('?').first()
            
       
            data = {
                'sentence': f"{sentences_with_no_comments.body}",
                'sentence_id': f"{sentences_with_no_comments.id}"
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Izoh yoki gapni topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
