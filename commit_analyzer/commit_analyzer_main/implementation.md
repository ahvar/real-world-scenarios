

## 📥 Group all commits by month year

Format: MM-YYYY


### Steps:

1. Convert the date to a datetime instance and get the month and year

2. Create a dict of commits for each mm-yyyy with string representation of month-year as keys

3. Add the commits for each month

4. Iterate through the commit dict, calculate the metrics below, store them in a dict, and append that dict to a list:

#### Metric	Description
 - commit_count:	Total number of commits in that month
 - average_message_length:	Average character length of commit messages
 - unique_authors:	Number of distinct commit authors (by email or name)