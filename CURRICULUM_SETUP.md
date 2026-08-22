# Siksha Sahayak — Comprehensive Curriculum Seed

This build adds a **Class 5–10** curriculum across the six subjects already used by the project:

- Mathematics
- Science
- English
- History
- Geography
- Computer Science

Each topic receives:

- one detailed advanced study-material record;
- exactly 20 MCQ question-bank records;
- one 20-question quiz containing all 20 questions;
- mixed Easy / Medium / Hard difficulty;
- explanations for every answer.

## Run the seed

From the project root:

```bat
.venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_curriculum
python manage.py runserver
```

## Re-running

`seed_curriculum` is designed to refresh the topic content and recreate the chapter question bank + quiz for each curriculum topic. It does not delete users or unrelated data.

## Current scope

The command seeds Class 5 through Class 10 because those are the class levels currently represented by the original project seed. The curriculum list is defined near the top of `materials/management/commands/seed_curriculum.py`, so Class 1–4 or 11–12 can be added later by extending the `CLASSES` dictionary.
