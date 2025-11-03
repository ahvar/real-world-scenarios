## Simple Queries
1. View all tables and their structure:
 - Show all tables in the database
 - Display the schema for Authors and Commits tables

2. Count total commits and authors:
 - Get the total number of commits in the database
 - Count how many unique authors exist

3. List all authors:
 - Display all author names and emails, sorted alphabetically

4. Most recent commits:
 - Show the 10 most recent commits with date, message, and repository name

## Moderate Queries
5. Top contributors by commit count:
 - Find which authors have made the most commits
 - Include author name, email, and commit count
 - Sort by number of commits (highest first)

6. Average message length by author:
 - Calculate the average commit message length for each author
 - Only include authors with 3 or more commits
 - Show author name, commit count, and average message length

7. Monthly commit activity:
 - Group commits by month and year
 - Show commit count and number of unique authors per month
 - Sort by most recent months first

8. Find commits with longest/shortest messages:
 - Identify commits with the longest messages (top 5)
 - Find very short commit messages (under 20 characters)
 - Include author name and message preview

## More Complex Queries
9. Authors who haven't committed recently:
 - Find authors whose last commit was more than 30 days ago
 - Show author details and their last commit date

10. Commit patterns by day of week:
 - Analyze which days of the week have the most commits
 - Group by day name and count commits
 - Sort by commit frequency

11. Find duplicate commit messages:
 - Identify commit messages that appear multiple times
 - Show the message, occurrence count, and all authors who used it
 - Sort by frequency of duplication

12. Repository comparison:
 - Compare activity across different repositories
 - Show commit count, contributor count, and date range for each repo
 - Sort by total commits

## Advanced Analysis
13. Author collaboration (who commits to same repos):

Find pairs of authors who work on the same repositories
Count how many shared repositories each pair has
Identify the most collaborative author pairs
14. Commit message keyword analysis:

Count commits containing keywords like "fix", "feature", "bug", "test"
Analyze commit message patterns and categorize work types
15. Time-based commit frequency:

Analyze commit patterns by hour of day
Identify peak coding hours based on commit timestamps
Database Maintenance Operations
16. Find orphaned records (if any):

Check for any commits that reference non-existent authors
This shouldn't return anything due to foreign key constraints
17. Database statistics:

Get row counts for each table
Show overall database size and health metrics
