from .gemini_client import GeminiService


def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
You are updating an existing FitBuddy 7-day workout plan.

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Instructions:
- Preserve the useful structure of the original plan.
- Apply the user's feedback where it is reasonable and safe.
- Keep exactly 7 days.
- Maintain a suitable balance of training and recovery.
- Do not introduce dangerous volume, extreme dieting, or medical claims.
- Clearly label the result as an updated plan and briefly summarize the main changes first.
- If the feedback is unsafe or medically concerning, choose a safer alternative and say so briefly.
- Keep the output plain text and readable. Do not use markdown tables.
"""
    service = GeminiService()
    return service.generate(service.settings.gemini_workout_model, prompt)
