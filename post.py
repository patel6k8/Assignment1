from datetime import datetime
from user import User

class Post:
    total_posts = 0  

    def __init__(self, author, content, tags=None):
        if not self.is_valid_content(content):
            raise ValueError("Invalid post content.")
        
        self._author = author
        self._content = content
        self._created_on = datetime.now()
        self._tags = set() if tags is None else set(tags)
        self._liked_by = []
        self._comments = []
        
        Post.total_posts += 1

    @staticmethod
    def is_valid_content(content):
        return 3 <= len(content) <= 2200

    @staticmethod
    def is_valid_tag(tag):
        return len(tag) <= 30 and tag.isalnum()

    @property
    def content(self):
        return self._content

    @property
    def created_on(self):
        return self._created_on

    @property
    def tags(self):
        return self._tags

    @property
    def liked_by(self):
        return self._liked_by

    def add_tag(self, tag):
        if self.is_valid_tag(tag):
            self._tags.add(tag)
        else:
            raise ValueError("Invalid tag.")

    def remove_tag(self, tag):
        self._tags.discard(tag)

    @classmethod
    def get_post_count(cls):
        return cls.total_posts
