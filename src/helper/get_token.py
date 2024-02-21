def get_token_from_request(request):
    # Lấy giá trị của header Authorization từ request
    authorization_header = request.headers.get('Authorization')

    if authorization_header and 'Bearer' in authorization_header:
        # Tách lấy token từ chuỗi "Bearer [token]"
        token = authorization_header.split('Bearer ')[1]
        return token
    else:
        # Trả về None nếu không tìm thấy hoặc không đúng định dạng token
        return None
