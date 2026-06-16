# Password Auditor

Audits your exported browser password CSV file — locally. 
Nothing leaves your machine.

## What it checks
- Reused passwords across multiple sites
- Passwords that are too short
- Missing uppercase, numbers, or special characters
- Common passwords
- Passwords containing your username or site name

## How to use
1. Export from Chrome: `chrome://password-manager/passwords` → Settings → Export
2. Run: `python password_auditor.py`
3. Select your CSV when the file picker opens
4. Enter a name for your report
5. Open the report

## Requirements
Python 3. No external libraries needed.