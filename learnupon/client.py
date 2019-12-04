import requests
from urllib.parse import urljoin


class LearnUpon(object):

    def __init__(self, portal_url=None, username=None, password=None, verify=False):
        for input in [portal_url, username, password]:
            if not input:
                raise Exception("Missing one of 'portal_url, username, password'")

        self.session = requests.session()
        self.session.auth = (username, password)
        self.session.verify = verify
        self.base_url = urljoin(portal_url, 'api/v1/')
        if not self.base_url.endswith('/'):
            self.base_url += '/'

        self.test_auth()

    def request(self, method, endpoint, **kwargs):
        url = urljoin(self.base_url, endpoint)
        response = self.session.request(method=method, url=url, **kwargs)
        response.raise_for_status()
        return response.json()

    def test_auth(self):
        portals = self.request('get', 'portals')
        if not portals['portals']:
            raise Exception("This account does not have access to any portals!!")

    def invite_user(self, email_address):
        data = {
            'Invite': {
                'email': email_address
            }
        }

        user_invite = self.request('post', 'portal_invite', json=data)
        return user_invite

    def create_group(self, name):
        data = {
            'Group': {
                'Title': name
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
        membership_type_convert = {
            'learner': 1,
            'admin': 2,
            'instructor': 3,
            'manager': 4
        }
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
