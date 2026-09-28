# FitBuddy – AI Fitness Plan Generator

FitBuddy is a FastAPI + Jinja2 + SQLite web application that uses Google Gemini models to generate a personalized 7-day workout plan, a concise nutrition/recovery tip, and an AI-updated plan from user feedback.

## Features

- User form: name, user ID, age, weight, goal, intensity
- Gemini-powered 7-day workout plan
- Gemini-powered nutrition/recovery tip
- Feedback-based workout plan regeneration
- SQLite persistence with SQLAlchemy
- Jinja2 HTML frontend
- Admin/coach page at `/view-all-users`
- FastAPI interactive API docs at `/docs`
- Health check at `/health`

## Project structure

```text
FitBuddy/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── gemini_client.py
│   ├── gemini_flash_generator.py
│   ├── gemini_generator.py
│   ├── main.py
│   ├── routes.py
│   ├── schemas.py
│   └── updated_plan.py
├── static/
│   └── styles.css
├── templates/
│   ├── all_users.html
│   ├── index.html
│   └── result.html
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## VS Code setup on Windows

1. Open this folder in VS Code.
2. Open Terminal → New Terminal.
3. Create a virtual environment:

```powershell
python -m venv venv
```

4. Activate it:

```powershell
venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
venv\Scripts\Activate.ps1
```

5. Install dependencies:

```powershell
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.
7. Put your Google Gemini API key in `.env`:

```text
GEMINI_API_KEY=your_real_key_here
```

The model names are configurable. Defaults are:

```text
GEMINI_WORKOUT_MODEL=gemini-2.5-pro
GEMINI_TIP_MODEL=gemini-2.5-flash
```

If a model is unavailable to your API account, change the corresponding environment variable to a model available in your account.

## Run

From the project root:

```powershell
uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000 — FitBuddy UI
- http://127.0.0.1:8000/docs — FastAPI Swagger docs
- http://127.0.0.1:8000/view-all-users — admin/coach view
- http://127.0.0.1:8000/health — health check

## Test

With the virtual environment activated:

```powershell
pytest
```

The included tests verify the homepage and health endpoint without calling Gemini.

## How the AI flow works

1. `/generate-workout` validates the submitted form.
2. `gemini_generator.py` asks Gemini for a 7-day plan.
3. `gemini_flash_generator.py` asks Gemini for a concise nutrition/recovery tip.
4. `database.py` stores the user and generated plan in SQLite.
5. `result.html` displays the plan and feedback form.
6. `/submit-feedback` retrieves the latest saved plan.
7. `updated_plan.py` sends the original plan plus feedback to Gemini.
8. The updated plan and feedback are saved separately so the original plan is preserved.

## Important notes

- This is a student/demo health-tech project, not a medical device.
- Do not put `.env` or your API key into GitHub.
- The admin page is intentionally simple for the project specification; add authentication/authorization before real-world deployment.
- The generated workout content should be treated as general wellness guidance and reviewed by a qualified professional when appropriate.
