from .choices import ProductStatus
from .exceptions import DomainError
from .models import ProductMedia

def publish_product(product):
    """
    Check if the product has images or videos; if it doesn't, it cannot be published.
    """
    if not product.media.exists():
        raise DomainError("A product needs to have at least one media platform to be published.")
    product.status = ProductStatus.PUBLISHED
    product.save(update_fields=["status"])
    return product


def archive_product(product):
    """
    Archive a product
    """
    if product.status == ProductStatus.ARCHIVED:
        raise DomainError("Product is already archived.")
    
    product.status = ProductStatus.ARCHIVED
    product.save(update_fields=["status"])
    return product


def remove_product_media(product_media):
    product = product_media.product

    if product.media.count() <= 1:
        raise DomainError(
            "A product must have at least one media item."
        )

    product_media.delete()