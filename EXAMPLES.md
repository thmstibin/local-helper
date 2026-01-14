# 📚 Local Helper - Example Workflows

This document provides detailed examples of what you can do with Local Helper.

## 🗂️ File Organization

### Example 1: Organize Downloads by Type

**Request:**
```
Organize all files in my workspace by file type
```

**What happens:**
1. Agent scans all files in workspace
2. Groups files by extension (.pdf, .jpg, .txt, etc.)
3. Creates folders for each type
4. Moves files to appropriate folders
5. Reports summary of organized files

**Result:**
```
workspace/
├── pdf/
│   ├── document1.pdf
│   └── report.pdf
├── jpg/
│   ├── photo1.jpg
│   └── photo2.jpg
└── txt/
    └── notes.txt
```

### Example 2: Organize by Date

**Request:**
```
Organize files by modification date into monthly folders
```

**Result:**
```
workspace/
├── 2024-01/
│   └── old_file.txt
├── 2024-12/
│   └── recent_doc.pdf
└── 2025-01/
    └── new_file.xlsx
```

## 📄 Document Processing

### Example 3: Extract Data from Excel

**Request:**
```
Extract data from expenses.xlsx and create a summary
```

**What happens:**
1. Opens expenses.xlsx
2. Reads all sheets
3. Extracts data from each sheet
4. Creates a text summary with key information
5. Saves summary as expenses_summary.txt

### Example 4: Summarize Multiple PDFs

**Request:**
```
Create a summary report of all PDF files in the documents folder
```

**What happens:**
1. Finds all PDF files
2. Extracts text from each PDF
3. Generates summary for each document
4. Combines into a single report
5. Saves as pdf_summary_report.txt

## 🔍 Search Operations

### Example 5: Find Files by Content

**Request:**
```
Find all files containing the word "budget"
```

**What happens:**
1. Scans all text-based files
2. Searches content for "budget"
3. Returns list of matching files
4. Shows preview of matches

### Example 6: Find Recent Files

**Request:**
```
List all files modified in the last 7 days
```

**What happens:**
1. Checks modification dates
2. Filters files from last week
3. Sorts by date
4. Displays formatted list

## ⚡ Batch Operations

### Example 7: Rename Multiple Files

**Request:**
```
Rename all image files to include today's date
```

**What happens:**
1. Finds all image files (.jpg, .png, etc.)
2. Generates new names with date prefix
3. Renames each file
4. Reports renamed files

**Example result:**
```
photo.jpg → 2025-01-14_photo.jpg
image.png → 2025-01-14_image.png
```

### Example 8: Batch Convert Text Files

**Request:**
```
Convert all .txt files to uppercase and save as new files
```

**What happens:**
1. Reads each .txt file
2. Converts content to uppercase
3. Saves as filename_upper.txt
4. Preserves originals

## 📊 Report Generation

### Example 9: File Inventory Report

**Request:**
```
Create an inventory report of all files in the workspace
```

**Generated Report:**
```markdown
# File Inventory Report
Generated: 2025-01-14 10:30

## Summary
- Total Files: 45
- Total Size: 125.3 MB
- File Types: 8

## By Type
- PDF: 12 files (45.2 MB)
- XLSX: 8 files (32.1 MB)
- JPG: 15 files (28.5 MB)
- TXT: 10 files (0.5 MB)

## Recent Files
1. report.pdf (2025-01-14)
2. data.xlsx (2025-01-13)
3. notes.txt (2025-01-12)
...
```

### Example 10: Data Extraction Report

**Request:**
```
Extract all data from CSV files and create a combined report
```

**What happens:**
1. Finds all .csv files
2. Reads and parses each file
3. Extracts headers and row counts
4. Creates summary with preview data
5. Saves as csv_data_report.txt

## 🎯 Advanced Workflows

### Example 11: Clean Up Duplicates

**Request:**
```
Find and list all duplicate files based on filename
```

**What happens:**
1. Scans all files
2. Groups by filename (ignoring path)
3. Identifies duplicates
4. Creates report with duplicate groups
5. Suggests which to keep/remove

### Example 12: Archive Old Files

**Request:**
```
Move all files older than 6 months to an archive folder
```

**What happens:**
1. Checks modification dates
2. Identifies files older than 6 months
3. Creates "archive" folder
4. Moves old files to archive
5. Reports archived files

### Example 13: Extract Email Addresses

**Request:**
```
Find all email addresses in text files and create a contact list
```

**What happens:**
1. Reads all .txt files
2. Uses pattern matching to find emails
3. Removes duplicates
4. Creates formatted contact list
5. Saves as contacts.txt

### Example 14: Generate File Tree

**Request:**
```
Create a visual tree structure of all folders and files
```

**Generated Output:**
```
workspace/
├── documents/
│   ├── reports/
│   │   ├── q1_report.pdf
│   │   └── q2_report.pdf
│   └── notes.txt
├── images/
│   ├── photo1.jpg
│   └── photo2.jpg
└── data/
    └── sales.xlsx
```

## 🔄 Workflow Combinations

### Example 15: Complete Document Workflow

**Request:**
```
Process all invoices: extract data, organize by month, and create a summary report
```

**What happens:**
1. Finds all invoice files (PDF, Excel)
2. Extracts data from each invoice
3. Organizes into monthly folders
4. Generates summary report with totals
5. Creates backup of originals

### Example 16: Photo Organization Workflow

**Request:**
```
Organize all photos by date, rename with descriptive names, and create an index
```

**What happens:**
1. Finds all image files
2. Reads EXIF data for dates
3. Creates date-based folders
4. Renames with date + original name
5. Generates photo index with metadata

## 💡 Tips for Best Results

### Be Specific
❌ "Do something with my files"
✅ "Organize PDF files by creation date into yearly folders"

### Provide Context
❌ "Find documents"
✅ "Find all Word documents containing 'contract' in the legal folder"

### Break Down Complex Tasks
❌ "Clean up everything"
✅ "First organize by type, then remove duplicates, then archive old files"

### Use Natural Language
You can phrase requests naturally:
- "Can you help me organize my downloads?"
- "I need to find all invoices from last month"
- "Please create a summary of all the reports"

## 🚨 Safety Notes

### Automatic Backups
Before any destructive operation (delete, move, rename), Local Helper creates backups in `.backups/`

### Confirmation for Risky Operations
Some operations may require confirmation:
- Deleting multiple files
- Moving files outside workspace
- Overwriting existing files

### Undo Capability
Check operation history:
```python
# Operation history is logged
# You can review in local_helper.log
```

## 🎓 Learning from Examples

Start with simple tasks and gradually increase complexity:

1. **Beginner**: "List all PDF files"
2. **Intermediate**: "Organize files by type"
3. **Advanced**: "Extract data from all Excel files and create a combined report"
4. **Expert**: "Process invoices, extract totals, organize by vendor, and generate monthly summaries"

## 📝 Custom Workflows

You can create custom workflows by combining multiple requests:

```
1. "Find all expense reports from Q4"
2. "Extract totals from each report"
3. "Create a summary with monthly breakdown"
4. "Move processed reports to archive"
```

Each step builds on the previous one, creating a complete automated workflow.

