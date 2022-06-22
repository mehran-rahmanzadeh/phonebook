from django.utils.translation import ugettext_lazy as _
from painless.utils.constants.interfaces import IMessage

class Label(IMessage):
    """Class based Messaging system for handling all response messages in views"""

    ######################
    ###      User      ###
    ######################
    FIRST_NAME = _('نام')
    LAST_NAME = _('نام خانوادگی')
    PHONE_NUMBER = _('شماره تلفن همراه')
    EMAIL = _('ایمیل')
    TEL = _('تلفن ثابت')
    IS_SELF_RECEIVER = _('من خودم گیرنده هستم')
    
    ######################
    ###     Profile    ###
    ######################
    NATIONAL_CODE = _('کد ملی')
    BIRTH_DATE = _('تاریخ تولد')
    GENDER = _('جنسیت')
    JOB = _('شغل')
    
    ######################
    ###     STEPS      ###
    ######################
    INITIAL = _('اولیه')
    PENDING = _('در انتظار پرداخت')
    INPROGRESS = _('در حال پردازش')
    SHIPPED = _('در حال ارسال')
    DELIVERED = _('تحویل داده شده')
    CANCELED = _('لغو شده')
    
    ######################
    ###    ADDRESS     ###
    ######################
    ADDRESS_NAME = _('نام آدرس')
    STATE = _('استان')
    CITY = _('شهر')
    REGION = _('محله')
    POSTAL_CODE = _('کد پستی')
    POSTAL_ADDRESS = _('آدرس پستی')
    DESCRIPTION = _('توضیحات')
    
    ######################
    ###    COMPANY     ###
    ######################
    COMPANY_NAME = _('نام شرکت')


    def get_content(self, attr):
        return getattr(self, attr)

