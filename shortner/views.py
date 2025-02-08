import traceback

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse


from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg.utils import swagger_auto_schema

from core.utils import render_htmx
from core import constants
from domain.shortner.client import ShortnerClient
from .serializer import URLSerializer


class RedirectToLongURLView(APIView):
    def get(self, request: HttpRequest, short_code: str):
        try:
            # Get the original long url from the database
            url_entry = ShortnerClient.get_long_url(short_code=short_code)
            return HttpResponseRedirect(redirect_to=url_entry.long_url)
        except ObjectDoesNotExist as e:
            print(f"Invalid short code. Error: {e}")
            traceback.print_exc()
            return Response(data={}, status=404)


class URLViews(ViewSet):

    @action(
        methods=["get"],
        detail=False,
        url_path="home",
        url_name="home",
    )
    def home(self, request: HttpRequest):
        context = {"shorten_url": reverse("shortner-shorten")}
        return render_htmx(
            request=request,
            template_name=constants.INPUT_TMPL,
            context=context,
        )

    @swagger_auto_schema(
        request_body=URLSerializer,
        responses={201: "Success"},
    )
    @action(
        methods=["post"],
        detail=False,
        url_path="shorten",
        url_name="shorten",
    )
    def shorten_url(self, request: HttpRequest):
        try:
            # implement business logic
            serializer = URLSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Check if long url already exists
            short_code = ShortnerClient.get_or_create_short_url(
                long_url=serializer.validated_data["long_url"]
            )

            """
            Return JSON response
            return Response(
                data={"short_url": f"http://localhost:8000/{short_code}"},
                status=201,
            )
            """

            # Return html response
            render_htmx(request=request, template_name=constants.INPUT_TMPL)
        except ValidationError as e:
            print(f"Invalid request body. Error: {e}")
            traceback.print_exc()
            return Response(data=e.detail, status=400)
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
