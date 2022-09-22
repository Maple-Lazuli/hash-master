# !/usr/bin/python

import os
import random

if __name__ == "__main__":

    root_dir = "/home/maple/temp"

    file_list = []
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            file_list.append(os.path.join(root,f))

    files_to_remove = set([random.choice(file_list) for _ in range(random.randint(10, 20))])

    for f in files_to_remove:
        os.remove(f)

    files_to_mutate = set([random.choice(file_list) for _ in range(random.randint(10, 20))])

    for f in files_to_mutate:
        with open(f, "a") as file_out:
            file_out.write("-Injection!")

    print(str(len(files_to_remove)) + " files were removed")
    print(str(len(files_to_mutate)) + " files were mutated")
