from datetime import datetime

from django.contrib import admin, messages
from django.utils.html import format_html

from interview.models import Candidate
from jobs.models import Job, Resume
import logging

logger = logging.getLogger(__name__)

# Register your models here.

class JobAdmin(admin.ModelAdmin):
    # 定义在列表页展示哪些字段
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'create_date', 'modified_date')

    # 不显示
    exclude = ('creator', 'create_date', 'modified_date')

    def save_model(self, request, obj, form, change):
        """在保存模型前做一个操作"""
        obj.creator = request.user
        super().save_model(request, obj, form, change)


def enter_interview_process(modeladmin, request, queryset):
    candidate_names = ""
    for resume in queryset:
        candidate = Candidate()
        # 把 简历 对象中的所有属性拷贝到 候选人 对象中:
        candidate.__dict__.update(resume.__dict__)
        candidate.created_date = datetime.now()
        candidate.modified_date = datetime.now()
        candidate_names = candidate.username + "," + candidate_names
        candidate.creator = request.user.username
        candidate.save()
    messages.add_message(request, messages.INFO, '候选人: %s 已成功进入面试流程' % (candidate_names))


enter_interview_process.short_description = u"进入面试流程"


class ResumeAdmin(admin.ModelAdmin):
    actions = (enter_interview_process,)

    #
    def image_tag(self, obj):

        if obj.picture:
            return format_html('<img src="{}" style="width:100px;height:80px;"/>'.format(obj.picture.url))
        return ""

    image_tag.allow_tags = True
    image_tag.short_description = 'Image'

    list_display = (
        'username','applicant', 'city', 'apply_position', 'bachelor_school', 'master_school', 'major','image_tag', 'created_date')

    readonly_fields = ('applicant', 'created_date', 'modified_date',)

    fieldsets = (
        (None, {'fields': (
            "applicant", ("username", "city", "phone"),
            ("email", "apply_position", "born_address", "gender",), ("picture", "attachment",),
            ("bachelor_school", "master_school"), ("major", "degree"), ('created_date', 'modified_date'),
            "candidate_introduction", "work_experience", "project_experience",)}),
    )

    def save_model(self, request, obj, form, change):
        obj.applicant = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Job, JobAdmin)
admin.site.register(Resume, ResumeAdmin)
