from django.urls import include, re_path, path
from jobs import views

urlpatterns = [
    # 职位列表
    re_path(r"^joblist/", views.joblist, name="joblist"),
    re_path(r"^job/(?P<job_id>\d+)/$", views.detail, name="detail"),  # ?P 声明一个命名组
    re_path(r"^$", views.joblist, name="home"),  # ^字符开始 $字符结束 匹配一个空字符串
    # 提交简历
    path('resume/add/', views.ResumeCreateView.as_view(), name='resume-add'),
    # 简历详情页
    path('resume/<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
]