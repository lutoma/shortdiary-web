from django.db import migrations
from django.core.files.base import ContentFile
from os.path import basename
from django_q.tasks import async_task


def forwards(apps, schema_editor):
	Post = apps.get_model('diary', 'Post')
	print('\nMigrating images to PostImage model')

	for post in Post.objects.exclude(image=''):
		file = ContentFile(post.image.read())
		file.name = basename(post.image.name)

		post_image = post.images.create(image=file)
		async_task('diary.tasks.create_post_image_thumbnail', post_image)
		print('.', end='')

	print()


class Migration(migrations.Migration):

	dependencies = [
		('diary', '0011_postimage'),
	]

	operations = [
		migrations.RunPython(forwards),
	]
