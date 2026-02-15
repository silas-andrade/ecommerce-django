from pathlib import Path
import uuid

def review_media_path(instance, filename):
    ext = Path(filename).suffix
    filename = f"{uuid.uuid4()}{ext}"

    return (
        f"products/{instance.review.product.id}/"
        f"reviews/{instance.review.id}/"
        f"{filename}"
    )