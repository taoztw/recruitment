# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Continents(models.Model):
    """大陆 洲"""
    name = models.CharField(max_length=16, blank=True, null=True, db_comment='英文名')
    cname = models.CharField(max_length=16, blank=True, null=True, db_comment='中文名')
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'continents'

    def __str__(self):
        return self.cname if self.name else ""


class Countries(models.Model):
    """国家"""
    id = models.SmallAutoField(primary_key=True)
    continent_id = models.IntegerField(blank=True, null=True)
    # continent_id = models.ForeignKey(Continents, db_column='countryid', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=3, db_comment='地区代码')
    name = models.CharField(max_length=50, blank=True, null=True, db_comment='名称')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    full_cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'countries'

    def __str__(self):
        return self.cname if self.name else ""


class Area(models.Model):
    # country_id = models.IntegerField(blank=True, null=True)
    country_id = models.ForeignKey(Countries, db_column='country_id', null=True, on_delete=models.SET_NULL)
    code = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area'

    def __str__(self):
        return self.cname if self.name else ""


class States(models.Model):
    id = models.SmallAutoField(primary_key=True)
    # country_id = models.SmallIntegerField(db_comment='所属国家代码')
    country_id = models.ForeignKey(Countries, db_column='country_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=255, blank=True, null=True)
    area_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'states'

    def __str__(self):
        return self.cname if self.name else ""


class Cities(models.Model):
    id = models.SmallAutoField(primary_key=True)
    # state_id = models.SmallIntegerField(db_comment='所属州省代码')
    state_id = models.ForeignKey(States, db_column='state_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=255, blank=True, null=True)
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=9, db_comment='地区代码')

    class Meta:
        managed = False
        db_table = 'cities'

    def __str__(self):
        return self.cname if self.name else ""


class Regions(models.Model):
    """地区"""
    id = models.SmallAutoField(primary_key=True)
    # city_id = models.SmallIntegerField(db_comment='所属城市代码')
    city_id = models.ForeignKey(Cities, db_column='city_id', null=True, on_delete=models.SET_NULL)
    code = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    cname = models.CharField(max_length=50, blank=True, null=True, db_comment='名称')
    lower_name = models.CharField(max_length=255, blank=True, null=True)
    code_full = models.CharField(max_length=12, db_comment='地区代码')

    class Meta:
        managed = False
        db_table = 'regions'

    def __str__(self):
        return self.cname if self.cname else ""
