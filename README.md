# 🎓 YART - Yet Another Review Tool

## 📌 Project Overview

YART (Yet Another Review Tool) is a student project aimed at simplifying the process of managing code reviews. 

The project is built in **Python** and follows a structured approach with separate modules for configuration, 
models, services, and UI.  

---

## ⚙️ Technical Requirements

- **Programming Language:** Python3  
- **Database:** SQLite  
- **Version Control:** Git  
- **Honorable mentions:**
  - `PyQt5` – To create the graphical user interface  
  - `GitPython` – To handle Git operations in the application  
- **Testing Frameworks:** `pytest`, `pytest-qt`  

---

## 🚀 How to Run?

1. **Clone the repository:**
   ```commandline
   git clone https://github.com/YetAnotherReviewTool/YART.git
   cd YART
2. **Build the database and initial users**
    ```commandline
   py models/database_new.py
   py services/login_service.py
   ```
3. **Launch the app**
    ```commandline
   py main.py
   ```
4. **Enjoy! ✨**