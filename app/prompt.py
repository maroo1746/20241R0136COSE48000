question_system_prompt = """Your mission is to create a quiz with %s questions according to the following contents.
Each question should have a question, type, answer, choices, and reason.
The type can be 'choice' or 'short', or 'long'.
The answer should be the correct answer to the question.
The choices should be a dictionary with the key as the choice number and the value as the choice.
The reason should be an explanation of why the answer is correct.

The contents are as follows:
"""

question_response_prompt = """Your response MUST BE in the following format:
[
  {
    "question": "다음 중 옳은 것은?",
    "type": "choice",
    "answer": 1,
    "choices": {
      "1": "컴퓨터는 2진수로 데이터를 처리한다.",
      "2": "컴퓨터는 10진수로 데이터를 처리한다.",
      "3": "컴퓨터는 8진수로 데이터를 처리한다.",
      "4": "컴퓨터는 16진수로 데이터를 처리한다."
    },
    "reason": "컴퓨터는 2진수로 데이터를 처리한다."
  },
  {
    "question": "컴퓨터의 CPU는 무엇의 약자인가?",
    "type": "short",
    "answer": "Central Processing Unit",
    "reason": "CPU는 Central Processing Unit의 약자이다."
  }
]
"""
