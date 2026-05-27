"""
Code Documentation Exercise
==================================================
Algorithm chosen: Task Priority Sorting (Calculate_Task_Score)

This file contains four sections:
1.Original Code
2.Prompt 1
3.Prompt 2
4.Final combined documentation
"""

from datetime import datetime
from models import TaskPriority, TaskStatus


#=================================================================
#Section 1: Original code
#==================================================================

def calculate_task_score(task):
    """Calculate a priority score for a task based on multiple factors."""
    # Base priority weights
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Calculate base score from priority
    score = priority_weights.get(task.priority, 0) * 10

    # Add due date factor (higher score for tasks due sooner)
    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:  # Overdue tasks
            score += 35
        elif days_until_due == 0:  # Due today
            score += 20
        elif days_until_due <= 2:  # Due in next 2 days
            score += 15
        elif days_until_due <= 7:  # Due in next week
            score += 10

    # Reduce score for tasks that are completed or in review
    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    # Boost score for tasks with certain tags
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Boost score for recently updated tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score

def sort_tasks_by_importance(tasks):
    """Sort tasks by calculated importance score (highest first)."""
    # Calculate scores once and sort by the score
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks

def get_top_priority_tasks(tasks, limit=5):
    """Return the top N priority tasks."""
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]

#==============================================================================
#Section 2 :Promt 1- Comprehensive Function Documentation
#
#Prompt used:
#"Please create comprehensive documentation for this function following
#    Google-style Python docstring conventions. Include: a clear description
#    of what the function does, all parameters with types and descriptions,
#    return value with type and description, any exceptions or errors that
#    might be thrown, example usage, and any important notes or edge cases
#    developers should be aware of."
#===============================================================================

