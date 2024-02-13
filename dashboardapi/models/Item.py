from django.db import models
import uuid
from .Category import Category
from .Tag import Tag

class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    sku = models.TextField()
    name = models.TextField()
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    in_stock = models.DecimalField(decimal_places=3, max_digits=100)
    available_stock = models.DecimalField(decimal_places=3, max_digits=100)
    tags = models.ManyToManyField(to=Tag)
    
    def to_front_end_dict (self):
        # Customized conversion of Model to JSON
        return {
            "id": str(self.id),
            "sku": self.sku,
            "name": self.name,
            "category": self.category.name,
            "in_stock": self.in_stock,
            "available_stock": self.available_stock,
            "tags": [
                tag.name for tag in self.tags.all()
            ]
        }
