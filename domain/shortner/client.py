import string
from django.db import transaction

from shortner.models import URLCounter, URLs

BASE62_ALPHABETS = string.ascii_letters + string.digits
MAX_COUNTER_6 = 62**6 - 1


class ShortnerClient:
    """
    A URL Shortner client to encode long urls into base62 format
    Retries long url associates with short codes
    """

    @staticmethod
    def encode_base62(number, length):
        """
        Encode decimal number to base 62 string with a fixed length
        """
        result = []
        while number:
            number, remainder = divmod(number, 62)
            result.append(BASE62_ALPHABETS[remainder])

        # Padding with 'a'
        while len(result) < length:
            result.append(BASE62_ALPHABETS[0])
        return "".join(result[::-1])

    @staticmethod
    def get_next_short_code():
        """
        Generates the next short code based on a counter
        """
        # TODO: If counter reaches limit for 6 chars, overrride length
        with transaction.atomic():
            counter_instance, _ = URLCounter.objects.select_for_update().get_or_create( # noqa
                id=1
            )
            counter = counter_instance.counter

            short_code = ShortnerClient.encode_base62(number=counter, length=6)

            # Atomic update to prevent race condition
            counter_instance.counter = counter + 1
            counter_instance.save()

        return short_code

    @staticmethod
    def get_or_create_short_url(long_url: str):
        """
        Returns existing short url or creates a new one
        """
        existing_long_url = URLs.objects.filter(long_url=long_url).first()
        if existing_long_url:
            return existing_long_url.short_code

        # Generate a new short code
        short_code = ShortnerClient.get_next_short_code()

        # Create and save the new short code
        URLs.objects.create(long_url=long_url, short_code=short_code)

        return short_code

    @staticmethod
    def get_long_url(short_code: str):
        """
        Returns long url associated with the short code
        Raises `model.ObjectDoesNotExist` if not found
        """

        long_url = URLs.objects.get(short_code=short_code)
        return long_url
