# learning_plans/ai_services.py

import os
import requests
import json
import time # Added this import to fix the TimeError in the backoff logic
from django.conf import settings
from django.shortcuts import get_object_or_404

# Assuming these models are importable from their respective apps
from learning_plans.models import LearningPlan 
from progress.models import ProgressItem

# NOTE: Key is now loaded from settings (which pulls from the .env file)
GEMINI_API_KEY = settings.GEMINI_API_KEY
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def get_mock_ai_response():
    """Returns a hardcoded, structured mock response for testing when the API key is missing."""
    return {
        "task_title": "Mock Task: Use Color-Coded Flashcards for Borrowing",
        "task_description": "Create 10 subtraction problems (3-digit minus 2-digit). Use red for the digit being 'borrowed from' and blue for the 'borrowed' 10, ensuring a strong visual cue. This task bypasses external API due to missing key.",
        "reasoning": "Progress history shows struggles specifically with the 'borrowing' mechanic. This adaptive task uses strong visual cues (color-coding) to reinforce the concept, a common neuro-adaptive technique."
    }

def generate_next_task_suggestion(plan_id):
    """
    Generates a personalized "Next Best Task" using the Gemini API 
    based on the student's progress history for a given plan.
    """
    try:
        # --- MOCKING LOGIC (Checks for a key indicating it's not a mock key) ---
        if not GEMINI_API_KEY or not GEMINI_API_KEY.startswith('AI_'):
            # The 'AI_' check is a common practice to differentiate a real key from a mock placeholder.
            return get_mock_ai_response()
        # ---------------------

        # 1. Gather Data for the Prompt
        learning_plan = get_object_or_404(LearningPlan, pk=plan_id)
        
        # Get the latest 10 progress items (to keep the context window small)
        progress_history = ProgressItem.objects.filter(
            learning_plan=learning_plan
        ).order_by('-created_at')[:10]

        # Format history into a simple list of dictionaries for the prompt
        # Use 'description' (FIXED BUG)
        history_data = [
            {
                "description": item.description, 
                "status": item.status,
                "completed_on": item.completed_at.strftime("%Y-%m-%d") if item.completed_at else "N/A"
            }
            for item in progress_history
        ]
        
        # 2. Construct the System and User Prompt
        system_prompt = (
            "You are an expert neuro-adaptive learning system (NeuroFix AI) designed to "
            "suggest the single best next learning task for a student with disabilities. "
            "Analyze the student's current learning plan and their progress history. "
            "Focus on suggesting a task that builds on successes or strategically addresses a weakness. "
            "Your output MUST be a JSON object conforming to the provided schema."
        )

        user_query = (
            f"The student's current plan is titled '{learning_plan.title}' "
            f"with the description: '{learning_plan.description}'. "
            f"Progress History (Most Recent First):\n{json.dumps(history_data, indent=2)}\n\n"
            "Based ONLY on this information, suggest the single, actionable, and specific 'Next Best Task' "
            "that aligns with the overall plan goals and the student's history."
        )

        # 3. Define the Structured Output Schema 
        response_schema = {
            "type": "OBJECT",
            "properties": {
                "task_title": {"type": "STRING", "description": "A concise, specific title for the next task (e.g., 'Practice 3-Digit Subtraction using a Visual Grid')."},
                "task_description": {"type": "STRING", "description": "A detailed, step-by-step description of the task, focusing on neuro-adaptive techniques."},
                "reasoning": {"type": "STRING", "description": "Brief, internal-use explanation of why this task was chosen based on the student's progress history (e.g., 'Student mastered addition but failed on carrying over in subtraction')."}
            },
            "required": ["task_title", "task_description", "reasoning"]
        }

        # 4. Construct the Full API Payload
        payload = {
            "contents": [{"parts": [{"text": user_query}]}],
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "config": {
                "responseMimeType": "application/json",
                "responseSchema": response_schema
            }
        }

        # 5. Make the API Request
        url_with_key = f"{GEMINI_API_URL}?key={GEMINI_API_KEY}"
        
        # Using a standard loop for exponential backoff (up to 3 retries)
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url_with_key, 
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload),
                    timeout=20 # Set a reasonable timeout
                )
                response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
                
                # Success
                result = response.json()
                
                # Extract the JSON text content
                json_text = result.get('candidates', [{}])[0] \
                                 .get('content', {}) \
                                 .get('parts', [{}])[0] \
                                 .get('text', '{}')
                
                # Parse the final JSON response
                return json.loads(json_text)

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    raise Exception(f"AI service failed after {max_retries} attempts: {e}")

    except Exception as e:
        # Catch any errors (e.g., plan not found, network failure, JSON parsing)
        return {"detail": f"Failed to generate task: {e}"}