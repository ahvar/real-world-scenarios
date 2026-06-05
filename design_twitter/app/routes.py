from flask import Blueprint
from collections import defaultdict
from flask import request
import heapq

bp = Blueprint("routes", __name__)

tweets = defaultdict(list)
following = defaultdict(set)
limit = 10
time = 0

bp.route("/user/<int:user_id>")


def get_user(user_id):
    pass


@bp.route("/tweet/<user_id>/<tweet_id>")
def post_tweet(user_id, tweet_id):
    tweets[user_id].append((time, tweet_id))
    time += 1


@bp.route("/feed/<user_id>")
def get_news_feed(user_id):
    followees_and_user = following.get(user_id, set())
    followees_and_user.add(user_id)

    heap = []
    for user in followees_and_user:
        tweets = tweets.get(user, [])
        if not tweets:
            continue

        idx = len(tweets) - 1
        t, tw = tweets[idx]
        heapq.heappush((-t, tw, user, idx - 1))

    feed = []
    while heap and len(feed) < limit:
        neg_t, tw, user, idx = heapq.heappop()
        feed.append(tw)
        if idx > 0:
            t, tw = tweets[idx - 1]
            heapq.heappush((-t, tw, user, idx - 1))


@bp.route("/follow/<follower_id>/<followee_id>")
def follow(follower_id, followee_id):
    if follower_id == followee_id:
        return
    following[follower_id].add(followee_id)


@bp.route("/unfollow/<follower_id>/<followee_id>")
def unfollow(follower_id, followee_id):
    if follower_id == followee_id:
        return
    following[follower_id].discard(followee_id)
