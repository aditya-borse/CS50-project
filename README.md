# PayTrackr - Analyzing PhonePe Transaction History with Flask

#### Video Demo: https://www.youtube.com/watch?v=7N76oGERle4

#### Description:

Welcome to PayTrackr, a Flask web application designed to help PhonePe users in India analyze their transaction history conveniently. In this detailed README, we'll walk through the structure of the project, the purpose of each file, and how to use the application effectively.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Usage](#usage)
4. [Understanding the Code](#understanding-the-code)

## Introduction

PayTrackr addresses a common issue faced by PhonePe users in India – the inability to export transaction history directly from the app. This Flask application takes an mbox file containing transaction-related emails sent by PhonePe and processes it to generate a user-friendly CSV file. The CSV file includes details such as date, time, transaction description, and amount spent. Additionally, the application provides an analysis summary on a web page and allows users to download the generated CSV file securely.

## Project Structure

The project consists of several files that work together to create the PayTrackr application:

- **app.py**: The main Flask application file. It handles routing, file uploads, processing, and result presentation. The file also manages temporary storage and deletion of CSV files after a certain period for user privacy.

- **helpers.py**: This file contains the `PayTrackr` function, which performs the actual processing of the mbox file. It uses regex to extract relevant information from each email and generates a CSV file. The `allowed_file` function checks if the uploaded file has a valid mbox extension.

- **templates directory**: Contains HTML templates used for rendering web pages. Notable templates include `layout.html` (the base template), `result.html` (displays the analysis summary), `apology.html` (renders an apology page in case of errors), and `upload.html` (handles file uploads).

## Usage

1. Follow the on-screen instructions to upload your emails as a mbox file and view the analysis summary.

2. Download the generated CSV file for further analysis.

## Understanding the Code

### app.py

#### Introduction
The `app.py` file is the main file of the PayTrackr Flask application. It defines various routes and handles the logic for uploading files, processing them, and presenting the analysis results.

#### Routes

1. `/` (index)
   - **Purpose**: Redirects users to the file upload page.
   - **Route Handler**: `index()` function.
   - **Implementation**: Uses Flask's `redirect` function to direct users to the `/upload` route.

2. `/upload`
   - **Purpose**: Manages file uploads, processes mbox files, and displays analysis results.
   - **Route Handler**: `upload_file()` function.
   - **Implementation**:
      - Handles both GET and POST requests.
      - On GET, renders the `upload.html` template, providing users with a file upload form.
      - On POST, checks for file validity, saves it temporarily, processes it using the `PayTrackr` function from `helpers.py`, and renders the `result.html` template with analysis results.

3. `/download`
   - **Purpose**: Allows users to download the generated CSV file.
   - **Route Handler**: `download_file()` function.
   - **Implementation**:
      - Retrieves the CSV file path from the session, copies it to a temporary directory, and sends it as an attachment to the user.
      - Initiates a timer to delete the temporary files after 10 seconds for user privacy.

4. `/apology`
   - **Purpose**: Displays an apology message in case of errors.
   - **Route Handler**: `apology()` function.
   - **Implementation**:
      - Renders the `apology.html` template, providing a customizable apology message.

5. `delete_file` Function
   - **Purpose**: Deletes temporary files after a specified time.
   - **Implementation**:
      - Called by the Timer in the `/download` route.
      - Removes temporary files and directories created during file processing.

#### Additional Notes

- The `MAX_CONTENT_LENGTH` configuration ensures that uploaded files do not exceed a specified size limit (100 MB in this case).
- A session variable (`csv_filename`) is used to pass the CSV file name between routes.

### helpers.py

#### Introduction
The `helpers.py` file contains the `PayTrackr` function, which performs the actual processing of mbox files to extract relevant transaction information and generates a CSV file.

#### PayTrackr Function

- **Purpose**: Processes mbox files and generates a CSV file with transaction details.
- **Parameters**: `mboxfile` - Path to the mbox file.
- **Implementation**:
   - Uses the `mailbox` module to read the mbox file.
   - Defines regex patterns to identify PhonePe transaction emails and extract relevant information.
   - Decodes email subjects, extracts date and time, and stores transaction details in a list.
   - Creates a CSV file with a timestamp and writes the transaction details.
   - Returns the list of results, total amount spent, and the CSV filename.

#### allowed_file Function

- **Purpose**: Checks if the uploaded file has a valid mbox extension.
- **Parameters**: `filename` - Name of the uploaded file.
- **Implementation**:
   - Uses the `rsplit` method to split the filename and check if the extension is 'mbox'.
   - Returns `True` if the file has a valid extension, `False` otherwise.

## Google Login Functionality (Future Work)

### The plan was to implement a secure and convenient way for users to log in using their Google accounts, granting access to their emails for automated processing. Unfortunately, due to technical challenges and insufficient experience in using OAuth, this feature is yet to be implemented. It remains a future goal for the project, aimed at providing users with a seamless and secure experience.
---