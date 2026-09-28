from .gemini_client import GeminiService
from .schemas import UserInput


def generate_workout_gemini(user: UserInput) -> str:
    prompt = f"""
You are FitBuddy, a careful fitness-planning assistant.
Create a personalized 7-day beginner-to-intermediate workout plan.

User:
- Name: {user.username}
- Age: {user.age}
- Weight: {user.weight} kg
- Goal: {user.goal}
- Preferred intensity: {user.intensity}

Requirements:
1. Give exactly 7 days, clearly labeled Day 1 through Day 7.
2. Each day should contain Focus, Warm-up (5-10 minutes), Main workout with exercise names and sets/reps or duration, Rest guidance, and Cooldown/recovery.
3. Match the requested intensity and goal.
4. Include at least one sensible recovery/rest day.
5. Do not prescribe medical treatment, diagnose conditions, or encourage unsafe extreme dieting/training.
6. Mention that the user should stop if they experience sharp pain, dizziness, chest pain, or unusual symptoms and seek qualified medical advice.
7. Keep the plan practical for a normal gym/home setting; do not assume specialized equipment.
8. Do not claim that the plan replaces a doctor, physiotherapist, or qualified coach.

Return clean, readable plain text with headings. Do not use markdown tables.
"""
    service = GeminiService()
    return service.generate(service.settings.gemini_workout_model, prompt)
