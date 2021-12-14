# -*- coding: utf-8 -*-
"""Page models."""
from django.db import models
from django.db.models.fields import BooleanField, CharField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.images.api.fields import ImageRenditionField
from wagtail.core.fields import StreamField, RichTextField
from wagtail.embeds.blocks import EmbedBlock

from wagtail.contrib.routable_page.models import RoutablePageMixin

from .streamfields import (
    RichTextBlock,
    ImageBlock,
    ButtonBlock,
    ContentBlock,
    ImageGalleryBlock,
    CallToActionBlock,
)

from wagtail.api import APIField

from grapple.models import (
    GraphQLBoolean,
    GraphQLString,
    GraphQLStreamfield,
)


class Publication(Page):
    """The publication class"""

    # parent_page_types = []
    subpage_types = ['pages.Chapter']
    # parent_page_types = ['wagtailcore.Page']

    subtitle = CharField(max_length=200, null=True, blank=True, help_text="Publication subtitle")
    abstract = RichTextField(
        null=True, blank=True,
        help_text='Publication abstract'
    )

    intro = RichTextField(
        null=True, blank=True,
        help_text='Publication introduction'
    )

    staged = BooleanField(
        'staged',
        help_text="Content is shown in staged area",
        default=False)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full"),
        FieldPanel('abstract', classname="full"),
        FieldPanel('intro', classname="full"),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('staged')
    ]

    graphql_fields = [
        GraphQLString("subtitle"),
        GraphQLString("abstract"),
        GraphQLString("intro"),
        GraphQLBoolean("staged"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('live'),
        APIField('draft_title'),
        APIField('subtitle'),
        APIField('abstract'),
        APIField('intro'),
        APIField('staged'),
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

    staged = BooleanField(
        'staged',
        help_text="Content is shown in staged area",
        default=False)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('abstract'),
    ]

    settings_panels = Page.settings_panels + [
        FieldPanel('staged')
    ]

    graphql_fields = [
        GraphQLString("abstract"),
        GraphQLBoolean("staged"),
    ]

    api_fields = [
        APIField('abstract'),
        APIField('staged'),
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
        ('EmbedBlock', EmbedBlock()),
        ('RichTextBlock', RichTextBlock(
            features=["h4","h5","h6","bold","ol","ul","hr","document-link","italic","link","snippet-link","snippet-embed"],
        )),
        ('ButtonBlock', ButtonBlock()),
        ('ImageBlock', ImageBlock()),
        ('ImageGalleryBlock', ImageGalleryBlock()),
        # ('CallToActionBlock', CallToActionBlock()),
    ], null=True, blank=True)

    staged = BooleanField(
        'staged',
        help_text="Content is shown in staged area",
        default=False)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('abstract', classname="full"),
        StreamFieldPanel('body'),
    ]

    settings_panels = [
        FieldPanel('staged')
    ] + Page.settings_panels

    graphql_fields = [
        GraphQLString("abstract"),
        GraphQLStreamfield("body"),
        GraphQLBoolean("staged"),
    ]

    api_fields = [
        APIField('abstract'),
        APIField('body'),
        APIField('staged'),
    ]

    class Meta:
        """Meta information."""

        verbose_name = "Post"
        verbose_name_plural = "Posts"
