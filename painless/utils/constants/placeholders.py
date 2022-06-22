from django.utils.translation import ugettext_lazy as _
from painless.utils.constants.interfaces import IMessage

class Placeholder(IMessage):
    """Class based Messaging system for handling all response messages in views"""
    _required_expression = ' را وارد کنید'
    _common_expression = ' را به صورت اختیاری وارد کنید'

    ######################
    ###     COMMON     ###
    ######################
    EMPTY = ''

    ######################
    ###      User      ###
    ######################
    FIRST_NAME = _('نام')
    LAST_NAME = _('نام خانوادگی')
    NATIONAL_CODE = _('کد ملی')
    COMPANY_NAME = _('نام شرکت')
    PHONE_NUMBER = _('شماره تماس')
    TEL = _('تلفن ثابت')
    STATE = _('استان')
    CITY = _('شهر')
    REGION = _('محله')
    POSTAL_CODE = _('کد پستی')
    POSTAL_ADDRESS = _('آدرس پستی')
    DESCRIPTION = _('توضیحات')
    ADDRESS_NAME = _('نام آدرس')

    def get_content(self, attr, type):
        content = getattr(self, attr)
        if type == 'required':
            content += self._required_expression
        elif type == 'optional':
            content += self._common_expression
        elif type == 'empty':
            content = self.EMPTY

        return content