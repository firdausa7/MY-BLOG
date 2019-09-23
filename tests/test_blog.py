import unittest
from app.models import User, Blog, Comment
from app import db

class BlogModelTest(unittest.TestCase):

    def setUp(self):
        self.user_firdausa = User(username = "firdausa", password = "frida123", email="frida@yahoo.com")
        self.new_blog = Blog(title="code", body = "coding rocks", user_id =self.user_firdausa.id )

    def tearDown(self):
        Blog.query.delete()
        User.query.delete()



    def test_instance(self):
        self.assertTrue(isinstance(self.new_blog, Blog))

    def test_check_instance_variables(self):
        self.assertEquals(self.new_blog.title, 'code')
        self.assertEquals(self.new_blog.body,"coding rocks")
        self.assertEquals(self.new_blog.user_id, self.user_firdausa.id)

    def test_save_blog(self):
        self.new_blog.save_blog()
        self.assertTrue(len(Blog.query.all())>0)

    def test_get_blogs(self):

        self.new_blog.save_blog()
        blogs = Blog.get_blogs()
        self.assertTrue(len(blogs)==1)

