import csv
import tkinter as tk
from tkinter import filedialog

def load_common_passwords():
    common = []
    try:
        with open("common_pass.txt", "r") as file:
            for line in file:
                clean = line.strip()
                common.append(clean)
    except FileNotFoundError:
        print("Warning: common_passwords.txt not found. Wordlist check will be skipped.")
        
    return common

def get_file():
    root = tk.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename(
        title="Select your password CSV",
        filetypes=[("CSV files", "*.csv")]
    )
    return filename

def main():
    common_pass = load_common_passwords()
    entries = []
    filename = get_file()
    report_name = input("Save report as: ")
    if not filename:             
            print("No file selected.")
            return

    try:
        with open(filename, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                site = row["name"]
                username = row["username"]
                password = row["password"]
                entries.append([site, username, password])
    except FileNotFoundError:
        print("File not found! Please check the file name.")
        return
    
    with open(report_name, "w") as report:
        report.write("")
        password_to_sites = {}
        for entry in entries:
            username = entry[1]
            site = entry[0]
            password = entry[2]
        
            if password in password_to_sites:
                password_to_sites[password].append(site)
            else:
                password_to_sites[password] = [site]

        results = []            
        for entry in entries:
            username = entry[1]
            site = entry[0]
            pw = entry[2]
            sites_using_this_pw = password_to_sites[pw]
            has_issues = False
            warnings = []
        
            if len(sites_using_this_pw) > 1:
                warnings.append("- Warning: Reused password!")
                has_issues = True
            if is_too_short(pw):   
                warnings.append(" - Warning: Too short!")
                has_issues = True
            if not is_upper(pw):
                warnings.append(f" - Warning: Password has no uppercase letters!")
                has_issues = True
            if not is_digit(pw):
                warnings.append(f" - Warning: Password doesn't have digits!")
                has_issues = True 
            if not has_special_characters(pw):
                warnings.append(f" - Warning: Password doesn't have special characters!")
                has_issues = True
            if is_all_numbers(pw):
                warnings.append(f" - Warning: Password is all numbers!")
                has_issues = True
            if is_common(pw, common_pass):
                warnings.append(f" - Warning: Password is too common!")
                has_issues = True
            if contains_personal_info(pw, username, site):
                warnings.append(f" - Warning: Password contains personal info!")
                has_issues = True
            results.append({
                "site": site,
                "username": username,
                "warnings": warnings,
                "issue_count": len(warnings)
                })
        
        results.sort(key=lambda r: r["issue_count"], reverse=True)
        issues_found = 0
        for result in results:
            report.write(f" Website: {result['site']}\n")
            report.write(f" Username: {result['username']}\n")
            if result["warnings"]:
                for warning in result["warnings"]:
                    report.write(f"{warning}\n")
                issues_found += 1
            else:
                report.write(" - No issues found!\n")
            report.write("-------------------------\n")
            
        report.write(f"SUMMARY: {len(entries)} passwords audited. {issues_found} have issues.\n")
        print(f"Report saved to {report_name}")




def is_too_short(password):
    return len(password) < 8

def is_upper(password):
    for caps in password:
        if caps.isupper():
            return True
    return False

def is_digit(password):
    for digit in password:
        if digit.isdigit():
            return True
    return False

def has_special_characters(password):
    specials = "!@#$%^&*()-_=+[]{};:,.<>/?"
    for spec in password:
        if spec in specials:
            return True
    return False

def is_all_numbers(password):
    return password.isdigit()

def is_common(password, common_passwords):
    return password.lower() in common_passwords

def contains_personal_info(password, username, site_name):
    if username.lower() in password.lower():
        return True
    if site_name.lower() in password.lower():
        return True
    return False


main()