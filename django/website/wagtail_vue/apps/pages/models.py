# -*- coding: utf-8 -*-
"""Page models."""
from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.core.fields import StreamField, RichTextField

from .streamfields import (
    ButtonBlock,
    ContentBlock,
    ImageGalleryBlock,
    CallToActionBlock,
)

from grapple.models import (
    GraphQLImage,
    GraphQLString,
    GraphQLStreamfield,
)

class FlexPage(Page):
    """A flexible page class."""

    # template = "cms/pages/home_page.html"
    subpage_types = ['pages.FlexPage']

    headline = models.TextField(
        max_length=140, blank=True, null=True,
        help_text="An optional subtitle"
    )
    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="An optional banner image",
    )
    body = RichTextField(
        null=True, blank=True,
        help_text='Article body'
    )
    content = StreamField([
        ('ContentBlock', ContentBlock()),
        ('ImageGalleryBlock', ImageGalleryBlock()),
        ('CallToActionBlock', CallToActionBlock()),
    ], null=True, blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('headline'),
        FieldPanel('body'),
        ImageChooserPanel('banner_image'),
        StreamFieldPanel('content'),
    ]

    graphql_fields = [
        GraphQLString("headline"),
        GraphQLString("body"),
        GraphQLImage("banner_image"),
        GraphQLImage("banner_image_thumbnail", serializer=ImageRenditionField("fill-100x100", source="banner_image")),
        GraphQLStreamfield("content"),
    ]

    class Meta:
        """Meta information."""

        verbose_name = "Page"
        verbose_name_plural = "Pages"
