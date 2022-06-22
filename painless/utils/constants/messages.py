from django.utils.translation import ugettext_lazy as _

################
##### auth #####
################
PASSWORD_UPDATE_SUCCESS = _('Password updated successfully.')
PASSWORD_NOT_VALID = _("Password is not valid.")
PASSWORD_INCORRECT = _("The current password is incorrect")
ACCOUNT_NOT_ACTIVE = _("Dear user, Your account is not active.")
USER_NOT_FOUND = _("User not found.")
USER_EXISTS = _("User Exists.")
LOGIN_SUCCESS = _("You have been logged in successfully.")
LOGIN_FAILURE = _("login failed.")
USERNAME_OR_PASSWORD_INCORRECT = _("Username or password is incorrect.")
TOKEN_VALID = _('Token is valid.')
TOKEN_EXPIRED = _('Token Expired.')
YOU_CAN_NOT_REGISTER = _("You Can't Register!")
REGISTER_SUCCESS = _("User registered successfully.")
REGISTER_FAILURE = _("Registration failed.")
YOU_CAN_NOT_RESET_PASSWORD = _("Your Can't ResetPassword!")
RESET_PASSWORD_SUCCESS = _('Password updated successfully')
RESET_PASSWORD_FAILURE = _("Reset Password Failed.")

#############
### users ###
#############
USER_EMAIL_EXISTS = _('A User with this email already exists.')
ENTER_VALID_EMAIL = _('Enter a valid Email Address')
USER_IVAN_PROFILE_EXISTS = _('A User with this Ivan Profile already exists.')
FIELD_AVATAR_SQUARE = _('field `avatar` must have square dimension.')
IMAGE_NOT_FOUND = _("User image doesn't exist.")
FIELD_TITLE_REQUIRED = _('field `title` is required')
TAG_TITLE_NOT_FOUND = _('Tag with title {} doesn\'t exist.')
FIELD_TITLE_ENABLE_REQUIRED = _('field `title` and `enabled` is required.')
NOTIF_TITLE_NOT_FOUND = _('Notification with title {} does not exist.')
FIELD_NOTIF_REQUIRED = _('field `notifications` is required.')
USER_HAS_MEMBERSHIP = _('User already has a membership plan.')
PLAN_NOT_FOUND = _('Plan Not Found!')
FREE_USER_CAN_NOT_JOIN_BUNDLE = _('Free user cannot join to the bundle.')
USER_HAS_ACTIVE_TRAINING_COURSE = _('The user currently has an active training course.')
USER_PARTICIPATED_IN_TRAINING_COURSE = _('The user has already participated in this training course.')
PARTICIPATION_NOT_FOUND = _('Participation Not Found.')
CANCELLED_SUCCESS = _('Cancelled successfully.')
USER_HAS_NO_BASKET = _('User has no active basket!')
FIELD_SCOPE_REQUIRED = _('Field `scope` is required.')
CHECKOUT_NOT_FOUND = _('Checkout Not Found!')
PRODUCT_NOT_FOUND = _('Product Not Found!')
ADDED_SUCCESS = _('Added successfully')
REMOVED_SUCCESS = _('Removed successfully')