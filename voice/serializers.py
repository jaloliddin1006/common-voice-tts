from rest_framework import serializers

class AudioFileSerializer(serializers.Serializer):
    audio_file = serializers.FileField()
    sentence = serializers.CharField()
    sentence_id = serializers.IntegerField()