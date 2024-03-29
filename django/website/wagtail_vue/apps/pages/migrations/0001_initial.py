# Generated by Django 3.1.7 on 2021-04-05 17:00

from django.db import migrations, models
import django.db.models.deletion
import pages.streamfields
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0060_fix_workflow_unique_constraint'),
        ('wagtailimages', '0023_add_choose_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('headline', models.TextField(blank=True, help_text='An optional subtitle', max_length=140, null=True)),
                ('body', wagtail.core.fields.RichTextField(blank=True, help_text='Article body', null=True)),
                ('content', wagtail.core.fields.StreamField([('ContentBlock', wagtail.core.blocks.StructBlock([('content', wagtail.core.blocks.StreamBlock([('RichTextBlock', pages.streamfields.RichTextBlock()), ('ButtonBlock', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=True)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_link', wagtail.core.blocks.CharBlock(required=False))])), ('ImageBlock', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('align', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full', 'Full')]))]))]))])), ('ButtonBlock', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=True)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_link', wagtail.core.blocks.CharBlock(required=False))])), ('ImageGalleryBlock', wagtail.core.blocks.StructBlock([('images', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('ImageBlock', wagtail.images.blocks.ImageChooserBlock(required=True))])))])), ('CallToActionBlock', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(required=False)), ('text', wagtail.core.blocks.RichTextBlock(features=['h2', 'h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'link'], required=False)), ('buttons', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=True)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_link', wagtail.core.blocks.CharBlock(required=False))], required=False), default=[]))]))], blank=True, null=True)),
                ('banner_image', models.ForeignKey(help_text='An optional banner image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=('wagtailcore.page',),
        ),
    ]
