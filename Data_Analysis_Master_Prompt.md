# Simple Dynamic Data Analysis Master Prompt

Use this prompt with an AI assistant that can access your project folder. The goal is to generate a clear, student-friendly Jupyter Notebook for whatever CSV data exists in the project.

## How to use
1. Open your AI assistant inside the project folder.
2. Copy the text between `BEGIN PROMPT` and `END PROMPT`.
3. Send it to the assistant.

---
**BEGIN PROMPT**
---

You are an expert data analyst and Python teacher.

I will not attach the CSV files manually. You have access to my project folder. Your job is to search the project, find all CSV files, understand the data, and create a complete Jupyter Notebook (`.ipynb`) for the data that exists in this project.

The notebook must be:
- beginner-friendly
- easy to read
- correct
- well explained
- suitable for students learning data analysis

## Important style rules
- Use simple Python and simple pandas code.
- Import all CSV files found in the project.
- Use normal `pd.read_csv()` statements.
- Do not use the `warnings` module unless absolutely necessary.
- Avoid unnecessary `numpy` logic if pandas can do the work clearly.
- Avoid complicated loop-heavy code when direct code is easier for students to read.
- Use short markdown explanations before every important code block.
- When multiple tables are merged, explain every merge separately in simple words.

## Required notebook structure

### 1. Title
Create a clear notebook title based on the actual dataset.

### 2. About the Data
Before any analysis, write a markdown section called `About the Data`.

In that section:
- explain what the data is about in simple words
- identify the likely business or project domain
- explain the role of each CSV file in 1-2 simple lines

### 3. Import All CSV Files
Search the project and import every CSV file you find.

Requirements:
- use direct `pd.read_csv()` code
- use clear variable names based on the filenames
- do not create a noisy "Found X CSV files" printout block unless it is truly needed

### 4. Basic Inspection
Show:
- row counts for all imported tables
- sample rows for the most important tables
- important column checks such as missing values and duplicate key checks

### 5. Data Cleaning
Clean the data based on the real columns that exist.

Examples:
- convert date columns to datetime
- handle obvious nulls
- remove or explain unnecessary columns if they are fully null
- check duplicate primary keys if relevant

Explain each cleaning step in simple language.

### 6. Feature Engineering
Create a few useful new columns based on the dataset.

Examples:
- year or month from a date
- number of days between two dates
- simple groups or categories from numeric columns

Explain why each new column is useful.

### 7. Merges and Master Table
If there are multiple related tables, build a final master table.

This section is very important.

For every merge:
- add a markdown heading for that merge step
- explain which two tables are being merged
- explain the key used for the merge
- explain why the merge is needed
- explain what new information is added after the merge

Then show the merge code.

If there is only one table, clearly say no merge is needed.

### 8. KPI Calculation
Calculate the most useful business or project KPIs based on the actual data.

Examples:
- total revenue
- total records
- average value
- completion rate
- top categories
- top customers
- top locations

Print the KPIs clearly.

### 9. Charts
Create a few simple charts using `matplotlib` and `seaborn`.

Suggested chart types:
- histogram for an important numeric column
- bar chart for an important category
- line chart for time trend if dates exist
- one grouped chart for comparison

After each chart, include 2-3 simple student-friendly interpretation points.

### 10. Final Summary
End with a short simple summary:
- what the data is about
- the most important result
- one or two key business or project insights

## Final requirement
The notebook must adapt to whatever CSV files are present in the project. Do not write generic filler. Use the real files, real columns, and real relationships found in the workspace.

---
**END PROMPT**
---
