from django.contrib import admin
from running.models import Continents, Cities, Countries, States, Regions, Area


# Register your models here.



class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + [field.name for field in obj._meta.fields] + [field.name for field in obj._meta.many_to_many]

    # 展示所有list 数据库中的字段
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.concrete_fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

# 这里只做一个实例的情况
# Regionss 依赖 city city会很多

@admin.register(Regions)
class RegionsAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name', 'city_id')
    list_display = ('cname', 'name', 'code')
    autocomplete_fields = ['city_id']


@admin.register(Cities)
class CitiesAdmin(ReadOnlyAdmin):
    search_fields = ('cname', 'name')


# admin.site.register(Continents)
# # admin.site.register(Cities)
# admin.site.register(Countries)
# admin.site.register(States)
# admin.site.register(Area)
