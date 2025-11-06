 National ID Management System

A secure web-based application built with Flask and SQLite for managing citizen identity records. Designed for government or institutional use, it supports registration, verification, editing, and exporting of citizen data.

 Features

-  Admin login and profile management
-  Citizen registration with form validation
-  Identity verification by NIN
-  Edit and delete records
-  Export data to CSV
-  SQLite database integration
-  Responsive UI with static assets

 Tech Stack

- Backend: Flask (Python)
- Database: SQLite
- Frontend: HTML, CSS, JavaScript
  

 Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/nid_web_app.git
cd nid_web_app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
