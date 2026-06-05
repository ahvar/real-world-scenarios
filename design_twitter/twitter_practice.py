from collections import defaultdict
import heapq


class Twitter:

    def __init__(self):
        self._following = defaultdict(set)
        self._tweets = defaultdict(list)
        self._limit = 10
        self._time = 0

    def post_tweet(self, user_id, tweet_id):
        self._tweets[user_id].append((self._time, tweet_id))
        self._time += 1

    def get_news_feed(self, user_id):
        followees_and_user = self._following.get(user_id, set())
        followees_and_user.add(user_id)

        heap = []
        for user in followees_and_user:
            tweets = self._tweets.get(user, [])
            if not tweets:
                continue

            idx = len(tweets) - 1
            t, tw = tweets[idx]
            heapq.heappush((-t, tw, user, idx - 1))

        feed = []
        while heap and len(feed) < self._limit:
            neg_t, tw, user, idx = heapq.heappop()
            feed.append(tw)
            if idx > 0:
                t, tw = tweets[idx - 1]
                heapq.heappush((-t, tw, user, idx - 1))

    def follow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        self._following[follower_id].add(followee_id)

    def unfollow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        self._following[follower_id].discard(followee_id)
