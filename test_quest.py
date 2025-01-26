import pytest
from quest import Quest, QuestStatus, Priority
from datetime import datetime, timedelta

# Quest Class Testing
    # Quest Creation
    # Quest Validation
    # Circular Dependency
    # Update Progress
    # Add Component

def create_quest(name, description, **kwargs):
    return Quest(name=name, description=description, **kwargs)

def test_quest_creation():
    due_date = datetime.now() + timedelta(days=1)
    
    quest = create_quest(
        name="Test Quest",
        description="This is a test quest.",
        rewards=["100 gold", "200 xp"],
        status=QuestStatus.IN_PROGRESS,
        progress=50.0,
        priority=Priority.MEDIUM,
        due_date=due_date
    )
    
    assert quest.name == "Test Quest"
    assert quest.description == "This is a test quest."
    assert quest.rewards == ["100 gold", "200 xp"]
    assert quest.status == QuestStatus.IN_PROGRESS
    assert quest.progress == 50.0
    assert quest.priority == Priority.MEDIUM
    assert isinstance(quest.created_at, datetime)
    assert quest.updated_at is None
    assert quest.due_date == due_date

def test_quest_validation():
    with pytest.raises(ValueError):
        create_quest(name="", description="This is a test quest.").validate_quest()
    
    with pytest.raises(ValueError):
        create_quest(name="Test Quest", description="").validate_quest()

def test_quest_circular_dependency():
    quest1 = create_quest(name="Quest 1", description="This is Quest 1.")
    quest2 = create_quest(name="Quest 2", description="This is Quest 2.")
    quest3 = create_quest(name="Quest 3", description="This is Quest 3.")
    
    quest1.add_subquest(quest2)
    quest2.add_subquest(quest3)
    quest3.add_subquest(quest1)
    
    with pytest.raises(ValueError):
        quest1.validate_quest()

def test_update_progress():
    quest = create_quest(name="Test Quest", description="This is a test quest.")
    
    quest.update_progress(50.0)
    assert quest.progress == 50.0
    
    with pytest.raises(ValueError):
        quest.update_progress(-10.0)
    
    with pytest.raises(ValueError):
        quest.update_progress(110.0)
    
def test_dates():
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_in_the_future = datetime.now() + timedelta(days=1)
    
    create_quest(name="Test Quest", description="This is a test quest.", due_date=one_day_in_the_future).validate_quest()
    
    with pytest.raises(ValueError):
        create_quest(name="Test Quest", description="This is a test quest.", due_date=one_day_ago).validate_quest()
    
    with pytest.raises(ValueError):
        create_quest(name="Test Quest", description="This is a test quest.", created_at=one_day_in_the_future, due_date=one_day_ago).validate_quest()
