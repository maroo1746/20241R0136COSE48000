CREATE TABLE IF NOT EXISTS course (
    id SERIAL PRIMARY KEY,
    timestamp timestamp,
    user_id integer,
    course_name varchar(255),
    content text,
    summary text,
);

CREATE TABLE IF NOT EXISTS quiz (
    id SERIAL PRIMARY KEY,
    timestamp timestamp,
    course_id integer,
    question text,
);

CREATE TABLE IF NOT EXISTS user_answer (
    id SERIAL PRIMARY KEY,
    timestamp timestamp,
    quiz_id integer,
    answer text,
    attempt integer,
);

CREATE TABLE IF NOT EXISTS editing (
    id SERIAL PRIMARY KEY,
    timestamp timestamp,
    answer_id integer,
);

-- insert some test data
INSERT INTO course (timestamp, user_id, course_name, content, summary) VALUES
    (NOW(), 1, 'Course 1', 'Content 1', 'Summary 1'),
    (NOW(), 1, 'Course 2', 'Content 2', 'Summary 2'),
    (NOW(), 2, 'Course 3', 'Content 3', 'Summary 3');

INSERT INTO quiz (timestamp, course_id, question) VALUES 
    (NOW(), 1, 'Question 1'),
    (NOW(), 1, 'Question 2'),
    (NOW(), 2, 'Question 3');

INSERT INTO user_answer (timestamp, quiz_id, answer, attempt) VALUES
    (NOW(), 1, 'Answer 1', 1),
    (NOW(), 1, 'Answer 2', 1),
    (NOW(), 2, 'Answer 3', 1);

INSERT INTO editing (timestamp, answer_id) VALUES
    (NOW(), 1),
    (NOW(), 2);

    