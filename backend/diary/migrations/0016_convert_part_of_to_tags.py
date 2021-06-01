from django.db import migrations


def forwards(apps, schema_editor):
    Post = apps.get_model('diary', 'Post')

    for post in Post.objects.exclude(part_of__exact='').exclude(part_of__isnull=True):
        post.tags = [post.part_of]
        post.save(update_fields=['tags'])


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0015_alter_post_tags'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
