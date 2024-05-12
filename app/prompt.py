question_system_prompt = """We’ll help students review the class by making some quiz for them.
Based on the contents of course below, give {count} descriptive question related to important concepts. The answer to the question must be inside the course content. You must output only the quiz.
You should never say additional words such as "Yes, I understand." or “Sure!”.
JUST OUTPUT THE QUIZ. DO NOT INCLUDE PREFIXES LIKE "1. "
Your question should be in Korean.

The course contents are as follows: {content}
"""

question_response_prompt = """Your response MUST BE in the following example format:

- OSI 7계층을 쓰고, 각각의 계층에 대해 설명하시오.
- HTTP 통신에서의 멱등성에 대해 설명하고, 각 메서드별로 어떤 멱등성을 가지는지 설명하시오."
"""

correction_prompt = """
The text below is extracted from a recording of a lecture on {category} given at the University of "{department}".
Considering the lecture title, and department where the lecture takes place, correct any grammatically incorrect or spelling incorrect words and reprint the text below.
Also, convert the major words of the lecture as English.
For example, you should fix the sentence "시뮬러리티 쪽 진도가 약간 길어지긴 했는데 이제 멀웨어 분석과 관련된 거, " into " Simularity 쪽 진도가 약간 길어지긴 했는데 이제 malware 분석과 관련된 거".
You must output only extracted text from the lecture recording you corrected.
You should never say additional words such as "Yes, I understand." or "Sure!".
JUST OUTPUT THE FIXED TEXT.
"""

summary_prompt = """The text below is extracted from a recording of a lecture on "{category}" given at the University of "{department} Science". 
Please refer to the lecture title, and department where the lecture takes place, present the key contents of the text below in an structured form.
However, it should not be summarized too briefly.
Since students will be studying for exams based on your summary, it should be including all key concepts and detailed explanation for that.
Also, if there is content in the lecture that is presumed to invite students to attend, ignore that part and do not summarize it.
Remember, this is a summary of the lecture.
You must never include information in your summary from sources other than the lecture materials and lecture recordings I have presented!
And this is part of the recording of the lecture.
"""

summary_notice_prompt = """you MUST not use words like “The lecture concluded~”.
You should never say additional words such as "Yes, I understand." or “Sure!”.
YOUR OUTPUT SHOULD BE IN KOREAN AND MARKDOWN FORMAT.
The title level starts with h1, and DO NOT include numbering.
JUST OUTPUT THE SUMMARY, NOTHING ELSE.
Organize the contents of the lecture in parallel. DO NOT give the main title (such as "{category} 강의 내용") and conclusion you made.
"""

advice_prompt = """Now, we will give some feedback to the user's answer.
Based on the contents of following content, give some feedback to the answer.
You should give detail feedback by referring to what part of the class material is written and how it is written.
Please write a better answer yourself and let user know.
The answer should be in Korean.
The answer should be more than 500 characters.
You must output only the text of the feedback.
You should never say additional words such as "Yes, I understand." or “Sure!”. JUST OUTPUT THE FEEDBACK.

content:
{content}

question:
{question}"""
