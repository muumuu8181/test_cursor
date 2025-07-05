import tweepy
import logging
from PIL import Image
import os
from config import Config

class TwitterClient:
    def __init__(self):
        self.config = Config()
        self.api = None
        self.client = None
        self.setup_api()
    
    def setup_api(self):
        """Initialize Twitter API client"""
        try:
            # API v1.1 for media upload
            auth = tweepy.OAuthHandler(
                self.config.TWITTER_API_KEY,
                self.config.TWITTER_API_SECRET
            )
            auth.set_access_token(
                self.config.TWITTER_ACCESS_TOKEN,
                self.config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.api = tweepy.API(auth)
            
            # API v2 for posting
            self.client = tweepy.Client(
                consumer_key=self.config.TWITTER_API_KEY,
                consumer_secret=self.config.TWITTER_API_SECRET,
                access_token=self.config.TWITTER_ACCESS_TOKEN,
                access_token_secret=self.config.TWITTER_ACCESS_TOKEN_SECRET
            )
            
            logging.info("Twitter API initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize Twitter API: {e}")
            raise
    
    def validate_image(self, image_path):
        """Validate image file and size"""
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        # Check file size
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > self.config.MAX_IMAGE_SIZE_MB:
            raise ValueError(f"Image too large: {file_size_mb:.2f}MB (max: {self.config.MAX_IMAGE_SIZE_MB}MB)")
        
        # Check if it's a valid image
        try:
            with Image.open(image_path) as img:
                img.verify()
        except Exception as e:
            raise ValueError(f"Invalid image file: {e}")
    
    def post_with_image(self, message, image_path):
        """Post a tweet with an image"""
        try:
            # Validate image
            self.validate_image(image_path)
            
            # Upload image using API v1.1
            media = self.api.media_upload(image_path)
            
            # Post tweet with image using API v2
            response = self.client.create_tweet(
                text=message,
                media_ids=[media.media_id]
            )
            
            logging.info(f"Posted tweet successfully: {response.data['id']}")
            return response.data['id']
            
        except Exception as e:
            logging.error(f"Failed to post tweet: {e}")
            raise
    
    def test_connection(self):
        """Test Twitter API connection"""
        try:
            user = self.client.get_me()
            logging.info(f"Connected as: @{user.data.username}")
            return True
        except Exception as e:
            logging.error(f"Connection test failed: {e}")
            return False