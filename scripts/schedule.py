from pathlib import Path
import yaml


def load_schedule(path):
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def valid_day(schedule, week_id, day_id):
    return get_day(schedule, week_id, day_id) is not None


def get_day(schedule, week_id, day_id):
    for week in schedule.get("weeks", []):
        if week.get("id") == week_id:
            for day in week.get("days", []):
                if day.get("id") == day_id:
                    return {
                        "week_id": week_id,
                        "topic": week.get("topic"),
                        "day_id": day_id,
                        "subtopic": day.get("subtopic"),
                    }
    return None
