from django.utils.translation import ugettext_lazy as _
from painless.utils.constants.interfaces import IMessage

class MessageSuccess(IMessage):
    """Class based Messaging system for handling all response messages in views"""
    _common_expression = _(' با موفقیت {} شد. ')

    ADDRESS = _('آدرس')
    COMMENT = _('نظر')
    NOTIF = _('اعلان')
    FAVORITE = _('علاقه مندی')

    SUBMIT_ACTION = _('ثبت')
    EDIT_ACTION = _('ویرایش')
    DELETE_ACTION = _('حذف')

    def get_content(self, attr, action):
        expression = self._common_expression.format(getattr(self, action))
        return getattr(self, attr) + expression 

