from django.contrib import admin
from .models import Post, Category
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        skip_unchanged = True
        report_skipped = False
        exclude = ('id',)
        import_id_fields = ('name',)

class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
admin.site.register(Post)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(User)
# admin.site.register(UserProfile)
# admin.site.register(SubscriptionOrder)
# admin.site.register(EventOrder)

