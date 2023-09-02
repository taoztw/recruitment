from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from interview.dingtalk import send
from .tasks import test_send
from interview.models import Candidate
import csv
from datetime import datetime
import logging
from interview.candidate_fieldset import default_fieldsets, default_fieldsets_first, default_fieldsets_second
from jobs.models import Resume

logger = logging.getLogger(__name__)


# 定义导出的字段
exportable_fields = (
    'username', 'city', 'phone', 'bachelor_school', 'master_school', 'degree', 'first_result', 'first_interviewer_user',
    'second_result', 'second_interviewer_user', 'hr_result', 'hr_score', 'hr_remark', 'hr_interviewer_user')
# 定义导出的Action
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-candidates',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    writer = csv.writer(response)
    # 写入表头
    writer.writerow(
        [queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],
    )
    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    logger.info(" %s has exported %s candidate records" % (request.user.username, len(queryset)))
    logger.error(" %s has exported %s candidate records" % (request.user.username, len(queryset)))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'
export_model_as_csv.allowed_permissions = ("export",)


# 通知一面面试官面试
def notify_interviewer(modeladmin, request, queryset):
    candidates = ""
    interviewers = ""
    for obj in queryset:
        candidates = obj.username + ";" + candidates
        interviewers = obj.first_interviewer_user.username + ";" + interviewers
    # 这里的消息发送到钉钉， 或者通过 Celery 异步发送到钉钉
    # send(f"候选人 {candidates} 进入面试环节，亲爱的面试官，请准备好面试： {interviewers}")
    test_send.delay(f"候选人 {candidates} 进入面试环节，亲爱的面试官，请准备好面试： {interviewers}")
    # send_dingtalk_message.delay("候选人 %s 进入面试环节，亲爱的面试官，请准备好面试： %s" % (candidates, interviewers) )
    messages.add_message(request, messages.INFO, '已经成功发送面试通知')


notify_interviewer.short_description = u'通知一面面试官'
# 如果用户有export权限，则可以导出
notify_interviewer.allowed_permissions = ("notify",)

class CandidateAdmin(admin.ModelAdmin):
    # 执行动作
    actions = (export_model_as_csv, notify_interviewer)

    exclude = ('creator', 'created_date', 'modified_date')

    # 当前用户是否有导出权限
    def has_export_permission(self, request):
        opts = self.opts
        return request.user.has_perm(f'{opts.app_label}.export')

    def has_notify_permission(self, request):
        opts = self.opts
        return request.user.has_perm(f"{opts.app_label}.notify")

    # 设置只读的字段
    # readonly_fields = ("first_interviewer_user", "second_interviewer_user")
    def get_group_names(self, user):
        group_names = []
        for g in user.groups.all():
            group_names.append(g.name)
        return group_names
    # 设置 一面面试官，二面面试官为只读属性
    def get_readonly_fields(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if "interviewer" in group_names:
            logger.info(f"interviewer is in user's group for {request.user.username}")
            return ("first_interviewer_user", "second_interviewer_user")
        return ()

    # 可以直接在列表页修改一面面试官，二面面试官
    default_list_editable = ("first_interviewer_user", "second_interviewer_user")
    def get_list_editable(self, request):
        group_names = self.get_group_names(request.user)

        if request.user.is_superuser or "hr" in group_names:
            return self.default_list_editable
        return ()
    # django 没有实现get_list_editable，需要覆盖父类
    def get_changelist_instance(self, request):
        self.list_editable = self.get_list_editable(request)
        return super().get_changelist_instance(request)

    # 列表页默认会对用这个方法。对于非管理员，非HR，获取自己是一面面试官或者二面面试官的候选人集合:s
    def get_queryset(self, request):  # show data only owned by the user
        qs = super(CandidateAdmin, self).get_queryset(request)

        group_names = self.get_group_names(request.user)
        if request.user.is_superuser or 'hr' in group_names:
            return qs
        return Candidate.objects.filter(
            Q(first_interviewer_user=request.user) | Q(second_interviewer_user=request.user))

    # 在列表页展示哪些字段、
    list_display = (
        'username', 'city', 'bachelor_school', "get_resume", 'first_score', 'first_result', 'first_interviewer_user', 'second_score',
        'second_result', 'second_interviewer_user', 'hr_score', 'hr_result', 'hr_interviewer_user',)

    # 除了直接使用真实的字段外，还可以用函数
    def get_resume(self, obj):
        if not obj.phone:
            return ""
        resumes = Resume.objects.filter(phone=obj.phone)
        if resumes and len(resumes) > 0:
            return mark_safe(u"<a href='/resume/%s' target='_blank'>%s</a>" % (resumes[0].id, "查看简历"))
        return ""

    # 查询字段
    search_fields = ('username', "phone", "bachelor_school")

    # 筛选条件
    list_filter = ('hr_result', 'second_result', 'first_result')

    # 默认显示排序
    ordering = ('hr_result', 'second_result','first_result')

    # fieldsets 分组页面信息展示, （根据权限控制页面展示字段）一面面试官仅填写一面反馈， 二面面试官可以填写二面反馈
    def get_fieldsets(self, request, obj=None):
        group_names = self.get_group_names(request.user)

        if "interviewer" in group_names and obj.first_interviewer_user == request.user:
            return default_fieldsets_first
        if "interviewer" in group_names and obj.second_interviewer_user == request.user:
            return default_fieldsets_second
        return default_fieldsets


admin.site.register(Candidate, CandidateAdmin)
