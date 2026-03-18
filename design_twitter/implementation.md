# Twitter Design Implementation Steps

## Base Solution

1. Define the exact API behavior before building internals.
Write down what each operation must do: post adds content for one user, follow adds a subscription, unfollow removes a subscription, and news feed returns recent tweet identifiers. Decide the feed limit up front and keep that rule fixed for all tests.

2. Set clear data ownership for relationships.
Track follow relationships from the follower perspective so each user directly owns the set of accounts they follow. This makes follow and unfollow updates local, predictable, and easy to validate.

3. Set clear data ownership for tweets.
Store tweets under the author who created them, and keep each author history ordered by creation time. This guarantees fast append behavior and makes it straightforward to read the newest tweets first.

4. Establish a single global recency source.
Use one monotonic timeline for all tweets across all users. Every new tweet gets the next recency value so tweets from different users can be compared without ambiguity.

5. Implement posting as an atomic state update.
When processing a post, create one tweet record, assign recency immediately, and append to the author history in the same operation flow. The expected result is that a subsequent feed request can immediately see this tweet.

6. Implement follow with idempotent behavior.
Ensure repeated follow attempts do not create duplicate relationships or inconsistent state. If a relationship already exists, leave state unchanged and treat the operation as already satisfied.

7. Implement unfollow with safe removal semantics.
Remove a relationship only when present, and avoid errors when it is missing. Decide and document whether unfollowing self is ignored or blocked, then keep that behavior consistent.

8. Define feed membership precisely.
Build the candidate author set as the requesting user plus all currently followed users. Use only current relationships at request time so the feed reflects the latest follow and unfollow changes.

9. Retrieve feed items using newest-first multi-source selection.
Start from the newest tweet in each candidate author history, then repeatedly select the most recent available item across those authors. After selecting one item, advance only within that same author history and continue.

10. Enforce the feed size limit during retrieval.
Stop as soon as the required number of items is collected, even if more tweets exist. This keeps runtime tied to requested output size and avoids unnecessary scanning.

11. Define and verify empty-state behavior.
Confirm the system returns an empty feed for users with no own tweets and no followed tweets. Confirm follow and unfollow operations on unseen users do not crash and leave the system in a valid state.

12. Run operation-sequence validation.
Test realistic chains such as post then feed, follow then feed, unfollow then feed, and interleaved posts across multiple users. Verify ordering is always newest to oldest and that relationship changes are reflected immediately.

## Depth Upgrades

1. Replace ad hoc tweet records with a dedicated tweet model.
Define explicit fields for identity, recency, and payload so sorting intent is built into the data representation. This reduces accidental field misuse and clarifies feed merge behavior.

2. Upgrade collection initialization to automatic defaults.
Ensure relationship and tweet-history containers are created automatically the first time a user is referenced. This removes repetitive existence checks from core operation logic.

3. Add full type annotations to public and internal structures.
Annotate user identifiers, tweet identifiers, relationship mappings, tweet history mappings, and method returns. This helps static analysis catch mismatches before runtime.

4. Add reusable validation wrappers around state-changing operations.
Centralize common checks such as user existence normalization and invalid operation guards. Keep validation policy in one place so behavior is consistent across methods.

5. Add optional runtime measurement for performance study.
Wrap selected operations with timing instrumentation and record elapsed duration per call. Use this only for diagnostics so core behavior remains unchanged.

6. Add streaming-style feed retrieval as an internal option.
Provide a path that emits feed items incrementally, then keep the default external behavior returning a materialized list. This enables memory-friendly consumption while preserving API compatibility.

7. Re-run the full correctness suite after each upgrade.
After each enhancement, verify that operation outcomes, feed ordering, edge-case handling, and idempotency are unchanged. Treat any behavior drift as a regression and fix before moving on.