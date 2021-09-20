from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

def check_user_exist(user , new_phone):
    exists_user = User.objects.filter(phone=new_phone).first()
    if exists_user and exists_user.phone != user.phone:
        raise ValidationError([
            ValidationError('کاربری با این موبایل قبلا ثبت شده است!', code='duplicate'),
        ])