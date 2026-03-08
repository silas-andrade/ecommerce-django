from django.db import models


class PaymentStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    PAID = "paid", "Paid"
    FAILED = "failed", "Failed"
    REFUNDED = "refunded", "Refunded"


class PaymentMethod(models.TextChoices):
    PIX = "pix", "PIX"
    PAYPAL = "paypal", "PayPal"
    BANK_SLIP = "bank_slip", "Bank Slip"
    CARD = "card", "Card"


class CardType(models.TextChoices):
    CREDIT = "credit", "Credit"
    DEBIT = "debit", "Debit"


class CardBrand(models.TextChoices):
    VISA = "visa", "Visa"
    MASTERCARD = "mastercard", "MasterCard"
    ELO = "elo", "Elo"
    AMEX = "amex", "American Express"