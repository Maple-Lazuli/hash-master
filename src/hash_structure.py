# !/usr/bin/python

import datetime
import hashlib
import json
import os

results = {
    "root_dir": "/home/maple/temp",
    "time_stamp": str(datetime.datetime.now()),
    "files_processed": []
}

for root, dirs, files in os.walk("/home/maple/temp", topdown=True):
    for f in files:
        f_result = dict()
        f_result['name'] = f.split("/")[-1]
        f_result['full_name'] = os.path.abspath(os.path.join(root, f))
        f_result['md5'] = ""
        f_result['sha512'] = ""
        f_result['sha384'] = ""
        f_result['sha256'] = ""
        f_result['error_msg'] = "None"
        f_result['error_type'] = "None"

        try:
            with open(f_result['full_name'], "rb") as file_in:
                contents = file_in.read()
                f_result['md5'] = hashlib.md5(contents).hexdigest()
                f_result['sha512'] = hashlib.sha512(contents).hexdigest()
                f_result['sha384'] = hashlib.sha384(contents).hexdigest()
                f_result['sha256'] = hashlib.sha256(contents).hexdigest()
            f_result['processed'] = True
        except Exception as e:
            f_result['processed'] = False
            f_result['error_msg'] = e.message
            f_result['error_type'] = e.__class__.__name__

        results["files_processed"].append(f_result)

with open("results.json", "w") as file_out:
    file_out.write(json.dumps(results))
