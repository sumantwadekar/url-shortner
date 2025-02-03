import traceback

from rest_framework.viewsets import ViewSet
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from domain.shortner.client import ShortnerClient
from .serializer import URLSerializer


class URLViews(ViewSet):
    # TODO: Add swagger required fields decorator
    @action(
        methods=["post"],
        detail=False,
        url_path="shorten",
        url_name="shorten",
    )
    def shorten_url(self, request: HttpRequest):
        try:
            # implement business logic
            serializer = URLSerializer(request.data)
            serializer.is_valid(raise_exception=True)

            # Check if long url already exists
            short_code = ShortnerClient.get_or_create_short_url(
                long_url=serializer.long_url
            )
            return Response(
                data={"short_url": f"http://localhost:8000/{short_code}"},
                status=201,
            )
        except ValidationError as e:
            print(f"Invalid request body. Error: {e}")
            traceback.print_exc()
            return Response(data=serializer.error_messages, status=400)
        except Exception as e:
            print(f"Internal server error. {e}")
            traceback.print_exc()

    @action(
        methods=["get"],
        detail=False,
        url_path="urls",
        url_name="urls",
    )
    def get_all_urls(self, request: HttpRequest, pk=None):
        # implement business logic
        return Response(
            data={"message": "List of all shortned urls"},
            status=200,
        )
