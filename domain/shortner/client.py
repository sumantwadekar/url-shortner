import string

from shortner.models import URLCouner, URLs

BASE62_ALPHABETS = string.ascii_letters + string.digits
MAX_COUNTER_6 = 62**6 - 1


class ShortnerClient:

    @staticmethod
    def encode_base62(number, length):
        """
        Encode decimal number to base 62 format
        """
        result = []
        while number:
            number, remainder = divmod(number, 62)
            result.append(BASE62_ALPHABETS[remainder])

        # Padding with 'a'
        while len(result) < length:
            result.append(BASE62_ALPHABETS[0])
        return ''.join(result[::-1])

    @staticmethod
    def get_next_short_code():
        # TODO: If counter reaches limit for 6 chars, overrride length
        counter_instance, _ = URLCouner.objects.get_or_create(id=1)
        counter = counter_instance.counter

        short_code = ShortnerClient.encode_base62(number=counter, length=6)
        counter_instance.counter = counter + 1
        counter_instance.save()

        return short_code

    @staticmethod
    def get_or_create_short_url(long_url: str):
        """
        Returns existing short url or creates a new one
        """
        existing_long_url = URLs.objects.get(long_url=long_url)
        if existing_long_url:
            return existing_long_url.short_code

        # Generate a new short code
        short_code = ShortnerClient.get_next_short_code()

        # Create and save the new short code
        URLs.objects.create(long_url=long_url, short_code=short_code)

        return short_code
