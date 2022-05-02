import uuid


class User(dict):
    def __init__(
        self,
        email=None,
        first_name=None,
        last_name=None,
        enabled=None,
        user_type=None,
        language=None,
        password=None,
        *args,
        **kwargs
    ):
        self["email"] = email if email else None
        self["first_name"] = first_name if first_name else None
        self["last_name"] = last_name if last_name else None
        self["language"] = language if language else "en"
        self["enabled"] = enabled if enabled else True
        self["user_type"] = user_type if user_type else "learner"
        self["change_password_on_first_login"] = False
        self["password"] = password if password else str(uuid.uuid4())
        if len(list(kwargs)) > 0:
            for k, v in list(kwargs):
                self[k] = v
        # self["CustomData"] = {}
        # self["account_expires"] = ""
        # self["membership_type"] = ""
        # self["sf_user_id"] = None
        # self["sf_contact_id"] = None
        # self["is_salesforce_contact"] = 0
        # self["customDataFieldValues"] = []
        # self["locale"] = ""
        # self["enabled"] = True
        # self["user_type"] = ""
        # self["can_enroll"] = True
        # self["can_delete_users"] = False
        # self["can_unenroll_users"] = False
        # self["can_move_groups"] = False
        # self["can_mark_complete"] = False
        # self["tutor_can_edit_their_courses"] = True
        # self["tutor_can_create_courses"] = False
