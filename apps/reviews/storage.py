from pathlib import Path

def review_media_path(instance, filename):
    ext = Path(filename).suffix
    return f"reviews/{instance.review.id}/{instance.id}{ext}"