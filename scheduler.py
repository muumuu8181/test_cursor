import schedule
import time
import logging
from datetime import datetime
from twitter_client import TwitterClient
from post_manager import PostManager
from config import Config

class AutoPoster:
    def __init__(self):
        self.config = Config()
        self.twitter_client = TwitterClient()
        self.post_manager = PostManager()
        self.running = False
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=getattr(logging, self.config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.LOG_FILE, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def check_and_post(self):
        """Check for pending posts and post them"""
        try:
            pending_posts = self.post_manager.get_pending_posts()
            
            if not pending_posts:
                logging.debug("No pending posts found")
                return
                
            for post in pending_posts:
                try:
                    logging.info(f"Posting: {post['folder_name']}")
                    
                    # Post to Twitter
                    tweet_id = self.twitter_client.post_with_image(
                        post['data']['message'],
                        post['data']['image_path']
                    )
                    
                    # Mark as processed
                    self.post_manager.mark_as_processed(post['folder_name'])
                    
                    logging.info(f"Successfully posted: {post['folder_name']} (Tweet ID: {tweet_id})")
                    
                except Exception as e:
                    logging.error(f"Failed to post {post['folder_name']}: {e}")
                    
        except Exception as e:
            logging.error(f"Error in check_and_post: {e}")
    
    def test_system(self):
        """Test the system setup"""
        logging.info("Testing system setup...")
        
        # Test Twitter connection
        if not self.twitter_client.test_connection():
            logging.error("Twitter connection failed")
            return False
            
        # Test post manager
        upcoming_posts = self.post_manager.get_upcoming_posts()
        logging.info(f"Found {len(upcoming_posts)} upcoming posts")
        
        for post in upcoming_posts[:3]:  # Show first 3
            logging.info(f"Upcoming: {post['folder_name']} at {post['post_time']}")
        
        logging.info("System test completed")
        return True
    
    def start_scheduler(self):
        """Start the posting scheduler"""
        self.setup_logging()
        logging.info("Starting Auto Poster...")
        
        # Test system first
        if not self.test_system():
            logging.error("System test failed. Please check configuration.")
            return
        
        # Schedule the check
        schedule.every(self.config.CHECK_INTERVAL_MINUTES).minutes.do(self.check_and_post)
        
        logging.info(f"Scheduler started. Checking every {self.config.CHECK_INTERVAL_MINUTES} minutes.")
        
        self.running = True
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user")
        except Exception as e:
            logging.error(f"Scheduler error: {e}")
        finally:
            self.running = False
    
    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        logging.info("Scheduler stopping...")
    
    def run_once(self):
        """Run the posting check once (for testing)"""
        self.setup_logging()
        logging.info("Running posting check once...")
        
        if self.test_system():
            self.check_and_post()
        
        logging.info("One-time run completed")

if __name__ == "__main__":
    poster = AutoPoster()
    poster.start_scheduler()