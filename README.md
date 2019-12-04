# Swimlane Learnupon

## Description
A python package for interacting with the LearnUpon LMS.

## Installation
```
pip install learnupon
```

## Usage
```
from learnupon import LearnUpon

learnupon = LearnUpon(portal_url="https://myportal.learnupon.com", 
                      username="abc123", password="def456")
                      
new_user = learnupon.invite_user(email_address="new_user@mycompany.com")
```