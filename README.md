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
