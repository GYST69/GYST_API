from rest_framework import serializers
from .models import Habit, HabitInstance
from rest_framework.validators import UniqueTogetherValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "name", "color", "description", "root_id", "habit_level")

    def validate(self, attrs):
        root_id = attrs.get("root_id")
        habit_level = attrs.get("habit_level")
        if root_id is not None and habit_level is not None:
            # Check if a habit with the same root_id and habit_level already exists
            queryset = Habit.objects.filter(root_id=root_id, habit_level=habit_level)
            if self.instance is not None:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    "Habit with this root_id and habit_level already exists."
                )
        return attrs


class HabitInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitInstance
        fields = ("id", "habit_id", "completed_at")
