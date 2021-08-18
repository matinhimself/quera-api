from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class ContestModel:
    name: str
    start_date: str
    time: str
    contestants: int
    link: str


@dataclass
class Test:
    name: str
    inp: str
    otp: str


@dataclass
class Question:
    qid: str
    name: str
    link: str
    score: str = ''
    tests: List[Test] = field(default_factory=lambda: [])
    description_md: str = ""
    time_limit: str = ""
    storage_limit: str = ""

    def addTest(self, t: Test):
        self.tests.append(t)