import requests
from urllib.parse import urljoin

membership_type_convert = {
            'learner': 1,
            'admin': 2,
            'instructor': 3,
            'manager': 4
        }


class LearnUpon(object):

    def __init__(self, portal_url=None, username=None, password=None, verify=True):
        for input in [portal_url, username, password]:
            if not input:
                raise Exception("Missing required input {}".format(input))

        self.session = requests.session()
        self.session.auth = (username, password)
        self.session.verify = verify
        self.base_url = urljoin(portal_url, 'api/v1/')
        if not self.base_url.endswith('/'):
            self.base_url += '/'

        self.test_auth()

    def request(self, method, endpoint, **kwargs):
        endpoint = endpoint.lstrip("/")
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method=method, url=url, **kwargs)
        response.raise_for_status()
        return response.json()

    def test_auth(self):
        portals = self.request('get', 'portals')
        if not portals['portals']:
            raise Exception("This account does not have access to any portals!!")

    def get_users(self):
        """
        Gets all users from LearnUpon
        :return: List of Users :rtype list
        """
        users = self.request('get', 'users')
        return users

    def search_for_user(self, email=None, username=None):
        """
        Search for user via email OR username
        :param email: Email address of user :type str
        :param username: Username of user :type str
        :return: Single User Dictionary :rtype dict
        """
        params = None
        if email:
            params = {'email': email}
        if username:
            params = {'username': username}
        if not params:
            raise ValueError("One of email or username must be provided")
        user_search = self.request('get', 'users/search', params=params)
        return user_search['user'][0]

    def get_user(self, user_id):
        """
        Gets a user by user id
        :param user_id: The id of the user :type str
        :return: A dictionary of user attributes :rtype dict
        """
        user = self.request('get', 'users/{}'.format(user_id))
        return user['user'][0]

    def create_user(self, email, password, username=None, last_name=None, first_name=None):
        for input in [email, password]:
            if not input:
                raise ValueError("Missing required input {}".format(input))

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        data = {
            "User": {
                "last_name": last_name,
                "first_name": first_name,
                "email": email,
                "username": username,
                "password": password
            }
        }

        new_user = self.request('post', 'users', json=data)
        return new_user

    # TODO continue testing update user functionality
    # def update_user(self, user_data):
    #     """
    #     Updates an existing user in LearnUpon
    #     :param user_data: A dictionary of user attributes :type dict
    #     :return: A dictionary of the updated users attributes :rtype dict
    #     """
    #     data = {"User": {}}
    #     for key in user_data:
    #         if user_data[key]:
    #             data['User'][key] = user_data[key]
    #     updated_user = self.request('put', 'users/{}'.format(user_data['id']), json=data)
    #     return updated_user

    def delete_user(self, user_id):
        """
        Deletes a user by user_id
        :param user_id: The user id of the user to be deleted
        :return: True if deleted successfully :rtype boolean
        """
        self.request('delete', 'users/{}'.format(user_id))
        return True


    def invite_user(self, email_address):
        data = {
            'Invite': {
                'email': email_address
            }
        }

        user_invite = self.request('post', 'portal_invite', json=data)
        return user_invite

    def get_courses(self, name=None, course_id=None):
        """
        Gets all courses in the portal.
        :param name: (Optional) The name of the course you are looking for
        :param course_id: (Optional) The course id of the course you are looking for
        :return: A list of courses with attributes :rtype list
        """
        params = None
        if name:
            params = {'name': name}
        elif course_id:
            params = {'course_id': course_id}
        courses = self.request('get', 'courses', params=params)
        return courses['courses']

    def get_groups(self, title=None):
        """
        Gets the groups from LearnUpon
        :param title: (Optional) The name of the group you are looking for
        :return: A list of groups :rtype list
        """
        params = None
        if title:
            params = {'title': title}
        groups = self.request('get', 'groups', params=params)
        return groups['groups']

    def create_group(self, name, description=None):
        """
        Create a new group in Learnupon
        :param name: The Name of your new group
        :param description: (Optional) The description of your group
        :return: A dictionary of the new group attributes :rtype dict
        """
        data = {
            'Group': {
                'title': name,
                'description': description
            }
        }

        new_group = self.request('post', 'groups', json=data)
        return new_group



    def add_user_to_group(self, group_id, user_id):
        data = {
            'GroupMembership': {
                'group_id': group_id,
                'user_id': user_id
            }
        }

        add_user = self.request('post', 'group_memberships', json=data)
        return add_user

    def create_group_invite(self, group_id, email_addresses, group_membership_type='Learner'):

        group_membership_type_id = membership_type_convert[group_membership_type.lower()]

        email_addresses = email_addresses if isinstance(email_addresses, str) else ",".join(email_addresses)

        data = {
            'GroupInvite': {
                'email_addresses': email_addresses,
                'group_id': group_id,
                'group_membership_type_id': group_membership_type_id
            }
        }

        group_invite = self.request('post', 'group_invites', json=data)
        return group_invite