def calculate_task_score_prompt1(task):
    """Calculates a numeric priority score for a task based on multiple factors.

    Combines five factors into a single integer score: the task's base
    priority level, how soon it is due, its current status, whether it
    carries critical tags, and how recently it was updated. A higher score
    means the task should be actioned sooner.

    Args:
        task (Task): A Task object with the following attributes:
            - priority (TaskPriority): Enum value — LOW, MEDIUM, HIGH, or URGENT.
            - due_date (datetime | None): The deadline, or None if not set.
            - status (TaskStatus): Enum value — TODO, IN_PROGRESS, REVIEW, or DONE.
            - tags (list[str]): List of tag strings attached to the task.
            - updated_at (datetime): Timestamp of the last update to the task.

    Returns:
        int: A numeric score representing the task's urgency and importance.
             Higher scores indicate higher priority. Typical range is roughly
             -10 (completed low-priority task) to 84 (overdue urgent task
             updated today with a critical tag).

             Score breakdown:
             - Base priority:   LOW=10, MEDIUM=20, HIGH=40, URGENT=60
             - Overdue:         +35
             - Due today:       +20
             - Due in 1-2 days: +15
             - Due in 3-7 days: +10
             - Status DONE:     -50
             - Status REVIEW:   -15
             - Critical tag:    +8
             - Updated today:   +5

    Raises:
        AttributeError: If the task object is missing any required attribute
            (priority, due_date, status, tags, updated_at).
        TypeError: If task.due_date is set but is not a datetime object,
            causing the subtraction from datetime.now() to fail.

    Example:
        >>> from models import Task, TaskPriority, TaskStatus
        >>> from datetime import datetime, timedelta
        >>>
        >>> task = Task("Fix login bug", priority=TaskPriority.HIGH)
        >>> task.due_date = datetime.now() + timedelta(days=1)  # due tomorrow
        >>> task.tags = ["blocker"]
        >>>
        >>> score = calculate_task_score(task)
        >>> print(score)
        68  # HIGH base (40) + due in 2 days (15) + blocker tag (8) + updated today (5)

    Notes:
        - Tasks with no due_date receive no date bonus — they are scored
          purely on priority, status, tags, and recency.
        - A DONE task will almost always score negatively relative to active
          tasks due to the -50 penalty, effectively pushing it to the bottom
          of any sorted list.
        - The "updated today" boost (days_since_update < 1) uses integer day
          difference, so a task updated 23 hours ago still qualifies.
        - Tag matching is case-sensitive: "Blocker" will NOT trigger the
          critical tag boost — only lowercase "blocker", "critical", "urgent".
        - The function does not mutate the task object in any way.
    """
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }
    score = priority_weights.get(task.priority, 0) * 10

    if task.due_date:
        days_until_due = (task.due_date - datetime.now()).days
        if days_until_due < 0:
            score += 35
        elif days_until_due == 0:
            score += 20
        elif days_until_due <= 2:
            score += 15
        elif days_until_due <= 7:
            score += 10

    if task.status == TaskStatus.DONE:
        score -= 50
    elif task.status == TaskStatus.REVIEW:
        score -= 15

    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance_prompt1(tasks):
    """Sorts a list of tasks by their calculated priority score, highest first.

    Uses calculate_task_score() to score each task, then returns a new list
    ordered from most to least important. The original list is not modified.

    Args:
        tasks (list[Task]): A list of Task objects to sort. Can be empty.

    Returns:
        list[Task]: A new list of Task objects sorted in descending order of
            priority score. If two tasks have the same score, their relative
            order is not guaranteed.

    Example:
        >>> sorted_tasks = sort_tasks_by_importance(my_tasks)
        >>> for task in sorted_tasks:
        ...     print(task.title)
        # Prints tasks from most to least urgent
    """
    task_scores = [(calculate_task_score(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks


def get_top_priority_tasks_prompt1(tasks, limit=5):
    """Returns the top N highest-priority tasks from a list.

    Sorts all tasks by priority score and returns only the top N results.
    Useful for dashboards or notifications where only the most urgent tasks
    should be shown.

    Args:
        tasks (list[Task]): A list of Task objects to evaluate.
        limit (int, optional): The maximum number of tasks to return.
            Defaults to 5. If the list has fewer tasks than limit, all
            tasks are returned.

    Returns:
        list[Task]: A list of up to `limit` Task objects, sorted from
            highest to lowest priority score.

    Example:
        >>> top_tasks = get_top_priority_tasks(all_tasks, limit=3)
        >>> print(len(top_tasks))
        3
    """
    sorted_tasks = sort_tasks_by_importance(tasks)
    return sorted_tasks[:limit]

#================================================================================
#Section 3: Promt 2 - Intent & Logic Explanation
#
# Promt used: 
#
#   "I need help documenting the intent and logic behind this code. Please:
#    1. Explain what this code is trying to accomplish at a high level
#    2. Break down the logic step-by-step
#    3. Identify any assumptions or edge cases in the implementation
#    4. Suggest inline comments for complex parts
#    5. Note any potential improvements while maintaining original functionality"
# ============================================================

## --- HIGH-LEVEL INTENT ---
#
# This algorithm answers the question: "What should I work on right now?"
#
# Instead of just sorting tasks alphabetically or by creation date, it
# combines FIVE real-world factors into one score so that the most
# actionable task always floats to the top:
#   1. How important is it?       (priority weight)
#   2. How soon is it due?        (due date urgency)
#   3. Is it already handled?     (status penalty)
#   4. Is it flagged as critical? (tag boost)
#   5. Was it just updated?       (recency boost)
#
# The three functions work as a pipeline:
#   calculate_task_score()       → scores one task
#   sort_tasks_by_importance()   → scores all tasks and sorts them
#   get_top_priority_tasks()     → returns just the top N from the sorted list
#
# --- STEP-BY-STEP LOGIC: calculate_task_score ---
#
# Step 1: PRIORITY BASE SCORE
#   Maps each priority level to a weight and multiplies by 10.
#   LOW=10, MEDIUM=20, HIGH=40, URGENT=60
#   Multiplying by 10 gives room for other factors to influence the score
#   without overwhelming the base priority.
#
# Step 2: DUE DATE URGENCY BONUS
#   Only runs if a due_date is set. Calculates integer days until due.
#   Overdue = +35 (biggest bonus — this needs attention NOW)
#   Due today = +20
#   Due in 1-2 days = +15
#   Due in 3-7 days = +10
#   No due date = no bonus (task treated as not time-sensitive)
#
# Step 3: STATUS PENALTY
#   DONE tasks get -50 (essentially removes them from active consideration)
#   REVIEW tasks get -15 (deprioritised — someone else is handling them)
#   This ensures finished/handed-off work doesn't clutter the top of the list.
#
# Step 4: CRITICAL TAG BOOST
#   If any tag matches "blocker", "critical", or "urgent" → +8
#   Uses any() with a membership check — efficient and readable.
#   Only ONE boost is given regardless of how many critical tags exist.
#
# Step 5: RECENCY BOOST
#   If the task was updated less than 1 full day ago → +5
#   Rewards tasks that are actively being worked on.
#
# --- ASSUMPTIONS & EDGE CASES ---
#
# 1. Tag matching is case-sensitive: "Blocker" ≠ "blocker"
#    A task tagged "Blocker" (capital B) gets NO boost — likely unintentional.
#
# 2. days_until_due uses integer days, not hours:
#    A task due in 23 hours shows days_until_due=0 (due today → +20 bonus).
#    A task due in 25 hours shows days_until_due=1 (due in 2 days → +15 bonus).
#    This cliff-edge behaviour could cause unexpected score jumps overnight.
#
# 3. No due_date = no urgency score:
#    Tasks without a deadline are treated as non-urgent regardless of priority.
#    An URGENT task with no due date scores only 60 — lower than a LOW task
#    that is overdue (10 + 35 = 45... actually urgent still wins here, but
#    edge cases exist at MEDIUM priority: 20 vs 45).
#
# 4. Multiple critical tags don't stack:
#    A task tagged ["blocker", "critical"] still only gets +8, not +16.
#
# 5. DONE tasks can still score positively if overdue + urgent:
#    60 (URGENT) + 35 (overdue) - 50 (DONE) = 45. A "done" task could
#    still appear in the top 5 if it was urgent and overdue. This may
#    be unintended behaviour.
#
# --- POTENTIAL IMPROVEMENTS ---
#
# 1. Case-insensitive tag matching:
#    Change to: tag.lower() in ["blocker", "critical", "urgent"]
#
# 2. Use hours instead of days for due date:
#    hours_until_due = (task.due_date - datetime.now()).total_seconds() / 3600
#    Gives smoother, more accurate urgency scoring.
#
# 3. Hard-zero DONE tasks:
#    Return 0 immediately if task.status == TaskStatus.DONE to prevent
#    completed tasks from appearing in priority lists.
#
# 4. Make weights configurable:
#    Accept a config dict parameter so the scoring can be tuned without
#    changing the source code.

def calculate_task_score_prompt2(task):
    # Maps priority levels to base weights; multiplied by 10 to leave
    # room for other factors to adjust the score meaningfully
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Start with the base score: priority is the most fundamental factor
    score = priority_weights.get(task.priority, 0) * 10

    # Only apply date urgency if a deadline exists — no due date = no time pressure
    if task.due_date:
        # Integer days difference: note this rounds DOWN (23hrs = 0 days)
        days_until_due = (task.due_date - datetime.now()).days

        # Tiered urgency bonuses — overdue gets the highest boost
        if days_until_due < 0:      # Already past the deadline
            score += 35
        elif days_until_due == 0:   # Must be done today
            score += 20
        elif days_until_due <= 2:   # Very soon — next 2 days
            score += 15
        elif days_until_due <= 7:   # Coming up — within the week
            score += 10
        # Beyond 7 days: no urgency bonus applied

    # Penalise tasks that don't need active attention
    if task.status == TaskStatus.DONE:
        score -= 50     # Large penalty — completed tasks should sink to bottom
    elif task.status == TaskStatus.REVIEW:
        score -= 15     # Smaller penalty — being reviewed, not fully done

    # One-time boost if ANY tag signals this is blocking or critical
    # Note: case-sensitive — "Blocker" will NOT match "blocker"
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Recency boost: reward tasks that are actively being worked on today
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:   # Updated within the last calendar day
        score += 5

    return score


# ============================================================
# SECTION 4: FINAL COMBINED DOCUMENTATION
#
# Merges the best elements from both prompts:
#   - Full Google-style docstrings from Prompt 1
#   - Inline comments and edge case awareness from Prompt 2
#   - Improvement suggestions added as Notes/TODO in docstrings
# ============================================================

def calculate_task_score_final(task):
    """Calculates a numeric priority score for a task based on multiple factors.

    Combines five real-world factors into a single integer score: the task's
    base priority level, how soon it is due, its current status, whether it
    carries critical tags, and how recently it was updated. A higher score
    means the task should be actioned sooner.

    The function answers the question: "What should I work on right now?"

    Args:
        task (Task): A Task object with the following attributes:
            - priority (TaskPriority): Enum — LOW, MEDIUM, HIGH, or URGENT.
            - due_date (datetime | None): The deadline, or None if not set.
            - status (TaskStatus): Enum — TODO, IN_PROGRESS, REVIEW, or DONE.
            - tags (list[str]): Tag strings attached to the task.
            - updated_at (datetime): Timestamp of the last update.

    Returns:
        int: A numeric urgency score. Higher = more important.

             Factor contributions:
             ┌─────────────────────────────┬────────┐
             │ Factor                      │ Points │
             ├─────────────────────────────┼────────┤
             │ Priority LOW                │ +10    │
             │ Priority MEDIUM             │ +20    │
             │ Priority HIGH               │ +40    │
             │ Priority URGENT             │ +60    │
             │ Overdue (past due date)     │ +35    │
             │ Due today                   │ +20    │
             │ Due in 1–2 days             │ +15    │
             │ Due in 3–7 days             │ +10    │
             │ Status DONE                 │ -50    │
             │ Status REVIEW               │ -15    │
             │ Has blocker/critical tag    │ +8     │
             │ Updated today               │ +5     │
             └─────────────────────────────┴────────┘

    Raises:
        AttributeError: If the task is missing any required attribute.
        TypeError: If task.due_date is not a datetime object.

    Example:
        >>> task = Task("Fix login bug", priority=TaskPriority.HIGH)
        >>> task.due_date = datetime.now() + timedelta(days=1)
        >>> task.tags = ["blocker"]
        >>> calculate_task_score(task)
        68   # HIGH(40) + due tomorrow(15) + blocker tag(8) + updated today(5)

    Notes:
        - Tasks with no due_date receive no date bonus.
        - DONE tasks almost always sink to the bottom due to the -50 penalty.
        - Tag matching is CASE-SENSITIVE: "Blocker" will not trigger the boost.
        - Multiple critical tags do not stack — only one +8 boost is applied.
        - "Updated today" uses integer day difference, so a task updated
          23 hours ago still qualifies (days_since_update = 0).

    TODO:
        - Make tag matching case-insensitive (tag.lower() in [...]).
        - Use total_seconds()/3600 for hours-based due date scoring.
        - Return 0 immediately for DONE tasks to prevent them appearing
          in active priority lists.
        - Accept a configurable weights dict parameter for flexibility.
    """
    # Maps priority levels to weights; x10 gives other factors room to matter
    priority_weights = {
        TaskPriority.LOW: 1,
        TaskPriority.MEDIUM: 2,
        TaskPriority.HIGH: 4,
        TaskPriority.URGENT: 6
    }

    # Base score — the most fundamental measure of importance
    score = priority_weights.get(task.priority, 0) * 10

    # Urgency bonus — only applied when a deadline exists
    if task.due_date:
        # Integer days: note 23hrs remaining still counts as 0 (due today)
        days_until_due = (task.due_date - datetime.now()).days

        if days_until_due < 0:      # Past the deadline — highest urgency
            score += 35
        elif days_until_due == 0:   # Due today
            score += 20
        elif days_until_due <= 2:   # Due very soon
            score += 15
        elif days_until_due <= 7:   # Due this week
            score += 10

    # Status penalties — deprioritise tasks that don't need action
    if task.status == TaskStatus.DONE:
        score -= 50     # Completed tasks sink to the bottom
    elif task.status == TaskStatus.REVIEW:
        score -= 15     # Under review — someone else is handling it

    # Critical tag boost — one-time +8 regardless of how many critical tags
    # WARNING: case-sensitive — "Blocker" will NOT match
    if any(tag in ["blocker", "critical", "urgent"] for tag in task.tags):
        score += 8

    # Recency boost — reward actively worked-on tasks
    days_since_update = (datetime.now() - task.updated_at).days
    if days_since_update < 1:
        score += 5

    return score


def sort_tasks_by_importance_final(tasks):
    """Sorts a list of tasks by priority score, highest first.

    Scores every task using calculate_task_score(), then returns a new list
    in descending order of urgency. The original list is not modified.

    Args:
        tasks (list[Task]): Tasks to sort. An empty list returns [].

    Returns:
        list[Task]: New list sorted from most to least urgent.

    Notes:
        - Scores are computed once per task and cached in a tuple list,
          avoiding redundant recalculation during sorting.
        - Equal-scored tasks retain an unspecified relative order.
    """
    # Score each task once, pair as (score, task), then sort descending
    task_scores = [(calculate_task_score_final(task), task) for task in tasks]
    sorted_tasks = [task for _, task in sorted(task_scores, reverse=True)]
    return sorted_tasks


def get_top_priority_tasks_final(tasks, limit=5):
    """Returns the top N highest-priority tasks from a list.

    Sorts all tasks by priority score and slices the top N results.
    Designed for dashboards and notifications where only the most
    urgent tasks should be surfaced.

    Args:
        tasks (list[Task]): Tasks to evaluate. Can be empty.
        limit (int, optional): Max tasks to return. Defaults to 5.
            If len(tasks) < limit, all tasks are returned.

    Returns:
        list[Task]: Up to `limit` tasks, sorted highest priority first.

    Example:
        >>> top3 = get_top_priority_tasks(all_tasks, limit=3)
        >>> [t.title for t in top3]
        ['Fix login bug', 'Deploy hotfix', 'Update SSL cert']
    """
    sorted_tasks = sort_tasks_by_importance_final(tasks)
    return sorted_tasks[:limit]  # slice safely handles limit > len(tasks)

#=======================================================================================
#What I Learned (My takeaway)
#======================================================================================
#1.Which parts of the documentation were most challenging for the AI
#-The AI struggled most with explaining the reasoning behind the scoring system,
#identifying hidden assumptions , and detecting edge cases like case-sensitive tags 
#and date-calculation issues. It could describe the code itself more easily than the logic 
#and design decisions behind it.
#
#2.What additional information you needed to provide in your prompts
#-I had to give detailed instructions about the type of documentation required, such as 
#google-style docstrings, examples,edge cases,exceptions, step-by-step logic explanations, and 
#improvement suggestions.More specific prompts produced much better results.
#
#3.How you would use this approach in your own projects
#-I would use a two step-step AI documentation process:
#First generate technical documentation and docstrings.
#Second explain the logic, assumptions and improvements

