# -*- coding: utf-8 -*-
"""Page models."""
from django.db import models
from django.db.models.fields import CharField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.core.fields import StreamField, RichTextField

from wagtail.contrib.routable_page.models import RoutablePageMixin

from .streamfields import (
    RichTextBlock,
    ImageBlock,
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

class Publication(RoutablePageMixin, Page):
    """The publication class"""

    # parent_page_types = []
    subpage_types = ['pages.Chapter']
    parent_page_types = ['wagtailcore.Page']

    subtitle = CharField(max_length=200, null=True, blank=True, help_text="Publication subtitle")
    abstract = RichTextField(
        null=True, blank=True,
        help_text='Publication abstract'
    )

    intro = RichTextField(
        null=True, blank=True,
        help_text='Publication introduction'
    )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full"),
        FieldPanel('abstract', classname="full"),
        FieldPanel('intro', classname="full"),
    ]

    graphql_fields = [
        GraphQLString("subtitle"),
        GraphQLString("abstract"),
        GraphQLString("intro"),
    ]

    class Meta:
        """Meta information."""

        verbose_name = "Publication"
        verbose_name_plural = "Publications"

class Chapter(Page):
    """The chapter class"""

    parent_page_types = ['pages.Publication']
    subpage_types = ['pages.Post']

    abstract = RichTextField(
        null=True, blank=True,
        help_text='Chapter abstract'
    )

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('abstract'),
    ]

    graphql_fields = [
        GraphQLString("abstract"),
    ]

    class Meta:
        """Meta information."""

        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

class Post(Page):
    """The post class"""

    parent_page_types = ['pages.Chapter']
    subpage_types = []

    abstract = RichTextField(
        null=True, blank=True,
        help_text='Post abstract'
    )
    body = StreamField([
        ('RichTextBlock', RichTextBlock()),
        ('ButtonBlock', ButtonBlock()),
        ('ImageBlock', ImageBlock()),
        ('ImageGalleryBlock', ImageGalleryBlock()),
        # ('CallToActionBlock', CallToActionBlock()),
    ], null=True, blank=True)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('abstract', classname="full"),
        StreamFieldPanel('body'),
    ]

    graphql_fields = [
        GraphQLString("abstract"),
        GraphQLStreamfield("body"),
    ]

    class Meta:
        """Meta information."""

        verbose_name = "Post"
        verbose_name_plural = "Posts"
