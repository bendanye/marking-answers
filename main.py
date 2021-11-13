from os import listdir
from os.path import isfile, join

import filecmp

import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


def _on_modified(event):
    print(f"hey buddy, {event.src_path} has been modified")
    compare_answer(questions_path, solutions_path,
                   event.src_path.replace(questions_path + "\\", ""))


def watch_modified_answer(questions_path):
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
    questions = [f for f in listdir(questions_path)
                 if isfile(join(questions_path, f))]

    for question in questions:
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

#check_all_answers(compare_answer, questions_path, solutions_path)
watch_modified_answer(questions_path)
