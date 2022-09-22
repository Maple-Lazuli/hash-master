# !/usr/bin/python

import os
import random
import string

if __name__ == "__main__":

    root_dir = "/home/maple/temp"

    for _ in range(random.randint(1, 10)):
        random_str = "".join([random.choice(string.ascii_letters) for l in range(random.randint(1, 15))])
        os.makedirs(root_dir + "/" + random_str)

    dirs = set()
    for _ in range(2):
        for root, ds, _ in os.walk(root_dir):
            for d in ds:
                dirs.add(os.path.join(root, d))

        for d in dirs:
            for _ in range(random.randint(0, 10)):
                random_str = "".join([random.choice(string.ascii_letters) for _ in range(random.randint(5, 15))])
                os.makedirs(d + "/" + random_str)

    for root, ds, _ in os.walk(root_dir):
        for d in ds:
            dirs.add(os.path.join(root, d))

    for d in dirs:
        for _ in range(random.randint(0, 10)):
            file_name = "".join([random.choice(string.ascii_letters) for _ in range(random.randint(5, 15))]) + ".txt"
            with open(d + "/" + file_name, "w") as file_out:
                for _ in range(random.randint(0, 10)):
                    file_out.write(
                        "".join([random.choice(string.ascii_letters) for _ in range(random.randint(0, 50))]) + "\n")

    num_files = 0
    num_dirs = 0
    for root, dirs, files in os.walk(root_dir):
        for f in files:
            num_files += 1
        for d in dirs:
            num_dirs += 1

    print(str(num_dirs) + " Directories were created")
    print(str(num_files) + " Files were created")

