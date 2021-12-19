# -*- coding: utf-8 -*-
"""Page models."""
from django.db import models
from django.db.models.fields import BooleanField, CharField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.embeds.blocks import EmbedBlock
from wagtail_references.blocks import ReferenceChooserBlock

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

from grapple.helpers import register_query_field
from grapple.models import (
    GraphQLBoolean,
    GraphQLString,
    GraphQLStreamfield,
    GraphQLCollection,
)

class Publication(Page):
    """The publication class"""

    # parent_page_types = []
    subpage_types = ['pages.Chapter','pages.Post']
    parent_page_types = ['wagtailcore.page']

    subtitle = CharField(max_length=200, null=True, blank=True, help_text="Publication subtitle")
    abstract = RichTextField(
        null=True, blank=True,
        help_text='Publication abstract',
        features=[],
    )

    staged = BooleanField(
        'staged',
        help_text="Content is shown in staged area",
        default=False)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('subtitle', classname="full"),
        FieldPanel('abstract', classname="full"),
    ]

    settings_panels = [
        FieldPanel('staged')
    ] + Page.settings_panels

    graphql_fields = [
        GraphQLString("subtitle"),
        GraphQLString("abstract"),
        GraphQLBoolean("staged"),
    ]

    # Export fields over the API
    api_fields = [
        APIField('live'),
        APIField('draft_title'),
        APIField('subtitle'),
        APIField('abstract'),
        APIField('staged'),
    ]

    def get_admin_display_title(self):
        if self.staged:
            return f"🌏 ▽ {self.draft_title}"
        else:
            return f"🌏 ▷ {self.draft_title}"

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
        help_text='Chapter abstract',
        features=[],
    )

    staged = BooleanField(
        'staged',
        help_text="Content is shown in staged area",
        default=False)

    content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('abstract'),
    ]

    settings_panels = [
        FieldPanel('staged')
    ] + Page.settings_panels

    graphql_fields = [
        GraphQLString("abstract"),
        GraphQLBoolean("staged"),
    ]

    def get_admin_display_title(self):
        if self.staged:
            return f"📒 ▽ {self.draft_title}"
        else:
            return f"📒 ▷ {self.draft_title}"

    class Meta:
        """Meta information."""

        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"


class Post(Page):
    """The post class"""

    parent_page_types = ['pages.Chapter','pages.Publication']
    subpage_types = []

    abstract = RichTextField(
        null=True, blank=True,
        help_text='Post abstract',
        features=[],
    )
    body = StreamField([
        ('EmbedBlock', EmbedBlock()),
        ('RichTextBlock', RichTextBlock(
            features=["h4","h5","h6","bold","ol","ul","hr","document-link","italic","link","reference-link"],
        )),
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
        # GraphQLCollection(
        #     GraphQLForeignKey,
        #     "related_references",
        #     "wagtail_references.Reference"
        # ),
        GraphQLBoolean("staged"),
    ]

    def get_admin_display_title(self):
        if self.staged:
            return f"📄 ▽ {self.draft_title}"
        else:
            return f"📄 ▷ {self.draft_title}"

    class Meta:
        """Meta information."""

        verbose_name = "Post"
        verbose_name_plural = "Posts"

@register_query_field('setting')
@register_setting(icon="cog")
class PageSettings(BaseSetting):

    impressum_footer = models.TextField(
        null=True, blank=True,
        help_text='Impressum in the footer',
    )
    facebook = models.URLField(
        help_text='Your Facebook page URL')
    twitter = models.CharField(
        max_length=255, help_text='Your Twitter username, without the @')
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @')
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL')

    graphql_fields = [
        GraphQLString("impressum_footer"),
        GraphQLString("facebook"),
        GraphQLString("twitter"),
        GraphQLString("instagram"),
        GraphQLString("youtube"),
    ]
