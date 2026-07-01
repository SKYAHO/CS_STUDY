from pathlib import Path


def render_questions(day_info, questions_md, template_path):
    tpl = Path(template_path).read_text(encoding="utf-8")
    return (
        tpl.replace("{{TOPIC}}", str(day_info["topic"]))
        .replace("{{SUBTOPIC}}", str(day_info["subtopic"]))
        .replace("{{WEEK_ID}}", str(day_info["week_id"]))
        .replace("{{DAY_ID}}", str(day_info["day_id"]))
        .replace("{{QUESTIONS}}", questions_md)
    )
