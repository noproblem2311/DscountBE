from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary.uploader

from datetime import datetime

@csrf_exempt
def handle_video(request):
    
    if request.method == 'POST':
        video_chunk = request.FILES.get('chunks')
        if video_chunk:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'webcam_{current_time}'
            print("type video", type(video_chunk))
            # Đọc nội dung của chunk video
            video_content = video_chunk.read()

            # Tải lên Cloudinary sử dụng nội dung của video
            try:
                upload_result = cloudinary.uploader.upload(
                    video_content,
                    resource_type='video',
                    public_id=file_name,
                    format='mp4'  # Đảm bảo bạn chỉ định đúng định dạng nếu cần
                )

                if upload_result.get('secure_url'):
                    return JsonResponse({'status': 'success', 'url': upload_result['secure_url']})
            except Exception as e:
                print(e)  # In lỗi ra console để debug
                return JsonResponse({'status': 'error', 'message': 'Upload failed'})

        else:
            return JsonResponse({'status': 'error', 'message': 'No file received'})
    