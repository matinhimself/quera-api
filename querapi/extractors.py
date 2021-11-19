import string

from .models import ContestModel, Question, Test, ClassUser, AssignmentUser, AssignmentSubmission
from .models import ContestModel, Question, ShortAssignment, Test, ClassUser, Course
from bs4 import BeautifulSoup, NavigableString
from typing import List
import re
from markdown import markdown

CodeBlock = re.compile(r"^description_md-")


def parse_question(content: str, q: Question) -> Question:
    # source: https://github.com/ParsaAlizadeh/universal-parser-tool
    expected = ("ورودی نمونه", "خروجی نمونه")
    soup = BeautifulSoup(content, 'html.parser')
    desc = soup.find(id=CodeBlock)
    if desc is None:
        return q
    md_soup = BeautifulSoup(markdown(desc.text), 'html.parser')
    sample = []
    counter: int = 0
    for elem in md_soup.find_all("code"):
        if elem.parent is None:
            continue
        if (header := elem.parent.find_previous_sibling()) and any(_ in header.text for _ in expected):
            sample.append("\n".join(elem.strings))

    for s in (it := iter(sample)):
        counter += 1
        q.addTest(
            Test(
                str(counter),
                s,
                next(it)
            )
        )
    return q


def extract_questions_metadata(content: str, url: str) -> Question:
    soup = BeautifulSoup(content, 'html.parser')
    desc = soup.find(id=CodeBlock)
    name = soup.find('div', {'class': 'ui center aligned fluid container'}).text.strip()
    time_limit = ""
    if len(tl := re.findall("محدودیت زمان: (.*)", desc.text)) >= 1:
        time_limit = tl[0].strip()

    storage_limit = ""
    if len(tl := re.findall("محدودیت حافظه: (.*)", desc.text)) >= 1:
        storage_limit = tl[0].strip()

    if len(tl := re.findall(r'/(\d+)', url)) >= 1:
        qid = tl[0]
    else:
        qid = url

    return Question(
        qid,
        name,
        url,
        description_md=desc.text,
        time_limit=time_limit,
        storage_limit=storage_limit
    )


def extract_contest_questions(content: str) -> List[Question]:
    questions: List[Question] = []

    soup = BeautifulSoup(content, 'html.parser')
    qs = list(filter(lambda s: s != '\n', soup.find(id='a-sidebar-problems').childGenerator()))
    for q in qs:
        question = Question(
            qid=q.get('data-pid'),
            name=[element for element in q if isinstance(element, NavigableString) if element != '\n'][0].strip(),
            link=q.get('href').strip(),
            score=q.find('div', {'data-content': "امتیاز"}).text.strip()
        )
        questions.append(question)

    return questions


def extract_contests(content: str) -> List[ContestModel]:
    contests: List[ContestModel] = []

    table = BeautifulSoup(content, 'html.parser').find('table', {'class': 'ui striped center aligned table'})
    rows = table.findChildren('tr')
    if len(rows) <= 1:
        return contests
    for row in rows[1:]:
        cells = row.findChildren('td')
        con = ContestModel(
            cells[0].text.strip(),
            cells[1].text.strip(),
            int(cells[2]["data-time"]),
            int(cells[3].text.strip()),
            int(cells[4].text),
            cells[5].findChild('a')['href'],
        )
        contests.append(con)

    return contests


def extract_class_users(content: str) -> List[ClassUser]:
    users: List[ClassUser] = []

    table = BeautifulSoup(content, 'html.parser').find('table', {'class': 'ui inverted celled green unstackable table'})
    rows = table.findChildren('tr')
    if len(rows) <= 1:
        return users
    for row in rows[1:-1]:
        cells = row.findChildren('td')
        s_id = cells[0].input.get("value")
        name = cells[1].text.strip()
        email = cells[2].div.text.strip()
        user = ClassUser(
            s_id,
            name,
            email
        )
        users.append(user)

    return users


def extract_assignment_submission(content: str) -> List[AssignmentSubmission]:
    assignments: List[AssignmentSubmission] = list()

    table = BeautifulSoup(content, 'html.parser').find('table', {'class': 'ui selectable unstackable center aligned small table'})
    rows = table.findChildren('tr')

    if len(rows) <= 1:
        return assignments

    for row in rows[2:-1]:
        cells = row.findChildren('td')
        s_id = cells[0].text.strip()
        name = cells[1].text.strip()
        delay_penalty = cells[4].text.strip()

        user = AssignmentUser(
            s_id,
            name
        )
        assignment = AssignmentSubmission(
            user,
            delay_penalty
        )

        assignments.append(assignment)

    return assignments

def extract_courses(content: str) -> List[Course]:
    courses: List[Course] = []
    table = BeautifulSoup(content, 'html.parser').find_all('a', {'class': 'ui small link card course-card'})
    for row in table:
        link = row['href']
        id = link.split('/')[-2]
        name = row.find('div', {'class': 'header'}).text
        course = Course(
            id = id,
            name = name,
            link = link
        )
        courses.append(course)
    return courses

def extract_short_assignments(content: str) -> List[ShortAssignment]:
    shortassignments: List[ShortAssignment] = []
    table = BeautifulSoup(content, 'html.parser').find('div', {'class': 'ui inline dropdown qu-dropdown right item'})
    for row in table.findChildren('a'):
        link = row['href']
        id = link.split('/')[-2]
        name = row.text
        shortassignment = ShortAssignment(
            id = id,
            name = name,
            link = link
        )
        shortassignments.append(shortassignment)
    return shortassignments