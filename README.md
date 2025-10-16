# Math_tests

A web application for managing, taking, and evaluating math tests & quizzes.  
This project includes backend logic, front-end views, and test management features.

---

##  Features

- Create, edit, and delete math tests / quizzes  
- Add questions, solutions, hints  
- Take tests and receive feedback / scores  
- Mark tests as “completed” and record results  
- Admin interface for test management  
- Front-end views for test-taking and review  

---

## Project Structure

Math_tests/
├── testsite/ # Main Django (or web framework) app
├── staticfiles/ # CSS, JS, images
├── manage.py
├── import_data.py
├── README.md
├── Requirements.txt
└── db.sqlite3 # default database (local development)

---

##  Installation & Setup

1. Clone the repository:  
   ```bash
   git clone https://github.com/KenyanWarriorTea/Math_tests.git
   cd Math_tests
2. Create virtual environment & install dependencies:
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   pip install -r Requirements.txt
3. Apply migrations and run server:
   python manage.py migrate
   python manage.py runserver

4. python manage.py migrate
   python manage.py runserver


Usage Example

1.Log in / sign up as admin

2.Create a test by adding questions and solutions

3.Go to “Take Test” page, answer questions

4.View result / feedback page

5.Admin dashboard allows editing / deleting tests

License

This project is licensed under the MIT License. See the LICENSE file for details.

