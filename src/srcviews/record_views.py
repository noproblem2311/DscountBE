
from rest_framework import viewsets
from rest_framework import permissions
from ..models import VideoTranscription
from src.srcserializers.record_serializer import VideoTranscriptionSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary.uploader
import assemblyai
import requests
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from src.helper.get_token import get_token_from_request
from src.helper.getuser import get_user_from_token
# Cấu hình API Key của AssemblyAI
assemblyai_api_key = "e6c7de9fe7a540c38165563ed2e3ae98"
@csrf_exempt
def handle_video(request):
    if request.method == 'POST':
        video_chunk = request.FILES.get('chunks')
        note = request.POST.get('note')
        token = get_token_from_request(request)
        user = get_user_from_token(token)
        
        if video_chunk:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'webcam_{current_time}'
            # Đọc nội dung của chunk video
            video_content = video_chunk.read()

            # Tải lên Cloudinary
            try:
                upload_result = cloudinary.uploader.upload(
                    video_content,
                    resource_type='video',
                    public_id=file_name,
                )

                video_url = upload_result.get('secure_url')
                if video_url:
                    # Tạo yêu cầu transcribe tới AssemblyAI
                    transcript = transcribe_video(assemblyai_api_key, video_url)
                    # VideoTranscription.create(video_url, transcript, datetime.now(), datetime.now()
                    VideoTranscription.objects.create(note= note,video_url=video_url, transcript=transcript, user=user)
                    return JsonResponse({'status': 'success', 'url': video_url, 'transcript': transcript, 'user': user.id})

            except Exception as e:
                print(e)  # In lỗi ra console để debug
                return JsonResponse({'status': 'error', 'message': 'Upload failed'})

        else:
            return JsonResponse({'status': 'error', 'message': 'No file received'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def transcribe_video(api_key, video_url):
    headers = {
        "authorization": api_key,
        "content-type": "application/json"
    }
    # Thêm tham số language_code vào payload
    payload = {
        "audio_url": video_url,
        "language_code": "vi"  # Đặt mã ngôn ngữ là tiếng Việt
    }
    response = requests.post('https://api.assemblyai.com/v2/transcript', json=payload, headers=headers)
    if response.status_code == 200:
        transcript_id = response.json()['id']
        # Poll for the transcript result
        while True:
            check_response = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcript_id}', headers=headers)
            if check_response.json()['status'] == 'completed':
                return check_response.json()['text']
            elif check_response.json()['status'] == 'failed':
                return "Transcription failed"
    else:
        return response.json()['message']





class VideoTranscriptionViewSet(viewsets.ModelViewSet):
    queryset = VideoTranscription.objects.all()
    serializer_class = VideoTranscriptionSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        This view should return a list of all the video transcriptions
        for the currently authenticated user.
        """
        return VideoTranscription.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a video transcription instance by its ID.
        """
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a video transcription instance.
        """
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def list_by_user(self, request):
        """
        Return a list of all video transcriptions for a specific user.
        """
        token = get_token_from_request(request)
        user = get_user_from_token(token)
        user_id = user.id
        if user_id is not None:
            transcriptions = VideoTranscription.objects.filter(user_id=user_id)
            serializer = self.get_serializer(transcriptions, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "User ID is required."}, status=status.HTTP_400_BAD_REQUEST)
