from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Bucketlist(models.Model):
    """Stores Bucketlists."""

    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % (self.name)


class Item(models.Model):
    """Stores Bucketlist Items"""

    name = models.CharField(max_length=30)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)
    bucketlist = models.ForeignKey(Bucketlist, on_delete=models.CASCADE)

    def __unicode__(self):
        return '%s' % (self.name)


# class User(models.Model, UserMixin):
#     """Stores users"""

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(128))
#     online = db.Column(db.Boolean)
#     bucketlists = db.relationship('Bucketlist')

#     def hash_password(self, password):
#         """Encrypt user password."""
#         self.password = pwd_context.encrypt(password)

#     def verify_password(self, password):
#         """Verify user password."""
#         return pwd_context.verify(password, self.password)

#     def generate_auth_token(self):
#         """Generate authentication token."""
#         data = [str(self.id), self.password]
#         return login_serializer.dumps(data)
