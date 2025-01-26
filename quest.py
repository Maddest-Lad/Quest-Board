from __future__ import annotations
from dataclasses import dataclass, field
import random
from typing import Optional
from uuid import uuid4
from datetime import datetime
from enum import Enum
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

@dataclass
class Quest:
    """
    A data object representing Quests.
    At a minimum, a quest has a name and a description.
    """
    name: str
    description: str
    id: str = field(default_factory=lambda: str(uuid4()))
    rewards: Optional[list[str]] = None
    subquests: Optional[list[Quest]] = None
    status: QuestStatus = QuestStatus.NOT_STARTED
    progress: float = 0.0  # 0.0 to 100.0
    priority: Optional[Priority] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    def validate_quest(self, visited=None):
        """
        Check if the quest is valid.
        A quest is valid if it has a name, a description, and doesn't contain circular quest dependencies.
        """
        if not self.name or not self.description :
            print(self.name, self.description)
            raise ValueError("Quest must have a name and a description")

        if visited is None:
            visited = set()
        if self.id in visited:
            raise ValueError(f"Circular dependency detected in quest: {self.name}")
        visited.add(self.id)

        if self.subquests:
            for subquest in self.subquests:
                subquest.validate_quest(visited)
                
        if self.due_date and self.due_date < datetime.now():
            raise ValueError("Due date must be in the future")
        
        if self.due_date and self.created_at > self.due_date:
            raise ValueError("Due date must be after creation")

                
    def add_subquest(self, subquest: Quest):
        """
        Add a subquest to the quest.
        """
        if self.subquests is None:
            self.subquests = []
        self.subquests.append(subquest)

    def update_progress(self, progress: float):
        """
        Update the progress of the quest.
        """
        if progress < 0 or progress > 100:
            raise ValueError("Progress must be between 0 and 100")
        self.progress = progress
        
    def __str__(self):
        return (f"{self.name} ({self.priority.name if self.priority else 'No Priority'}) - {self.description}\n"
            f"Status: {self.status.value}, Progress: {self.progress:.2f}%")
        
def generate_random_quests(number=1) -> list[Quest]:
    """
    Generate number random quests.
    """
    results = []
    
    try:
        with open('Resources\\Quests\\quests.csv', newline='', encoding='utf-8') as csvfile:
            quest_data = [(row['name'], row['description']) for row in csv.DictReader(csvfile)]
        with open('Resources\\Quests\\rewards.txt', 'r', encoding='utf-8') as rewardfile:
            rewards = rewardfile.read().splitlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Required file not found: {e.filename}")
        
    for i in range(number):
        name, description = quest_data.pop(random.randrange(len(quest_data)))
        reward = random.choice(rewards)
        priority = random.choice([Priority.LOW, Priority.MEDIUM, Priority.HIGH, Priority.CRITICAL])

        results.append(Quest(name=name, description=description, rewards=[reward], priority=priority))
        
    return results


if __name__ == "__main__":
    quests = generate_random_quests(5)
    [print(quest) for quest in quests]
