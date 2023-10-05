# OccuLesuire-Project

This Python program provides a simple user information management system using a graphical user interface (GUI) built with Tkinter. It allows users to input and manage their information, including their name, date of birth, and occupation. The program also provides functionality to manage favorite sports and activities associated with each user.

Key Features
User Information Input: Users can input their name, date of birth (in the format YYYY-MM-DD), and occupation.

Unique ID Generation: The system generates a unique ID for each user, ensuring no duplicates.

Favorite Things Management: Users can input their favorite sport and activity.

Data Merging: The system merges user information and favorite things data.

Data Search: Users can search for information based on either ID or name.

How to Use
User Info Tab:

Input your Name, Date of Birth, and Occupation.
Click the "Submit User Info" button to save the information.
Favorite Things Tab:

Input your User ID or Name.
Click the "Show User Info to Submit" button to display user information.
Input your Favorite Sport and Favorite Activity.
Click the "Submit Favorite Things" button to save the favorite things.
Search Data Tab:

Click the "Search" button after submitting all information to search for your data.
Important Notes
Make sure to provide all required information in the respective fields before submitting.

Dates must be in the format YYYY-MM-DD.

Please submit information carefully as duplicate names are not allowed.

When searching, ensure you have submitted all relevant information.

How It Works
The program uses CSV files (user_info.csv, favorite_things.csv, merge.csv) to store and manage user data. Each file is used for a specific purpose:

user_info.csv: Stores user information (ID, Name, Date of Birth, Occupation).
favorite_things.csv: Stores favorite sports and activities.
merge.csv: Merges user information and favorite things data.
The program ensures data integrity by performing checks before saving or updating information.

Authors
[Your Name]
