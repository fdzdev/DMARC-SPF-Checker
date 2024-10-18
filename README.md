# DMARC-SPF-Checker

## Overview

The **DMARC-SPF-Checker** is a Python-based application designed to analyze DMARC and SPF records for a list of domains. The tool provides insights into the email security policies of domains, logs the results for future reference, and offers options for sending spoofed emails for testing purposes. The application aims to enhance email security by ensuring domains are correctly configured with DMARC and SPF policies.
To run the program:
```
python3 mailwatch.py
```
The output will be:
```
Please enter the domains you want to check (comma-separated): {domain1}, {domain2}, {domain3}
```

![Analysis](https://github.com/Facuu35/DMARC-SPF-Checker/blob/main/Pictures/Screen0.png)

## Important
1. You need to add your own SMTP server in python_email_sender.py
2. You need to modify the receiver email address in mailwatch.py

## Features

1. **Email Sending Option**: 
   - Users can choose whether they want to send out a spoofed email.
   - If the user selects to send an email, the application prompts to execute `smtp.py`.

![Analysis](https://github.com/Facuu35/DMARC-SPF-Checker/blob/main/Pictures/Screen2.png)

2. **Logging Mechanisms**:
   - A comprehensive log is maintained of all records collected, including:
     - Timestamp
     - Domain
     - DMARC Record
     - SPF Record

![Analysis](https://github.com/Facuu35/DMARC-SPF-Checker/blob/main/Pictures/Screen1.png)

3. **DNS Collector Checks**:
   - Every time the DNS collector runs, it checks the logs for existing records.
   - If a matching record is found that is less than one day old, it will not be re-recorded. If the record is older, it will be executed again.

4. **Record Management**:
   - Allows users to add new records as needed.

5. **Flask Web Application**:
   - A Flask app is available to visualize all scanned records.
   - Users can select whether the scan was reported or not.

6. **Bounty Highlighting**:
   - The application allows users to highlight if a bounty was received for any reported vulnerabilities.

7. **Spoof Email Feature**:
   - Users can send a spoofed email directly from the Flask web application.

8. **SMTP Configuration**:
   - The web application allows users to configure SMTP settings for sending emails.

## Future Plans

This project aims to continuously improve email security analysis and visualization features. The following enhancements are planned:

- Complete the implementation of the logging system with timestamps for each recorded action.
- Develop user-friendly interfaces in the Flask application for managing and visualizing scanned records.
- Enhance the email spoofing feature to support more customizable options.
- Implement a notification system for highlighting bounties received based on reported vulnerabilities.

## Contribution

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bugs you may encounter.

## Issues / Ideas

Feel free to create a new issue if you have problems with the tool, or, would like to request an additional feature.
