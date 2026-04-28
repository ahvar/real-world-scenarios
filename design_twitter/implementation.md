
# Twitter Class Implementation Guide (Based on Provided Code)

This guide describes how to implement a simple Twitter-like system as in the provided `Twitter` class. Each step explains the logic and purpose of the main components and methods.

## 1. Data Structures

- **Following Relationships:**
	- Use a `defaultdict(set)` called `_following` to map each user to the set of users they follow.
	- This allows fast addition, removal, and lookup of followees for any user.

- **Tweets Storage:**
	- Use a `defaultdict(list)` called `_tweets` to map each user to a list of their tweets.
	- Each tweet is stored as a tuple `(timestamp, tweetId)`, where `timestamp` is a global counter incremented for every new tweet.

- **Feed Limit:**
	- Set a constant `_feed_limit` (e.g., 10) to limit the number of tweets returned in the news feed.

- **Global Time:**
	- Use an integer `_time` as a global timestamp, incremented with each new tweet to ensure recency ordering across all users.

## 2. Methods and Their Logic

### `__init__`
Initializes the data structures:
- `_following`: Tracks who each user follows.
- `_tweets`: Stores each user's tweets.
- `_feed_limit`: Sets the maximum number of tweets in the feed.
- `_time`: Monotonic counter for tweet recency.

### `postTweet(userId: int, tweetId: int) -> None`
- Appends a new tweet for `userId`.
- Stores the tweet as `(current_time, tweetId)` in the user's tweet list.
- Increments the global `_time` counter.
- **Purpose:** Ensures each tweet has a unique, increasing timestamp for global ordering.

### `getNewsFeed(userId: int) -> List[int]`
- Collects the set of users whose tweets should appear in the feed: the user themself and everyone they follow.
- For each candidate user, if they have tweets, push their most recent tweet onto a max-heap (using negative timestamp for newest-first ordering).
- Repeatedly pop the newest tweet from the heap, add its `tweetId` to the feed, and if that user has more tweets, push the next most recent tweet from that user onto the heap.
- Continue until the feed has `_feed_limit` tweets or the heap is empty.
- **Purpose:** Efficiently merges the most recent tweets from multiple users, always returning the newest tweets first.

### `follow(followerId: int, followeeId: int) -> None`
- Adds `followeeId` to the set of users that `followerId` follows.
- Ignores the operation if a user tries to follow themselves.
- **Purpose:** Allows users to subscribe to other users' tweets.

### `unfollow(followerId: int, followeeId: int) -> None`
- Removes `followeeId` from the set of users that `followerId` follows, if present.
- Ignores the operation if a user tries to unfollow themselves.
- **Purpose:** Allows users to stop seeing another user's tweets in their feed.

## 3. Key Behaviors and Notes

- **Idempotency:**
	- Following or unfollowing the same user multiple times does not cause errors or duplicate relationships.

- **Empty States:**
	- If a user has no tweets and follows no one, their feed is empty.
	- Following or unfollowing non-existent users does not cause errors.

- **Feed Recency:**
	- The feed always returns the most recent tweets first, up to the feed limit.

## 4. Example Usage

```python
twitter = Twitter()
twitter.postTweet(1, 5)  # User 1 posts tweet 5
twitter.getNewsFeed(1)   # Returns [5]
twitter.follow(1, 2)     # User 1 follows user 2
twitter.postTweet(2, 6)  # User 2 posts tweet 6
twitter.getNewsFeed(1)   # Returns [6, 5]
twitter.unfollow(1, 2)   # User 1 unfollows user 2
twitter.getNewsFeed(1)   # Returns [5]
```

---
This guide matches the logic and structure of the provided implementation, focusing on clarity and practical steps for building the class and its methods.