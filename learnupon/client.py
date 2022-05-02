from .rest_client import LearnUponRestAPI


class LearnUpon(LearnUponRestAPI):
    def __init__(self, *args, **kwargs):
        super(LearnUpon, self).__init__(*args, **kwargs)

    def get_users(self, *args, **kwargs):
        """
        Gets all users from LearnUpon
        :return: List of Users :rtype list
        """
        users = self.request("get", "users", *args, **kwargs)
        return users

    def get_user_by_username(self, username=None, *args, **kwargs):
        """
        Search for user via email OR username
        :param username: Username of user :type str
        :return: Single User Dictionary :rtype dict
        """
        url = "users/search"
        if username:
            url = url + "?username=" + username
        else:
            raise ValueError("Must provide value for username")
        return self.request("get", url, *args, **kwargs)

    def get_user_by_email(self, email=None, *args, **kwargs):
        """
        Search for user via email
        :param email: Email address of user :type str
        :return: Single User Dictionary :rtype dict
        """
        url = "users/search"
        if email:
            url = url + "?email=" + email
        else:
            raise ValueError("Must provide value for email")
        return self.request("get", url, *args, **kwargs)

    def get_user(self, user_id, *args, **kwargs):
        """
        Gets a user by user id
        :param user_id: The id of the user :type str
        :return: A dictionary of user attributes :rtype dict
        """
        url = "users/{}".format(user_id)
        return self.request("get", url, *args, **kwargs)

    def create_user(self, user, *args, **kwargs):
        data = {"User": user}
        return self.request("post", "users", json=data, *args, **kwargs)

    def delete_user(self, user_id, *args, **kwargs):
        """
        Deletes a user by user_id
        :param user_id: The user id of the user to be deleted
        :return: True if deleted successfully :rtype boolean
        """
        self.request("delete", "users/{}".format(user_id), *args, **kwargs)
        return True

    def create_course(self, course, *args, **kwargs):
        data = {"Course": course}
        return self.request("post", "courses", json=data, *args, **kwargs)

    def publish_course(self, course_id, *args, **kwargs):
        data = {"course_id": course_id}
        return self.request("post", "courses/publish", json=data, *args, **kwargs)

    def clone_course(
        self, portal_id, source_course_id, publish_after_clone=True, *args, **kwargs
    ):
        data = {
            "clone_to_portal_id": "{}".format(portal_id),
            "course_id": "{}".format(source_course_id),
            "publish_after_clone": publish_after_clone,
        }
        return self.request("post", "courses/clone", json=data, *args, **kwargs)

    def add_modules(self, course_id, module_id, *args, **kwargs):
        data = {
            "course_id": "{}".format(course_id),
            "module_id": "{}".format(module_id),
        }
        return self.request("post", "courses/add_modules", json=data, *args, **kwargs)

    def get_modules_by_course(self, course_id, *args, **kwargs):
        return self.request(
            "get", "modules?course_id={}".format(course_id), *args, **kwargs
        )

    def get_courses(self, *args, **kwargs):
        """
        Gets all courses in the portal.
        :param name: (Optional) The name of the course you are looking for
        :param course_id: (Optional) The course id of the course you are looking for
        :return: A list of courses with attributes :rtype list
        """
        return self.request("get", "courses", *args, **kwargs)

    def get_course(self, course_id, *args, **kwargs):
        """
        Gets all courses in the portal.
        :param name: (Optional) The name of the course you are looking for
        :param course_id: (Optional) The course id of the course you are looking for
        :return: A list of courses with attributes :rtype list
        """
        return self.request(
            "get", "courses?course_id={}".format(course_id), *args, **kwargs
        )

    def create_enrollment(
        self,
        email=None,
        course_id=None,
        username=None,
        course_name=None,
        re_enroll_if_completed=False,
        *args,
        **kwargs
    ):
        data = {"Enrollment": {"re_enroll_if_completed": re_enroll_if_completed}}
        if email:
            data["Enrollment"]["email"] = email
        if course_id:
            data["Enrollment"]["course_id"] = course_id
        if username:
            data["Enrollment"]["username"] = username
        if course_name:
            data["Enrollment"]["course_name"] = course_name
        return self.request("post", "enrollments", json=data, *args, **kwargs)

    def get_enrollment(
        self, enrollment_id=None, email=None, course_id=None, *args, **kwargs
    ):
        params = []
        if enrollment_id:
            return self.request("get", "enrollments/{}".format(enrollment_id))
        if email:
            params.append("email={}".format(email))
        if course_id:
            params.append("course_id={}".format(course_id))
        if len(params) > 0:
            url = "enrollments/search?" + "&".join(params)
            return self.request("get", url, *args, **kwargs)
        raise ValueError(
            "Must specify at least one argument: enrollment_id, email, course_id"
        )

    def create_markcomplete(
        self,
        enrollment_id=None,
        date_completed=None,
        status=None,
        percentage=None,
        *args,
        **kwargs
    ):
        data = {
            "Markcomplete": {
                "enrollment_id": enrollment_id,
                "status": status,
                "notes": "Imported from Archer Academy 1.0",
            }
        }
        if percentage:
            data["Markcomplete"]["percentage"] = str(percentage)
        if date_completed:
            data["Markcomplete"]["date_completed"] = date_completed
        return self.request("post", "markcompletes", json=data, *args, **kwargs)

    # Items past this point still need to be tested...

    def get_groups(self, title=None, *args, **kwargs):
        """
        Gets the groups from LearnUpon
        :param title: (Optional) The name of the group you are looking for
        :return: A list of groups :rtype list
        """
        params = None
        if title:
            params = {"title": title}
        return self.request("get", "groups", params=params, *args, **kwargs)

    def create_group(self, name, description=None, *args, **kwargs):
        """
        Create a new group in Learnupon
        :param name: The Name of your new group
        :param description: (Optional) The description of your group
        :return: A dictionary of the new group attributes :rtype dict
        """
        data = {"Group": {"title": name, "description": description}}
        return self.request("post", "groups", json=data, *args, **kwargs)

    def add_user_to_group(self, group_id, user_id, *args, **kwargs):
        data = {"GroupMembership": {"group_id": group_id, "user_id": user_id}}
        return self.request("post", "group_memberships", json=data, *args, **kwargs)

    def create_group_invite(
        self,
        group_id,
        email_addresses,
        group_membership_type="Learner",
        *args,
        **kwargs
    ):
        membership_type_convert = {
            "learner": 1,
            "admin": 2,
            "instructor": 3,
            "manager": 4,
        }
        group_membership_type_id = membership_type_convert[
            group_membership_type.lower()
        ]
        email_addresses = (
            email_addresses
            if isinstance(email_addresses, str)
            else ",".join(email_addresses)
        )
        data = {
            "GroupInvite": {
                "email_addresses": email_addresses,
                "group_id": group_id,
                "group_membership_type_id": group_membership_type_id,
            }
        }
        return self.request("post", "group_invites", json=data, *args, **kwargs)
