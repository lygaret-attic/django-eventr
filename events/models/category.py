from utils.models import BaseModel

class Category(BaseModel):

    class Meta:
        app_label = "events"
        ordering = ('name',)
        verbose_name_plural = "categories"
        
    def __unicode__(self):
        return self.name
