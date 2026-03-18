from typing import List
from collections import defaultdict
from dataclasses import dataclass

import heapq

"""
{followers: [], following: []}
"""


class Twitter:

    def __init__(self):
        self._following = defaultdict(set)
        self._tweets = defaultdict(list)
        self._feed_limit = 10
        self._time = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        post adds content for one user
        """
        self._tweets[userId].append((self._time, tweetId))
        self._time += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        candidates = set(self._following[userId])
        candidates.add(userId)

        heap = []

        for author_id in candidates:
            author_tweets = self._tweets.get(author_id, [])
            if not author_tweets:
                continue
            idx = len(author_tweets) - 1
            t, tw = author_tweets[idx]
            heapq.heappush(heap, (-t, tw, author_id, idx - 1))
        feed = []
        while heap and len(feed) < self._feed_limit:
            neg_t, tw, author_id, next_idx = heapq.heappop()
            feed.append(tw)

            if next_idx >= 0:
                t2, tw2 = self._tweets[author_id][next_idx]
                heapq.heappush(heap, (-t2, tw2, author_id, next_idx - 1))
        return feed

    def follow(self, followerId: int, followeeId: int) -> None:
        """
        adds subscription
        """
        if followerId == followeeId:
            return
        self._following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        removes subscription
        """
        if followerId == followeeId:
            return
        self._following[followerId].discard(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
