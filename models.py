from datetime import datetime
from uuid import uuid4
from sqlalchemy import String, Float, Enum as SqlEnum, DateTime, Text
from enum import Enum
from extensions import db
import random
import csv

class QuestStatus(Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FAILED = "Failed"


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class QuestModel(db.Model):
    __tablename__ = "quests"

    id = db.Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(String, nullable=False)
    description = db.Column(Text, nullable=False)
    rewards = db.Column(String)  # Comma-separated values for rewards
    status = db.Column(SqlEnum(QuestStatus), default=QuestStatus.NOT_STARTED)
    progress = db.Column(Float, default=0.0)  # 0.0 to 100.0
    priority = db.Column(SqlEnum(Priority))
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime)
    due_date = db.Column(DateTime)

    def validate(self):
        """
        Validate the quest instance.
        """
        if not self.name or not self.description:
            raise ValueError("Quest must have a name and a description")

        if self.due_date:
            if self.due_date < datetime.utcnow():
                raise ValueError("Due date must be in the future")
            if self.created_at and self.created_at > self.due_date:
                raise ValueError("Due date must be after creation")

    def update_progress(self, progress: float):
        """
        Update the progress of the quest.
        """
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be between 0 and 100")
        self.progress = progress

    def to_dict(self):
        """
        Convert the quest to a dictionary representation.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "rewards": self.rewards.split(",") if self.rewards else [],
            "status": self.status.value,
            "progress": self.progress,
            "priority": self.priority.name if self.priority else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
        }

    @classmethod
    def generate_random_quests(cls, number=1):
        """
        Generate a specified number of random quests.
        """
        results = []

        try:
            with open('Resources/Quests/quests.csv', newline='', encoding='utf-8') as csvfile:
                quest_data = [(row['name'], row['description']) for row in csv.DictReader(csvfile)]
            with open('Resources/Quests/rewards.txt', 'r', encoding='utf-8') as rewardfile:
                rewards = rewardfile.read().splitlines()
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Required file not found: {e.filename}")

        if number > len(quest_data):
            raise ValueError(f"Number of quests requested ({number}) exceeds available quest data ({len(quest_data)})")

        for _ in range(number):
            name, description = quest_data.pop(random.randrange(len(quest_data)))
            reward = random.choice(rewards)
            priority = random.choice([Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL])

            results.append(
                cls(
                    name=name,
                    description=description,
                    rewards=reward,
                    status=QuestStatus.NOT_STARTED,
                    progress=0.0,
                    priority=priority,
                    created_at=datetime.now()
                )
            )

        return results
