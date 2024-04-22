question_system_prompt = """Your mission is to create a quiz with %s questions according to the following contents.
Each question should have a question, type, answer, choices, and reason.
The type can be 'choice' or 'short', or 'long'.
The answer should be the correct answer to the question.
The choices should be a dictionary with the key as the choice number and the value as the choice.
The reason should be an explanation of why the answer is correct.
Your response should be Korean.

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

correction_prompt = """
The text below is extracted from a recording of a lecture on {department} given at the University of "{category}".
Considering the lecture title, and department where the lecture takes place, correct any grammatically incorrect or spelling incorrect words and reprint the text below. Also, print out the major words of the lecture as English.
For example, you should fix the sentence "시뮬러리티 쪽 진도가 약간 길어지긴 했는데 이제 멀웨어 분석과 관련된 거, " into " Simularity 쪽 진도가 약간 길어지긴 했는데 이제 malware 분석과 관련된 거".
You must output only extracted text from the lecture recording you corrected.
You should never say additional words such as "Yes, I understand." or "Sure!".
JUST OUTPUT THE FIXED TEXT.
Do not specifically mention what major words of the lecture you selected. 
"""
