from django.db import models
from django.contrib.auth.models import User
from api.utils import sendTransaction
import hashlib

# Post Model define fields
class Post(models.Model):

    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    hash = models.CharField(max_length=32, default=None, null=True)
    txId = models.CharField(max_length=66, default=None, null=True)

    # function to validate posts on blockchain
    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()
