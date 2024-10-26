from crewai_tools import BaseTool
from typing import Any, Optional, Type
from pydantic import ConfigDict, BaseModel, Field
import praw
import os
import pprint
import tweepy
import requests
import json
from bs4 import BeautifulSoup

class RedditToolSchema(BaseModel):
    title: str
    reddit_topic: Optional[str] = "latest ai development"
    max_results: Optional[int] = 10

class RedditTool(BaseTool):
    name: str = "Returns reddit threads for a given topic."
    description: str = (
        "Returns reddit text for a given topic that is requested by a user to be investigated."
    )
    reddit_topic: Optional[str] = "latest ai development"
    max_results: Optional[int] = 10

    args_schema = RedditToolSchema

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reddit_topic = kwargs.get("reddit_topic", self.reddit_topic)
        self.max_results = kwargs.get("max_results", self.max_results)

    def _run(self, **kwargs: Any) -> Any:
        # Implementation goes here
        
        reddit = praw.Reddit(
            client_id=os.getenv('REDDIT_CLIENT_ID'),
            client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
            user_agent=os.getenv('REDDIT_USER_AGENT')
        )
        
        reddit_topic = kwargs.get("reddit_topic", self.reddit_topic)
        max_results = kwargs.get("max_results", self.max_results)

        df = reddit.subreddit("all").search(query=reddit_topic, limit=max_results)

        results = []

        for submission in df:
            results.append( 
                "" + submission.title.__str__()
                + "\n" + submission.selftext.__str__()
                + "\n" + submission.url.__str__()
                + "\n" + submission.author.__str__()
                + "\n" + submission.created_utc.__str__()
            )

        return results
    

class TwitterTool(BaseTool):
    name: str = "Returns tweets for a given topic."
    description: str = (
        "Returns twitter text for a given topic that is requested by a user to be investigated."
    )

    def _run(self, twitter_topic: str) -> str:
        # Implementation goes here

        print(os.getenv('TWITTER_BEARER_TOKEN'))

        client = tweepy.Client(bearer_token=os.getenv('TWITTER_BEARER_TOKEN'))

        response = client.search_recent_tweets(query=twitter_topic, max_results=10)
        
        if response.data:
            for tweet in response.data:
                print(f"Tweet: {tweet.text}, Created at: {tweet.created_at}")
        else:
            print("No tweets found.")


class YoutubeToolSchema(BaseModel):
    title: str
    hashtags: Optional[str] = "#ai #llms"
    max_results: Optional[int] = 10

class YoutubeTool(BaseTool):
    name: str = "Returns tweets for a given topic."
    description: str = (
        "Returns twitter text for a given topic that is requested by a user to be investigated."
    )
    hashtags: Optional[str] = "#ai #llms"
    max_results: Optional[int] = 10

    args_schema = YoutubeToolSchema


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hashtags = kwargs.get("hashtags", self.hashtags)
        self.max_results = kwargs.get("max_results", self.max_results)

    def _run(self,  **kwargs: Any) -> Any:
        """
        Queries YouTube API for videos with specific hashtags and sorts them by relevance and date.

            Parameters:
            
        query: Hashtag or search term to query (e.g., "#example").
        max_results: Maximum number of videos to return (default is 10).

        Returns:
        List of videos with title, video ID, published date, and URL.
        """

        API_KEY = os.getenv('YOUTUBE_API_KEY')
        BASE_URL = 'https://www.googleapis.com/youtube/v3/search'
        # Sorted by date (most recent first)
        query = kwargs.get("hashtags", self.hashtags)
        max_results = kwargs.get("max_results", self.max_results)

        params = {'part': 'snippet','q': query,'type': 'video','order': 'date', 'maxResults': max_results,'key': API_KEY}

        response = requests.get(BASE_URL, params=params)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return []

        videos = response.json().get('items', [])

        result = []
        for video in videos:
            video_data = {
                'title': video['snippet']['title'],
                'video_id': video['id']['videoId'],
                'published_at': video['snippet']['publishedAt'],
                'url': f"https://www.youtube.com/watch?v={video['id']['videoId']}"
            }
            result.append(video_data)

        return result

class SNIAToolSchema(BaseModel):
    title: str
    max_results: Optional[int] = 10

class SNIATool(BaseTool):
    name: str = "Returns relevant SNIA text for a given topic."
    description: str = (
        "Returns relevant SNIA text for a given topic including links to PDFS, article content, and more."
    )
    max_results: Optional[int] = 10

    args_schema = SNIAToolSchema


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_results = kwargs.get("max_results", self.max_results)

    def _run(self,  **kwargs: Any) -> Any:
        """
        Queries YouTube API for videos with specific hashtags and sorts them by relevance and date.

            Parameters:
            
        query: Hashtag or search term to query (e.g., "#example").
        max_results: Maximum number of videos to return (default is 10).

        Returns:
        List of videos with title, video ID, published date, and URL.
        """

        #API_KEY = os.getenv('YOUTUBE_API_KEY')
        BASE_URL = 'https://www.snia.org/news-events'
        # Sorted by date (most recent first)
        max_results = kwargs.get("max_results", self.max_results)

        #params = {'part': 'snippet','q': query,'type': 'video','order': 'date', 'maxResults': max_results,'key': API_KEY}

        #response = requests.get(BASE_URL, params=params)
        response = requests.get(BASE_URL)

        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            return None
        
        soupified = BeautifulSoup(response.text)
        
        pprint.pprint(soupified.get_text())
        pprint.pprint(soupified.find_all('a'))

        return None
