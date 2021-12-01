from os import listdir
from os.path import isfile, join, sep

import filecmp

import sys

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def _on_modified(event):
    if event.src_path.endswith(".txt"):
        question = event.src_path.replace(questions_path + sep, "")
        compare_answer(questions_path, solutions_path, question)


def watch_modified_answer(questions_path):
    print("Running by watch and check answer when it changes")
    patterns = ["*"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_modified = _on_modified

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, questions_path,
                         recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()


def check_all_answers(compare_answer, questions_path, solutions_path):
    print("Running by check all answers")
    questions = [f for f in listdir(questions_path)
                 if isfile(join(questions_path, f))]

    for question in sorted(questions):
        compare_answer(questions_path, solutions_path, question)


def compare_answer(questions_path, solutions_path, question):
    is_same = filecmp.cmp(join(questions_path, question),
                          join(solutions_path, question))

    if is_same:
        print(f"{question} ✅")
    else:
        print(f"{question} ❌")


folder_path = ""
questions_folder_name = ""
solutions_folder_name = ""

questions_path = join(folder_path, questions_folder_name)
solutions_path = join(folder_path, solutions_folder_name)

if len(sys.argv) == 1:
    watch_modified_answer(questions_path)
else:
    check_all_answers(compare_answer, questions_path, solutions_path)
