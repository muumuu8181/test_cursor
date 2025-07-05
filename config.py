import os
from decouple import config

class Config:
    # Twitter API credentials
    TWITTER_API_KEY = config('TWITTER_API_KEY', default='')
    TWITTER_API_SECRET = config('TWITTER_API_SECRET', default='')
    TWITTER_ACCESS_TOKEN = config('TWITTER_ACCESS_TOKEN', default='')
    TWITTER_ACCESS_TOKEN_SECRET = config('TWITTER_ACCESS_TOKEN_SECRET', default='')
    
    # Posting settings
    POSTS_FOLDER = config('POSTS_FOLDER', default='posts')
    DEFAULT_TIMEZONE = config('DEFAULT_TIMEZONE', default='Asia/Tokyo')
    
    # Schedule settings
    CHECK_INTERVAL_MINUTES = config('CHECK_INTERVAL_MINUTES', default=5, cast=int)
    MAX_IMAGE_SIZE_MB = config('MAX_IMAGE_SIZE_MB', default=5, cast=int)
    
    # Log settings
    LOG_LEVEL = config('LOG_LEVEL', default='INFO')
    LOG_FILE = config('LOG_FILE', default='posting.log')