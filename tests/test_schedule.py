from pathlib import Path
import schedule

SCHEDULE_YML = Path(__file__).resolve().parents[1] / "curriculum" / "schedule.yml"


def test_load_schedule_returns_dict_with_weeks():
    data = schedule.load_schedule(SCHEDULE_YML)
    assert "weeks" in data
    assert len(data["weeks"]) == 6


def test_every_week_has_three_days():
    data = schedule.load_schedule(SCHEDULE_YML)
    for w in data["weeks"]:
        assert len(w["days"]) == 3, f"{w['id']}의 day 수가 3이 아님"


def test_valid_day_true_for_known():
    data = schedule.load_schedule(SCHEDULE_YML)
    assert schedule.valid_day(data, "week-01", "day-1") is True


def test_valid_day_false_for_unknown():
    data = schedule.load_schedule(SCHEDULE_YML)
    assert schedule.valid_day(data, "week-99", "day-1") is False
    assert schedule.valid_day(data, "week-01", "day-9") is False


def test_get_day_returns_info():
    data = schedule.load_schedule(SCHEDULE_YML)
    info = schedule.get_day(data, "week-02", "day-1")
    assert info == {
        "week_id": "week-02",
        "topic": "네트워크",
        "day_id": "day-1",
        "subtopic": "TCP-IP와 OSI 7계층",
    }


def test_get_day_none_for_unknown():
    data = schedule.load_schedule(SCHEDULE_YML)
    assert schedule.get_day(data, "week-99", "day-1") is None
