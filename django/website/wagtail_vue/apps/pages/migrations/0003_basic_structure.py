# Generated by Django 3.2.10 on 2021-12-09 21:45

from django.db import migrations, models
import django.db.models.deletion
import pages.streamfields
import wagtail.contrib.routable_page.models
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.documents.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailredirects', '0006_redirect_increase_max_length'),
        ('wagtailforms', '0004_add_verbose_name_plural'),
        ('wagtailcore', '0066_collection_management_permissions'),
        ('pages', '0002_alter_flexpage_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('abstract', wagtail.core.fields.RichTextField(blank=True, help_text='Chapter abstract', null=True)),
            ],
            options={
                'verbose_name': 'Chapter',
                'verbose_name_plural': 'Chapters',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('abstract', wagtail.core.fields.RichTextField(blank=True, help_text='Post abstract', null=True)),
                ('body', wagtail.core.fields.StreamField([('RichTextBlock', pages.streamfields.RichTextBlock()), ('ButtonBlock', wagtail.core.blocks.StructBlock([('text', wagtail.core.blocks.CharBlock(required=True)), ('page', wagtail.core.blocks.PageChooserBlock(required=False)), ('document', wagtail.documents.blocks.DocumentChooserBlock(required=False)), ('external_link', wagtail.core.blocks.CharBlock(required=False))])), ('ImageBlock', wagtail.core.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock(required=True)), ('caption', wagtail.core.blocks.CharBlock(required=False)), ('align', wagtail.core.blocks.ChoiceBlock(choices=[('left', 'Left'), ('right', 'Right'), ('full', 'Full')]))])), ('ImageGalleryBlock', wagtail.core.blocks.StructBlock([('images', wagtail.core.blocks.ListBlock(wagtail.core.blocks.StructBlock([('ImageBlock', wagtail.images.blocks.ImageChooserBlock(required=True))])))]))], blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Post',
                'verbose_name_plural': 'Posts',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('subtitle', models.CharField(blank=True, help_text='Publication subtitle', max_length=200, null=True)),
                ('abstract', wagtail.core.fields.RichTextField(blank=True, help_text='Publication abstract', null=True)),
                ('intro', wagtail.core.fields.RichTextField(blank=True, help_text='Publication introduction', null=True)),
            ],
            options={
                'verbose_name': 'Publication',
                'verbose_name_plural': 'Publications',
            },
            bases=(wagtail.contrib.routable_page.models.RoutablePageMixin, 'wagtailcore.page'),
        ),
        migrations.DeleteModel(
            name='FlexPage',
        ),
    ]
