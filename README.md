# LearnUpon Python SDK

## Description

A python package for interacting with the LearnUpon LMS.

## Installation

```bash
pip install learnupon
```

## Usage

### Environment Variables

```bash
LEARNUPON_ACCESS_KEY_ID='abcdefghijklmnopqrstuvwxyz'
LEARNUPON_SECRET_KEY='abcdefghijklmnopqrstuvwxyz'
LEARNUPON_PORTAL_URL='https://example.learnupon.com'
```

### Initiation

```python
import os
from learnupon import LearnUpon

# With Environment variables
learnupon = LearnUpon()

# Without Environment Variables
learnupon = LearnUpon(
        portal_url='https://example.learnupon.com',
        username='abcdefghijklmnopqrstuvwxyz',
        password='abcdefghijklmnopqrstuvwxyz',
        )

```

### User Retrieval

```python
from learnupon import LearnUpon, User
learnupon = LearnUpon()

# Get all users (paged)
users = learnupon.get_users()

# Get all users (paginate through results)
all_users = users.paginate()

# Get user by email
user = learnupon.get_user_by_email(email='some.user@company.com')

# Get user by user_id
user = learnupon.get_user(user_id=user['id'])

# Get user by username
user = learnupon.get_user_by_username(username='someuser883')

# Build User Model (password auto-generated)
new_user = User(email='some.user@company.com', first_name='some', last_name='user')

# Create a new user
user = learnupon.create_user(new_user)
```

```python
# Get Courses (Optional name filter)
courses = learnupon.get_courses(name='Course Name')
```
