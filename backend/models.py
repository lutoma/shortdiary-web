from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
	id = fields.UUIDField(pk=True)
	name = fields.CharField(max_length=255)
	email = fields.CharField(max_length=255)

	# Salt used during derivation of ephemeral key from login password
	ephemeral_key_salt = fields.CharField(max_length=22, null=True)

	# User master key, encrypted using ephemeral key
	master_key = fields.CharField(max_length=64, null=True)

	# Nonce used during encryption of master key
	master_key_nonce = fields.CharField(max_length=32, null=True)

	# Output of crypto_pwhash_str on second half of ephemeral key
	password = fields.CharField(max_length=100)

	# Old Django password for users that have not logged in since the migration
	legacy_password = fields.CharField(max_length=500, null=True)

	def __str__(self):
		return self.name


User_Pydantic = pydantic_model_creator(User, name='User')


class Post(Model):
	id = fields.UUIDField(pk=True)
	#author = fields.ForeignKeyField('models.User', related_name='posts')
	date = fields.DateField()

	# Encryption format used by this post. 0 = unencrypted (legacy posts from
	# before client-side encryption used to exist and use has not converted
	# yet), 1 = current format, all other values reserved for future use
	format_version = fields.IntField(default=1)

	# Nonce used for post encryption
	nonce = fields.CharField(max_length=32, null=True)
	data = fields.BinaryField()

#    class Meta:
#		unique_together=(('author', 'date'), )

	def __str__(self):
		return self.name


Post_Pydantic = pydantic_model_creator(Post, name='Post')
PostIn_Pydantic = pydantic_model_creator(Post, name='PostIn', exclude_readonly=True)
