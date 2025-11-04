# Data Transformations with Linux CLI Tools

## 🧪 COVID Data Science Exercises

Learn data science fundamentals using Linux command-line utilities to fetch, clean, explore, and analyze real-world COVID data.

---

## 📊 Dataset Overview

We'll work with COVID-19 historical data from the Disease.sh API:
- **Source**: `https://disease.sh/v3/covid-19/historical/usa?lastdays=10`
- **Format**: JSON with nested data structure
- **Contains**: Daily cases, deaths, and recovered counts for the USA (last 10 days)

---

## 🎯 Exercise 1: Fetch and Explore Raw Data
**Difficulty**: Beginner  
**Goal**: Get familiar with the data structure and basic JSON handling

### Tasks:
1. **Fetch the data** using `curl`
2. **Pretty-print** the JSON to understand its structure
3. **Count** how many lines the response contains
4. **Extract** just the country name from the response

### Commands to Learn:
- `curl` - Fetch data from web APIs
- `jq` - Parse and format JSON data
- `wc` - Count lines, words, characters
- `grep` - Search for patterns in text

### Expected Output:
```bash
# Pretty-formatted JSON showing nested structure
# Line count of the response
# Country name: "USA" or "US"
```

---

## 🎯 Exercise 2: Extract and Structure Case Data
**Difficulty**: Beginner-Intermediate  
**Goal**: Transform nested JSON into a flat, workable format

### Tasks:
1. **Extract daily case numbers** from the nested JSON structure
2. **Convert** the data into a simple two-column format: `date,cases`
3. **Save** the result to a CSV file named `cases.csv`
4. **Display** the first and last 3 rows to verify the data

### Commands to Learn:
- `jq` with advanced selectors (`.timeline.cases`)
- Output redirection (`>`)
- `head` and `tail` - View beginning/end of files
- CSV formatting concepts

### Expected Output:
```
date,cases
2024-10-25,12345
2024-10-26,12456
...
```

---

## 🎯 Exercise 3: Data Cleaning and Validation
**Difficulty**: Intermediate  
**Goal**: Clean the data and handle any inconsistencies

### Tasks:
1. **Check for missing values** in your cases.csv file
2. **Remove any duplicate dates** if they exist
3. **Sort** the data by date (chronologically)
4. **Validate** that all case numbers are positive integers
5. **Count** how many valid data points you have

### Commands to Learn:
- `sort` - Sort data by columns
- `uniq` - Remove duplicates
- `awk` - Process and validate data fields
- `grep -v` - Exclude lines matching patterns
- Pipe chaining for complex operations

### Expected Output:
```
# Number of missing values: 0
# Number of duplicate dates: 0
# Number of valid data points: 10
# Clean, sorted CSV file
```

---

## 🎯 Exercise 4: Statistical Analysis
**Difficulty**: Intermediate  
**Goal**: Calculate basic statistics about COVID trends

### Tasks:
1. **Calculate** the total cases across all days
2. **Find** the day with the highest case count
3. **Find** the day with the lowest case count
4. **Calculate** the average daily cases
5. **Determine** if cases are trending up or down (compare first vs last day)

### Commands to Learn:
- `awk` for mathematical operations
- `sort -n` - Numerical sorting
- `tail -1` and `head -1` - Get specific rows
- Arithmetic operations in shell
- Pattern matching and comparison

### Expected Output:
```
Total cases: 125,430
Highest day: 2024-10-28 (13,245 cases)
Lowest day: 2024-10-22 (11,892 cases)
Average daily cases: 12,543
Trend: INCREASING (cases up by 456 from start to end)
```

---

## 🎯 Exercise 5: Advanced Analysis and Reporting
**Difficulty**: Intermediate-Advanced  
**Goal**: Create a comprehensive data report with multiple metrics

### Tasks:
1. **Fetch deaths and recovered data** in addition to cases
2. **Calculate mortality rate** (deaths/cases) for each day
3. **Create a summary report** showing:
   - Daily statistics (cases, deaths, recovered)
   - Weekly totals and averages
   - Rate of change between consecutive days
   - Key insights and trends
4. **Format** the report in a readable table format
5. **Save** multiple output files: `daily_stats.csv`, `summary_report.txt`

### Commands to Learn:
- Multiple `jq` extractions and joins
- `paste` - Combine multiple files side-by-side
- `bc` - Calculator for decimal arithmetic
- `printf` - Format output nicely
- Complex `awk` scripts for calculations
- `column` - Format data in aligned columns

### Expected Output:
```
=== COVID-19 DATA ANALYSIS REPORT ===
Date Range: 2024-10-19 to 2024-10-28

DAILY AVERAGES:
Cases: 12,543
Deaths: 245
Recovered: 11,890
Mortality Rate: 1.95%

TRENDS:
Cases: +3.2% increase
Deaths: -1.1% decrease
Recovery Rate: 94.8%

HIGHEST SINGLE DAY:
2024-10-26: 13,456 cases, 267 deaths
```

---

## 🛠️ Required Tools

Ensure these tools are installed on your system:
```bash
# Check if tools are available
curl --version
jq --version
awk --version
sort --version
grep --version
```

If missing, install with:
```bash
# Ubuntu/Debian
sudo apt-get install curl jq gawk coreutils

# macOS
brew install curl jq
```

---

## 📋 Getting Started

1. **Create a working directory**:
   ```bash
   mkdir covid-analysis
   cd covid-analysis
   ```

2. **Test your connection**:
   ```bash
   curl -s "https://disease.sh/v3/covid-19/historical/usa?lastdays=10" | head -5
   ```

3. **Start with Exercise 1** and work through progressively

---

## 💡 Helpful Tips

### JSON Structure Preview:
The API returns data in this format:
```json
{
  "country": "USA",
  "timeline": {
    "cases": {
      "10/19/24": 103436829,
      "10/20/24": 103449915,
      ...
    },
    "deaths": {
      "10/19/24": 1127152,
      ...
    },
    "recovered": {
      "10/19/24": 0,
      ...
    }
  }
}
```

### Key `jq` Patterns:
- `.timeline.cases` - Extract cases object
- `.timeline.cases | to_entries` - Convert to key-value pairs
- `.[] | [.key, .value]` - Extract date and value
- `@csv` - Format as CSV

### Common Pitfalls:
- API date format is MM/DD/YY, not YYYY-MM-DD
- Some values might be cumulative, not daily
- Handle empty or null values gracefully
- Remember to use `-s` flag with curl for silent operation

---

## 🎖️ Success Criteria

By completing these exercises, you should be able to:
- ✅ Fetch data from REST APIs using `curl`
- ✅ Parse and transform JSON data with `jq`
- ✅ Clean and validate datasets using standard Unix tools
- ✅ Perform statistical calculations with `awk` and `bc`
- ✅ Create professional data analysis reports
- ✅ Chain multiple commands efficiently with pipes
- ✅ Handle real-world data inconsistencies and edge cases

---

## 🚀 Extension Challenges

Once you complete the main exercises:

1. **Automate** the entire analysis pipeline with a shell script
2. **Compare** multiple countries' data by modifying the API endpoint
3. **Create visualizations** using `gnuplot` or similar CLI tools
4. **Set up monitoring** that runs the analysis daily and emails results
5. **Add error handling** for network failures and malformed data

Good luck with your data science journey using the command line! 📈