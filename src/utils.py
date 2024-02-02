import cloudinary.uploader

def upload_to_cloudinary(video_path):
    response = cloudinary.uploader.upload(video_path, resource_type = "", public_id = "", format = "")


def combine_video_chunks(session_id):
    pass