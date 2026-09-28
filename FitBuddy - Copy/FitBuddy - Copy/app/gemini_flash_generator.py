from .gemini_client import GeminiService
from .schemas import UserInput


def generate_nutrition_tip_with_flash(user: UserInput) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip for this FitBuddy user.
Goal: {user.goal}
Age: {user.age}
Weight: {user.weight} kg
Intensity: {user.intensity}

Keep it to 2-4 sentences. Focus on generally safe habits such as hydration, balanced meals,
adequate protein, fruits/vegetables, sleep, and recovery. Do not prescribe supplements or
medical diets. Avoid exact calorie targets unless essential.
"""
    service = GeminiService()
    return service.generate(service.settings.gemini_tip_model, prompt)
