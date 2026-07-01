# CS 면접 스터디

취업 준비용 CS 면접 스터디 repo. 6주 커리큘럼, 주당 3일.

## 진행 방식

1. 운영자가 학습 자료 PDF를 Google NotebookLM에 올려 노트북을 구축한다.
2. NotebookLM에서 해당 주제 면접 예상 질문을 생성한다.
3. 운영자가 **Issue → `면접 질문 등록` 폼**으로 질문을 붙여넣는다.
4. GitHub Action이 `weeks/<주차>/<일자>/questions.md`를 자동 생성한다.
5. 멤버는 각자 `answers/<github-id>.md`를 작성해 PR을 올리고 서로 리뷰한다.

## 구조

- `curriculum/schedule.yml`: 6주 커리큘럼 정의
- `weeks/`: 주차/일자별 질문과 답안
- `templates/`: 질문/답안 템플릿

자세한 설계는 `docs/superpowers/specs/` 를 참고한다.

## 답안 제출 방법

1. `answer/<주차>/<일자>/<github-id>` 브랜치를 만든다.
2. `weeks/<주차>/<일자>/answers/<github-id>.md` 를 `templates/answer-template.md` 양식으로 작성한다.
3. PR을 올리고 다른 멤버의 리뷰(최소 1명)를 받는다.
4. 승인 후 merge.

`main` 브랜치는 보호되어 직접 push할 수 없다. (질문 자동 생성 Action만 bot 우회 권한으로 push.)

## 운영자 가이드 (NotebookLM)

1. 주제 PDF를 NotebookLM 노트북에 소스로 추가한다.
2. NotebookLM에서 "면접 예상 질문"을 생성한다.
3. repo에서 New issue → `면접 질문 등록` 폼으로 주차/일자 선택 후 질문을 붙여넣는다.
4. Action이 `questions.md`를 생성하고 Issue를 닫는다.
