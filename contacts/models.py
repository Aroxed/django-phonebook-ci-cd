from mongoengine import Document, StringField, DateTimeField
from datetime import datetime, UTC

class Contact(Document):
    name = StringField(required=True, unique=True, max_length=100)
    phone = StringField(required=True, max_length=20)
    created_at = DateTimeField(default=lambda: datetime.now(UTC))
    updated_at = DateTimeField(default=lambda: datetime.now(UTC))

    def save(self, *args, **kwargs):
        self.updated_at = datetime.now(UTC)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    meta = {
        'ordering': ['name'],
        'collection': 'contacts'
    } 