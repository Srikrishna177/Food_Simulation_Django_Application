import json
import os
import random
import urllib

import requests
from typing import List

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from conversations.models import Conversation

class Command(BaseCommand):
    help = (
        "Simulate 100 conversations where ChatGPT A asks about top three "
        "favourite foods and ChatGPT B replies.  If an OPENAI_API_KEY is "
        "present in the environment, responses are fetched from the "
        "OpenAI API; otherwise, random foods are selected from a list."
    )

    # List of foods to fall back on when no API key is provided.
    FALLBACK_FOODS = [
        'tofu', 'salad', 'falafel', 'vegetable curry', 'fruit salad', 'rice',
        'lentil soup', 'quinoa bowl', 'hummus', 'pumpkin soup', 'avocado toast',
        'cheese pizza', 'paneer tikka', 'pasta alfredo', 'omelette', 'ice cream',
        'steak', 'chicken curry', 'hamburger', 'fish and chips', 'pork ribs',
        'bacon', 'lamb chops', 'turkey sandwich', 'beef stew'
    ]

    MEAT_KEYWORDS = [
        'beef', 'pork', 'lamb', 'steak', 'chicken', 'fish', 'turkey', 'bacon',
        'ham', 'sausage', 'rib', 'prawn', 'shrimp', 'crab', 'lobster',
        'hamburger', 'meat', 'sushi'
    ]
    DAIRY_EGG_KEYWORDS = [
        'cheese', 'paneer', 'cream', 'milk', 'egg', 'butter', 'yoghurt',
        'ghee', 'custard', 'ice cream'
    ]

    def _classify(self, foods: List[str]) -> tuple[bool, bool]:
        """Return (is_vegetarian, is_vegan) flags based on keyword heuristics."""
        lowercased = [f.lower() for f in foods]
        is_vegan = True
        is_vegetarian = True
        for food in lowercased:
            if any(k in food for k in self.MEAT_KEYWORDS):
                is_vegan = False
                is_vegetarian = False
                continue
            if any(k in food for k in self.DAIRY_EGG_KEYWORDS):
                is_vegan = False
        return is_vegetarian, is_vegan

    def handle(self, *args, **options) -> None:
        # Ensure default user exists
        User = get_user_model()
        username, password = 'user', 'password'
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password, email='user@example.com')
            self.stdout.write(self.style.SUCCESS(f"Created default user '{username}' with password '{password}'"))
        else:
            self.stdout.write(self.style.WARNING(f"Default user '{username}' already exists"))

        api_key = os.environ.get('OPENAI_API_KEY')
        use_openai = bool(api_key)
        if use_openai:
            self.stdout.write(self.style.SUCCESS("Using OpenAI API for ChatGPT responses."))
        else:
            self.stdout.write(self.style.WARNING("OPENAI_API_KEY not set; falling back to random responses."))

        # Clear existing conversations
        Conversation.objects.all().delete()

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}" if api_key else "",
            "Content-Type": "application/json",
        }

        num_conversations = 100
        for _ in range(num_conversations):
            foods = None
            vegetarian_flag = False
            vegan_flag = False
            if use_openai:
                # Compose a prompt that requests JSON output from ChatGPT
                messages = [
                    {
                        "role": "system",
                        "content": (
                            "You are a friendly human who loves food. When asked for your top favourite foods, "
                            "you will return a JSON object with keys 'foods', 'vegetarian' and 'vegan'."
                            "The value for 'foods' must be an array of exactly three food names. "
                            "'vegetarian' should be true if all of the foods are vegetarian (contain no meat), "
                            "and 'vegan' should be true if all of the foods are vegan (contain no animal products). "
                            "Do not mention that you are an AI and do not output any text outside of the JSON object."
                        ),
                    },
                    {"role": "user", "content": "What are your top three favourite foods?"},
                ]
                payload = {"model": "gpt-3.5-turbo", "messages": messages, "max_tokens": 150, "temperature": 0.7}
                try:
                    data_bytes = json.dumps(payload).encode("utf-8")
                    req = urllib.request.Request(url, data=data_bytes, headers=headers, method="POST")
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        if resp.status == 200:
                            resp_data = resp.read().decode("utf-8")
                            parsed = json.loads(json.loads(resp_data)["choices"][0]["message"]["content"])
                            foods_candidate = parsed.get("foods")
                            if isinstance(foods_candidate, list) and len(foods_candidate) >= 3:
                                foods = [str(f).strip() for f in foods_candidate][:3]
                                vegetarian_flag = bool(parsed.get("vegetarian"))
                                vegan_flag = bool(parsed.get("vegan"))
                except Exception:
                    foods = None
            if not foods:
                # fallback to random
                foods = random.sample(self.FALLBACK_FOODS, 3)
                vegetarian_flag, vegan_flag = self._classify(foods)
            else:
                # if ChatGPT indicates False or omits flags, use heuristic to fill in
                if not vegetarian_flag or not vegan_flag:
                    h_veg, h_vgn = self._classify(foods)
                    vegetarian_flag = vegetarian_flag or h_veg
                    vegan_flag = vegan_flag or h_vgn
            # save the record
            Conversation.objects.create(foods=foods, vegetarian=vegetarian_flag, vegan=vegan_flag)

        self.stdout.write(self.style.SUCCESS(f"Simulation complete: {num_conversations} conversations recorded."))
