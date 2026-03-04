# Student Engagement & Performance Analytics Dashboard

An interactive web dashboard built with **Python**, **Plotly Dash**, and **Pandas** for analyzing student engagement, attendance behavior, parent involvement, and academic performance from the xAPI Education Dataset.

---

## Features

- **7 Dynamic Filters** — Gender, Academic Stage, Grade, Subject/Topic, Semester, Parent Satisfaction, Absence Category
- **7 KPI Cards** — Total students, High/Medium/Low performer percentages, average engagement metrics
- **Performance Overview** — Pie chart, bar by gender, bar by stage
- **Engagement Analytics** — Raised hands, visited resources, scatter plot, box plot by performance
- **Attendance & Parent Insights** — Absence impact, parent satisfaction, and parent survey charts
- **Interactive DataTable** — Sortable, paginated, filtered in real-time

---

## Installation

### 1. Clone / Navigate to the project directory
```bash
cd student_dashboard
```

### 2. (Recommended) Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running the App

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:8050
```

---

## Dataset

The dashboard reads `xAPI-Edu-Data.csv` located in the same directory as `app.py`.

| Column | Description |
|--------|-------------|
| `gender` | Student gender (M/F) |
| `NationalITy` | Nationality |
| `StageID` | Academic stage (lowerlevel, MiddleSchool, HighSchool) |
| `GradeID` | Grade level |
| `Topic` | Subject |
| `Semester` | Semester (F/S) |
| `raisedhands` | Times student raised hand in class |
| `VisITedResources` | Times student visited course resources |
| `AnnouncementsView` | Times student checked announcements |
| `Discussion` | Times student participated in discussion |
| `ParentAnsweringSurvey` | Whether parent answered survey (Yes/No) |
| `ParentschoolSatisfaction` | Parent satisfaction (Good/Bad) |
| `StudentAbsenceDays` | Absence category (Under-7 / Above-7) |
| `Class` | Final performance: L = Low, M = Medium, H = High |

---

## Tech Stack

- **Python 3.8+**
- **Dash** — Web framework for analytical apps
- **Plotly Express** — Interactive chart library
- **Pandas** — Data manipulation
- **Dash DataTable** — Interactive sortable table
