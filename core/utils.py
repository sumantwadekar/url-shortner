from django.shortcuts import render
from django.http import HttpRequest


def render_jinja2(
    request: HttpRequest,
    template_name: str,
    context: dict = None,
    content_type=None,
    status=None,
    using=None,
):
    using = "jinja2"
    return render(
        request=request,
        template_name=template_name,
        context=context,
        using=using
    )


def render_htmx(
    request: HttpRequest,
    template_name: str,
    context=None,
    content_type=None,
    status=None,
    htmx_headers=None,
):
    response = render_jinja2(
        request=request,
        template_name=template_name,
        context=context,
    )
    return response
