from dataclasses import dataclass, field


@dataclass
class ProjectMemberAverageRating:
    hard_skills: float = field(init=False)
    soft_skills: float = field(init=False)
    performance: float = field(init=False)
    activity: float = field(init=False)
    overall: float = field(init=False)

    def __init__(self, hard_skills, soft_skills, performance, activity):
        self.hard_skills = round(float(hard_skills), 2)
        self.soft_skills = round(float(soft_skills), 2)
        self.performance = round(float(performance), 2)
        self.activity = round(float(activity), 2)
        self.overall = round(float((hard_skills + soft_skills + performance + activity)) / 4, 2)
