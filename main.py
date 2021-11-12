from os import listdir
from os.path import isfile, join

import filecmp

folder_path = ""
questions_folder_name = ""
solutions_folder_name = ""

questions_path = join(folder_path, questions_folder_name)
solutions_path = join(folder_path, solutions_folder_name)

questions = [f for f in listdir(questions_path)
             if isfile(join(questions_path, f))]

for question in questions:

    is_same = filecmp.cmp(join(questions_path, question),
                          join(solutions_path, question))

    if is_same:
        print(f"{question} ✅")
    else:
        print(f"{question} ❌")
