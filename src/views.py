from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cloudinary.uploader

import os
from datetime import datetime




@csrf_exempt
def handle_video(request):
    if request.method == 'POST':
        video_chunk = request.FILES.get('chunks')
        if video_chunk:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f'webcam_{current_time}.mp4'  

            upload_result = cloudinary.uploader.upload_large(
                video_chunk,
                resource_type='video',
                public_id=file_name
            )

            if upload_result.get('secure_url'):
                print(upload_result['secure_url'])
                return JsonResponse({'status': 'success', 'url': upload_result['secure_url']})
            else:
                return JsonResponse({'status': 'error', 'message': 'Upload failed'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No file received'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})