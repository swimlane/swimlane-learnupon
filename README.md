# Swimlane Learnupon

## Description
A python package for interacting with the LearnUpon LMS.

## Installation
```
pip install learnupon
```

## Usage
```python
from learnupon import LearnUpon

learnupon = LearnUpon(portal_url="https://myportal.learnupon.com", 
                      username="abc123", password="def456")
# Get all users
users = learnupon.get_users()
# Get user by email
user = learnupon.search_for_user(email='some.user@company.com')
# Get user by user_id
user_again = learnupon.get_user(user_id=user['id'])
# Create a new user
new_user = learnupon.create_user(email='some.user@company.com',
                                 password="Thisisapassword")
# Invite a new user by email                      
new_user = learnupon.invite_user(email_address="new_user@mycompany.com")
# Get Courses (Optional name filter)
courses = learnupon.get_courses(name='Course Name')
# Get All Groups
groups = learnupon.get_groups(title="Group Name")
# Create Group Invite
group_invites = learnupon.create_group_invite(group_id=groups[0]["id"], 
                                             email_addresses=['user1@company.com', 'user2@company.com'])
```