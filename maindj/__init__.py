# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from django.core.serializers import register_serializer

register_serializer('json-no-uescape', 'serializers.json_no_uescape')