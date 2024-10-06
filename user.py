from datetime import datetime

class User:
    total_users = 0

    def __init__(self, username, email, bio=""):
        if not self.is_valid_username(username):
            raise ValueError("Invalid username.")
        self._username = username
        self._email = email
        self._bio = bio
        self._joined_on = datetime.now()
        self._posts = []
        self._liked_posts = []
        self._comments = []
        self._liked_comments = []
        self.following = []
        self.followers = []
        
        User.total_users += 1

    @staticmethod
    def is_valid_username(username):
        return len(username) >= 3 and username.isalnum()

    @property
    def username(self):
        return self._username

    @property
    def email(self):
        return self._email

    @property
    def bio(self):
        return self._bio

    @property
    def joined_on(self):
        return self._joined_on

    def update_bio(self, new_bio):
        self._bio = new_bio

    @classmethod
    def get_user_count(cls):
        return cls.total_users
