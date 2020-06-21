def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user_id': user.id,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name
    }
