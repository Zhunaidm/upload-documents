import uuid


def generate_presigned_url():
    return uuid.uuid4()

def is_valid_url(url):
    try:
        uuid.UUID(str(url))
        return True
    except ValueError:
        return False