from bs4 import BeautifulSoup
import json
import os
import requests
import random
import string
import sys
import time

class InstagramOSINT:
    def __init__(self, username):
        self.username = username
        self.useragents = [...]  # List of user agents

        self.profile_data = {}
        self.posts_data = []
        self.hashtags_data = []
        self.locations_data = []
        self.audience_demographics = {}
        self.competitors_influencers = []

    def scrape_profile(self):
        # Scrape profile data and store it in self.profile_data
        url = f"https://www.instagram.com/{self.username}/?__a=1"
        response = requests.get(url, headers={"User-Agent": random.choice(self.useragents)})
        data = response.json()
        self.profile_data = data["graphql"]["user"]

    def scrape_posts(self):
        if self.profile_data['is_private']:
            print("[*] Private profile, cannot scrape posts!")
            return

        for post in self.profile_data['edge_owner_to_timeline_media']['edges']:
            post_data = self.extract_post_data(post['node'])
            self.posts_data.append(post_data)

            # Extract hashtags and locations
            for hashtag in post_data['hashtags']:
                self.hashtags_data.append(self.extract_hashtag_data(hashtag))
            if post_data['location']:
                self.locations_data.append(self.extract_location_data(post_data['location']))

    def extract_post_data(self, post):
        return {
            "url": f"https://www.instagram.com/p/{post['shortcode']}/",
            "post_type": post['__typename'],
            "caption": post['edge_media_to_caption']['edges'][0]['node']['text'],
            "hashtags": [tag.name for tag in post['tags']],
            "mentions": [mention.username for mention in post['edge_media_to_tagged_user']['edges']],
            "location": post['location'],
            "likes_count": post['edge_liked_by']['count'],
            "comments_count": post['edge_media_to_comment']['count'],
            "posted_at": post['taken_at_timestamp'],
            "media_url": post['display_url']
        }

    def extract_hashtag_data(self, hashtag):
        url = f"https://www.instagram.com/explore/tags/{hashtag}/?__a=1"
        response = requests.get(url, headers={"User-Agent": random.choice(self.useragents)})
        data = response.json()
        return {
            "name": hashtag,
            "post_count": data['graphql']['hashtag']['edge_hashtag_to_media']['count'],
            "related_hashtags": [tag['name'] for tag in data['graphql']['hashtag']['edge_hashtag_to_related_tags']['edges']]
        }

    def extract_location_data(self, location):
        url = f"https://www.instagram.com/explore/locations/{location['id']}/?__a=1"
        response = requests.get(url, headers={"User-Agent": random.choice(self.useragents)})
        data = response.json()
        return {
            "name": location['name'],
            "latitude": location['lat'],
            "longitude": location['lng'],
            "post_count": data['graphql']['location']['edge_location_to_media']['count']
        }

    def extract_audience_demographics(self):
        url = f"https://www.instagram.com/api/v1/users/{self.profile_data['id']}/info/"
        response = requests.get(url, headers={"User-Agent": random.choice(self.useragents)})
        data = response.json()
        self.audience_demographics = {
            "age_distribution": data['user']['age_range'],
            "gender_distribution": data['user']['gender'],
            "location_distribution": data['user']['public_country']
        }

    def extract_competitors_influencers(self):
        competitors_url = f"https://www.instagram.com/graphql/query/?query_hash=your_competitors_query_hash&variables={{'user_id':'{self.profile_data['id']}'}}"
        response = requests.get(competitors_url, headers={"User-Agent": random.choice(self.useragents)})
        competitors_data = response.json()

        influencers_url = f"https://www.instagram.com/graphql/query/?query_hash=your_influencers_query_hash&variables={{'user_id':'{self.profile_data['id']}'}}"
        response = requests.get(influencers_url, headers={"User-Agent": random.choice(self.useragents)})
        influencers_data = response.json()

        # Process competitors data
        for competitor in competitors_data['data']['user']['edge_similar_accounts']['edges']:
            competitor_account = self.extract_account_data(competitor['node'])
            competitor_posts = self.extract_competitor_posts(competitor['node']['id'])
            engagement_metrics = self.calculate_engagement_metrics(competitor_posts)
            self.competitors_influencers.append({
                "account": competitor_account,
                "posts": competitor_posts,
                "engagement_metrics": engagement_metrics
            })

        # Process influencers data
        for influencer in influencers_data['data']['user']['edge_related_profiles']['edges']:
            influencer_account = self.extract_account_data(influencer['node'])
            influencer_posts = self.extract_influencer_posts(influencer['node']['id'])
            engagement_metrics = self.calculate_engagement_metrics(influencer_posts)
            self.competitors_influencers.append({
                "account": influencer_account,
                "posts": influencer_posts,
                "engagement_metrics": engagement_metrics
            })

    def extract_account_data(self, account):
        return {
            "username": account['username'],
            "account_type": account['business_category_name'],
            "bio": account['biography'],
            "website": account['external_url'],
            "profile_picture_url": account['profile_pic_url'],
            "followers_count": account['edge_followed_by']['count'],
            "following_count": account['edge_follow']['count'],
            "created_at": None,
            "is_verified": account['is_verified']
        }

    def extract_competitor_posts(self, user_id):
        # Extract competitor posts data using the provided user_id
        # Implement the logic based on the Instagram API or web scraping
        return []

    def extract_influencer_posts(self, user_id):
        # Extract influencer posts data using the provided user_id
        # Implement the logic based on the Instagram API or web scraping
        return []

    def calculate_engagement_metrics(self, posts):
        total_likes = sum(post['likes_count'] for post in posts)
        total_comments = sum(post['comments_count'] for post in posts)
        engagement_rate = (total_likes + total_comments) / len(posts)
        return {
            "average_likes": total_likes / len(posts),
            "average_comments": total_comments / len(posts),
            "engagement_rate": engagement_rate
        }

    def save_data(self):
        data = {
            "profile": self.profile_data,
            "posts": self.posts_data,
            "hashtags": self.hashtags_data,
            "locations": self.locations_data,
            "audience_demographics": self.audience_demographics,
            "competitors_influencers": self.competitors_influencers
        }
        with open(f"{self.username}_data.json", "w") as file:
            json.dump(data, file, indent=2)

def main():
    username = "example_username"
    osint = InstagramOSINT(username)
    
    osint.scrape_profile()
    osint.scrape_posts()
    osint.extract_audience_demographics()
    osint.extract_competitors_influencers()
    
    osint.save_data()

if __name__ == "__main__":
    main()
        
        
    
