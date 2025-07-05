import os
import re
from datetime import datetime, timedelta
import pytz
import logging
from pathlib import Path
from config import Config

class PostManager:
    def __init__(self):
        self.config = Config()
        self.posts_folder = Path(self.config.POSTS_FOLDER)
        self.timezone = pytz.timezone(self.config.DEFAULT_TIMEZONE)
        self.processed_posts = set()
        self.setup_folders()
    
    def setup_folders(self):
        """Create posts folder if it doesn't exist"""
        self.posts_folder.mkdir(exist_ok=True)
        logging.info(f"Posts folder ready: {self.posts_folder}")
    
    def parse_folder_datetime(self, folder_name):
        """Parse datetime from folder name
        
        Supported formats:
        - YYYY-MM-DD_HH-MM (2024-01-15_14-30)
        - YYYY-MM-DD (2024-01-15) - defaults to 09:00
        - YYYYMMDD_HHMM (20240115_1430)
        - YYYYMMDD (20240115) - defaults to 09:00
        """
        patterns = [
            # YYYY-MM-DD_HH-MM
            (r'^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})$', 
             lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]))),
            
            # YYYY-MM-DD (default to 09:00)
            (r'^(\d{4})-(\d{2})-(\d{2})$', 
             lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), 9, 0)),
            
            # YYYYMMDD_HHMM
            (r'^(\d{4})(\d{2})(\d{2})_(\d{2})(\d{2})$', 
             lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), int(m[4]), int(m[5]))),
            
            # YYYYMMDD (default to 09:00)
            (r'^(\d{4})(\d{2})(\d{2})$', 
             lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), 9, 0)),
        ]
        
        for pattern, parser in patterns:
            match = re.match(pattern, folder_name)
            if match:
                try:
                    dt = parser(match.groups())
                    return self.timezone.localize(dt)
                except ValueError as e:
                    logging.warning(f"Invalid date in folder name {folder_name}: {e}")
                    continue
        
        logging.warning(f"Unable to parse datetime from folder name: {folder_name}")
        return None
    
    def get_pending_posts(self):
        """Get posts that should be posted now"""
        now = datetime.now(self.timezone)
        pending_posts = []
        
        for folder_path in self.posts_folder.iterdir():
            if not folder_path.is_dir():
                continue
                
            folder_name = folder_path.name
            if folder_name in self.processed_posts:
                continue
                
            post_time = self.parse_folder_datetime(folder_name)
            if not post_time:
                continue
                
            # Check if it's time to post (within the check interval)
            time_diff = (now - post_time).total_seconds()
            if 0 <= time_diff <= (self.config.CHECK_INTERVAL_MINUTES * 60):
                post_data = self.load_post_data(folder_path)
                if post_data:
                    pending_posts.append({
                        'folder_name': folder_name,
                        'post_time': post_time,
                        'data': post_data
                    })
        
        return pending_posts
    
    def load_post_data(self, folder_path):
        """Load post data from folder"""
        try:
            # Find message file
            message_file = None
            for ext in ['.txt', '.md']:
                potential_file = folder_path / f"message{ext}"
                if potential_file.exists():
                    message_file = potential_file
                    break
            
            if not message_file:
                logging.warning(f"No message file found in {folder_path}")
                return None
            
            # Read message
            with open(message_file, 'r', encoding='utf-8') as f:
                message = f.read().strip()
            
            # Find image file
            image_file = None
            image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            for file_path in folder_path.iterdir():
                if file_path.suffix.lower() in image_extensions:
                    image_file = file_path
                    break
            
            if not image_file:
                logging.warning(f"No image file found in {folder_path}")
                return None
            
            return {
                'message': message,
                'image_path': str(image_file),
                'folder_path': str(folder_path)
            }
            
        except Exception as e:
            logging.error(f"Error loading post data from {folder_path}: {e}")
            return None
    
    def mark_as_processed(self, folder_name):
        """Mark a post as processed"""
        self.processed_posts.add(folder_name)
        logging.info(f"Marked as processed: {folder_name}")
    
    def get_upcoming_posts(self, days_ahead=7):
        """Get upcoming posts for the next N days"""
        now = datetime.now(self.timezone)
        future_limit = now + timedelta(days=days_ahead)
        upcoming_posts = []
        
        for folder_path in self.posts_folder.iterdir():
            if not folder_path.is_dir():
                continue
                
            folder_name = folder_path.name
            post_time = self.parse_folder_datetime(folder_name)
            
            if post_time and now < post_time <= future_limit:
                post_data = self.load_post_data(folder_path)
                if post_data:
                    upcoming_posts.append({
                        'folder_name': folder_name,
                        'post_time': post_time,
                        'data': post_data
                    })
        
        # Sort by post time
        upcoming_posts.sort(key=lambda x: x['post_time'])
        return upcoming_posts
    
    def create_example_post(self, folder_name):
        """Create an example post structure"""
        folder_path = self.posts_folder / folder_name
        folder_path.mkdir(exist_ok=True)
        
        # Create example message
        message_file = folder_path / "message.txt"
        with open(message_file, 'w', encoding='utf-8') as f:
            f.write("おはようございます！今日も一日頑張りましょう！ 🌟\n#朝活 #モチベーション")
        
        logging.info(f"Created example post structure: {folder_path}")
        return folder_path