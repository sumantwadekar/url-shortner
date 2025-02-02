from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import action


class URLViews(ViewSet):
    @action(
        methods=["post"],
        detail=False,
        url_path="shorten",
        url_name="shorten",
    )
    def shorten_url(self, request: HttpRequest):
        # implement business logic
        return Response(
            data={"message": "Hello world, you are in the url view"},
            status=201,
        )

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
