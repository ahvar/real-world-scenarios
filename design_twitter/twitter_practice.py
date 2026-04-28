from collections import defaultdict
import heapq


class Twitter:

    def __init__(self):
        self._following = defaultdict(set)
        self._tweets = defaultdict(list)
        self._time = 0
        self._limit = 10

    def post_tweet(self, user_id, tweet_id):
        self._tweets[user_id].append((self._time, tweet_id))
        self._time += 1

    def get_news_feed(self, user_id):
        candidates = self._following.get(user_id, {})
        candidates.add(user_id)
        heap = []
        for candidate in candidates:
            tweets = self._tweets.get(candidate, [])
            if not tweets:
                continue
            idx = len(tweets) - 1
            t, tw = tweets[idx]
            heapq.heappush(heap, (-t, tw, candidate, idx - 1))
        feed = []
        while heap and len(feed) < self._limit:
            net_t, tw, author_id, next_idx = heapq.heappop()
            feed.append(tw)

            if next_idx >= 0:
                t2, tw2 = self._tweets[author_id][next_idx]
                heapq.heappush(heap, (-t2, tw2, author_id, next_idx - 1))

    def follow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        self._following[follower_id].add(followee_id)

    def unfollow(self, follower_id, followee_id):
        if follower_id == followee_id:
            return
        self._following[follower_id].discard(followee_id)
