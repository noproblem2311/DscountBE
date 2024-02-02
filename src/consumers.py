import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .utils import combine_video_chunks, upload_to_cloudinary

class VideoUploadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass  # Xử lý khi kết nối bị đóng

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']
        
        if message_type == 'start':
            # Xử lý khi bắt đầu ghi
            pass
        elif message_type == 'chunk':
            # Lưu trữ và kết hợp chunk
            pass
        elif message_type == 'end':
            # Kết hợp các chunk và tải lên Cloudinary
            video_path = combine_video_chunks(text_data_json['session_id'])
            video_url = upload_to_cloudinary(video_path)
            await self.send(text_data=json.dumps({'type': 'video_url', 'url': video_url}))
