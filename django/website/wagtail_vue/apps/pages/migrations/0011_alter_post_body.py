# Generated by Django 3.2.10 on 2021-12-19 10:58

from django.db import migrations
import pages.streamfields
import wagtail.core.fields
import wagtail.embeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_pagesettings_impressum_footer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=wagtail.core.fields.StreamField([('EmbedBlock', wagtail.embeds.blocks.EmbedBlock()), ('RichTextBlock', pages.streamfields.RichTextBlock(features=['h4', 'h5', 'h6', 'bold', 'ol', 'ul', 'hr', 'document-link', 'italic', 'link', 'reference-link']))], blank=True, null=True),
        ),
    ]
