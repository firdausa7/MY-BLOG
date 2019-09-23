import unittest
from app.models import Comment, User, Blog
from app import db

class TestCommentModel(unittest.TestCase):

    def setUp(self):
        self.user_firdausa = User(username = "firdausa", password = "frida123", email="frida@yahoo.com")
        self.new_blog = Blog(title="code", body = "coding rocks", user_id =self.user_firdausa.id )
        self.new_comment=Comment(feedback="nice", user_id=self.user_firdausa.id,blog_id=self.new_blog.id)

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()
        Comment.query.delete()

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comment))

    def test_check_instance_variables(self):

        self.assertEquals(self.new_comment.feedback, 'nice')
        self.assertEquals(self.new_comment.user_id,self.user_firdausa.id)
        self.assertEquals(self.new_comment.blog_id, self.new_blog.id)

    def test_save_blog(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_blogs(self):

        self.new_comment.save_comment()
        comments = Comment.get_comments()
        self.assertTrue(len(comments)==1)