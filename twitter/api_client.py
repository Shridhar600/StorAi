import tweepy
from typing import Optional
from config.settings import (
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)


class TwitterClient:
    """Handles posting tweets to Twitter"""
    
    def __init__(self):
        # Authenticate with Twitter
        auth = tweepy.OAuth1UserHandler(
            TWITTER_API_KEY,
            TWITTER_API_SECRET,
            TWITTER_ACCESS_TOKEN,
            TWITTER_ACCESS_SECRET
        )
        self.api = tweepy.API(auth)
        
        # Verify credentials
        try:
            self.api.verify_credentials()
            print("Twitter authentication successful")
        except Exception as e:
            print(f"Twitter authentication failed: {e}")
    
    def post_tweet(self, text: str) -> Optional[str]:
        """Post a tweet and return its ID"""
        try:
            response = self.api.update_status(text)
            print(f"Tweet posted successfully: {response.id}")
            return response.id
        except Exception as e:
            print(f"Error posting tweet: {e}")
            return None