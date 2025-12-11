from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .models import Skill, Post, Profile
import uuid


class SkillModelTest(TestCase):
    """Tests for the Skill model"""
    
    def setUp(self):
        """Create test data that runs before each test method"""
        self.skill = Skill.objects.create(name="Python")
    
    def test_skill_creation(self):
        """Test that a skill can be created successfully"""
        self.assertEqual(self.skill.name, "Python")
        self.assertIsInstance(self.skill, Skill)
    
    def test_skill_str_method(self):
        """Test the string representation of a skill"""
        self.assertEqual(str(self.skill), "Python")
    
    def test_skill_name_max_length(self):
        """Test that skill name respects max_length constraint"""
        max_length = self.skill._meta.get_field('name').max_length
        self.assertEqual(max_length, 150)
    
    def test_skill_name_unique(self):
        """Test that duplicate skill names are not allowed"""
        with self.assertRaises(IntegrityError):
            Skill.objects.create(name="Python")
    
    def test_skill_name_required(self):
        """Test that skill name is required"""
        skill = Skill(name="")
        with self.assertRaises(ValidationError):
            skill.full_clean()


class PostModelTest(TestCase):
    """Tests for the Post model"""
    
    def setUp(self):
        """Create test user and post"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            user=self.user,
            body='This is a test post body'
        )
    
    def test_post_creation(self):
        """Test that a post can be created successfully"""
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.user, self.user)
        self.assertEqual(self.post.body, 'This is a test post body')
    
    def test_post_user_relationship(self):
        """Test the ForeignKey relationship with User"""
        self.assertEqual(self.post.user.username, 'testuser')
        self.assertIn(self.post, self.user.user_posts.all())
    
    def test_post_created_at_auto_add(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.post.created_at)
    
    def test_post_body_can_be_blank(self):
        """Test that post body can be empty"""
        post = Post.objects.create(
            title='No Body Post',
            user=self.user,
            body=''
        )
        self.assertEqual(post.body, '')
    
    def test_post_cascade_delete(self):
        """Test that posts are deleted when user is deleted"""
        post_id = self.post.id
        self.user.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())
    
    def test_post_title_max_length(self):
        """Test title max length constraint"""
        max_length = self.post._meta.get_field('title').max_length
        self.assertEqual(max_length, 150)


class ProfileModelTest(TestCase):
    """Tests for the Profile model"""
    
    def setUp(self):
        """Create test users, skills, and profile"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        self.skill1 = Skill.objects.create(name="Python")
        self.skill2 = Skill.objects.create(name="Django")
        
        self.profile = Profile.objects.create(
            user=self.user,
            bio='Test bio',
            urls='https://example.com',
            reputation_score=100
        )
        self.other_profile = Profile.objects.create(
            user=self.other_user,
            urls='https://other.com'
        )
    
    def test_profile_creation(self):
        """Test that a profile can be created successfully"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.reputation_score, 100)
    
    def test_profile_str_method(self):
        """Test the string representation of a profile"""
        self.assertEqual(str(self.profile), 'testuser')
    
    def test_profile_uuid_primary_key(self):
        """Test that profile uses UUID as primary key"""
        self.assertIsInstance(self.profile.id, uuid.UUID)
    
    def test_profile_uuid_uniqueness(self):
        """Test that each profile has a unique UUID"""
        self.assertNotEqual(self.profile.id, self.other_profile.id)
    
    def test_profile_default_values(self):
        """Test default values for profile fields"""
        new_user = User.objects.create_user(username='newuser', password='pass')
        new_profile = Profile.objects.create(user=new_user, urls='https://test.com')
        
        self.assertTrue(new_profile.is_active)
        self.assertEqual(new_profile.reputation_score, 0)
        self.assertEqual(new_profile.bio, '')
    
    def test_profile_one_to_one_relationship(self):
        """Test OneToOneField relationship with User"""
        self.assertEqual(self.user.user_profile, self.profile)
    
    def test_profile_cascade_delete(self):
        """Test that profile is deleted when user is deleted"""
        profile_id = self.profile.id
        self.user.delete()
        self.assertFalse(Profile.objects.filter(id=profile_id).exists())
    
    def test_profile_skills_many_to_many(self):
        """Test ManyToMany relationship with Skills"""
        self.profile.skills.add(self.skill1, self.skill2)
        
        self.assertEqual(self.profile.skills.count(), 2)
        self.assertIn(self.skill1, self.profile.skills.all())
        self.assertIn(self.skill2, self.profile.skills.all())
    
    def test_profile_following_relationship(self):
        """Test self-referential ManyToMany following relationship"""
        self.profile.following.add(self.other_profile)
        
        # Test following relationship
        self.assertEqual(self.profile.following.count(), 1)
        self.assertIn(self.other_profile, self.profile.following.all())
        
        # Test symmetrical=False (followers relationship)
        self.assertEqual(self.other_profile.following.count(), 0)
        self.assertIn(self.profile, self.other_profile.following_profile.all())
    
    def test_profile_bio_max_length(self):
        """Test bio max length constraint"""
        max_length = self.profile._meta.get_field('bio').max_length
        self.assertEqual(max_length, 500)
    
    def test_profile_urls_max_length(self):
        """Test URLs max length constraint"""
        max_length = self.profile._meta.get_field('urls').max_length
        self.assertEqual(max_length, 300)
    
    def test_profile_avatar_blank_null(self):
        """Test that avatar can be blank and null"""
        self.assertIsNone(self.profile.avatar.name)
    
    def test_profile_timestamps(self):
        """Test created_at and updated_at timestamps"""
        self.assertIsNotNone(self.profile.created_at)
        self.assertIsNotNone(self.profile.updated_at)
        self.assertIsNotNone(self.profile.last_activity)
    
    def test_profile_updated_at_changes(self):
        """Test that updated_at changes when profile is saved"""
        original_updated_at = self.profile.updated_at
        
        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)
        
        self.profile.bio = 'Updated bio'
        self.profile.save()
        
        self.assertNotEqual(self.profile.updated_at, original_updated_at)
    
    def test_profile_custom_permission(self):
        """Test that custom permission exists"""
        permissions = [p.codename for p in self.profile._meta.permissions]
        self.assertIn('can_verify_profile', permissions)
    
    def test_profile_reputation_score_positive(self):
        """Test that reputation_score is a PositiveIntegerField"""
        field = self.profile._meta.get_field('reputation_score')
        self.assertEqual(field.__class__.__name__, 'PositiveIntegerField')
    
    def test_multiple_followers(self):
        """Test profile with multiple followers"""
        user3 = User.objects.create_user(username='user3', password='pass')
        profile3 = Profile.objects.create(user=user3, urls='https://user3.com')
        
        # Both profiles follow other_profile
        self.profile.following.add(self.other_profile)
        profile3.following.add(self.other_profile)
        
        self.assertEqual(self.other_profile.following_profile.count(), 2)
        self.assertIn(self.profile, self.other_profile.following_profile.all())
        self.assertIn(profile3, self.other_profile.following_profile.all())