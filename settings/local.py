from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

## 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "w$46bks+b3-7f(13#i%v@jwejrnxc$^^#@#@^t@fofizy1^mo9r8(-939243423300"
#
# ## 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
# ## 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
# LDAP_AUTH_URL = "ldap://xxxxx:389"
# LDAP_AUTH_CONNECTION_USERNAME = "admin"
# LDAP_AUTH_CONNECTION_PASSWORD = "your_admin_credentials"
#
# INSTALLED_APPS += (
#     # other apps for production site
# )
#
#
# ## 钉钉群的 WEB_HOOK， 用于发送钉钉消息
# DINGTALK_WEB_HOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"


import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
sentry_sdk.init(
    dsn="http://074c45c6afa5c525062d59c18665ee58@127.0.0.1:9000/2",
    integrations=[DjangoIntegration()],
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    traces_sample_rate=1.0,
    send_default_pii=True,
)

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}