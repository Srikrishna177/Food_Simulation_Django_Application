from django.db import models


class Conversation(models.Model):
    """
    Represents a simulated conversation entry where a user lists their
    top three favourite foods.  The foods are stored in a JSON field.
    The record also records whether the foods are vegetarian/vegan.
    """

    foods = models.JSONField(help_text="List of three favourite foods")
    vegetarian = models.BooleanField(default=False)
    vegan = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:  # pragma: no cover - developer convenience
        return f"Conversation {self.id}: {self.foods}"