#!/usr/bin/env python3
import argparse
import sys
from datetime import datetime, timedelta
import pytz
from scheduler import AutoPoster
from post_manager import PostManager
from config import Config

def main():
    parser = argparse.ArgumentParser(description='Twitter Auto Poster')
    parser.add_argument('--start', action='store_true', help='Start the scheduler')
    parser.add_argument('--test', action='store_true', help='Test the system')
    parser.add_argument('--once', action='store_true', help='Run posting check once')
    parser.add_argument('--upcoming', action='store_true', help='Show upcoming posts')
    parser.add_argument('--create-example', type=str, help='Create example post folder (format: YYYY-MM-DD_HH-MM)')
    
    args = parser.parse_args()
    
    if args.start:
        poster = AutoPoster()
        poster.start_scheduler()
    
    elif args.test:
        poster = AutoPoster()
        poster.setup_logging()
        poster.test_system()
    
    elif args.once:
        poster = AutoPoster()
        poster.run_once()
    
    elif args.upcoming:
        show_upcoming_posts()
    
    elif args.create_example:
        create_example_post(args.create_example)
    
    else:
        parser.print_help()

def show_upcoming_posts():
    """Show upcoming posts"""
    post_manager = PostManager()
    config = Config()
    
    print(f"\n=== Upcoming Posts ===")
    upcoming_posts = post_manager.get_upcoming_posts(days_ahead=14)
    
    if not upcoming_posts:
        print("No upcoming posts found.")
        return
    
    timezone = pytz.timezone(config.DEFAULT_TIMEZONE)
    now = datetime.now(timezone)
    
    for post in upcoming_posts:
        post_time = post['post_time']
        time_diff = post_time - now
        
        if time_diff.total_seconds() > 0:
            if time_diff.days > 0:
                time_str = f"in {time_diff.days} days"
            else:
                hours = int(time_diff.total_seconds() // 3600)
                minutes = int((time_diff.total_seconds() % 3600) // 60)
                time_str = f"in {hours}h {minutes}m"
        else:
            time_str = "now"
        
        message_preview = post['data']['message'][:50] + "..." if len(post['data']['message']) > 50 else post['data']['message']
        
        print(f"📅 {post['folder_name']}")
        print(f"   Time: {post_time.strftime('%Y-%m-%d %H:%M')} ({time_str})")
        print(f"   Message: {message_preview}")
        print(f"   Image: {post['data']['image_path']}")
        print()

def create_example_post(folder_name):
    """Create an example post"""
    post_manager = PostManager()
    
    # Validate folder name format
    if not post_manager.parse_folder_datetime(folder_name):
        print(f"Error: Invalid folder name format: {folder_name}")
        print("Supported formats:")
        print("  - YYYY-MM-DD_HH-MM (2024-01-15_14-30)")
        print("  - YYYY-MM-DD (2024-01-15)")
        print("  - YYYYMMDD_HHMM (20240115_1430)")
        print("  - YYYYMMDD (20240115)")
        return
    
    folder_path = post_manager.create_example_post(folder_name)
    print(f"Created example post structure: {folder_path}")
    print(f"Please add your image file to: {folder_path}")
    print(f"Edit the message file: {folder_path}/message.txt")

if __name__ == "__main__":
    main()