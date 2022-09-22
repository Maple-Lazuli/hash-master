# !/usr/bin/python

import datetime
import hashlib
import json
import os


def create_dict_template():
    return {
        "name": "",
        "full_name": "",
        "original_md5": "None",
        "original_sha512": "None",
        "original_sha384": "None",
        "original_sha256": "None",
        "original_error_msg": "None",
        "original_error_type": "None",
        "new_md5": "None",
        "new_sha512": "None",
        "new_sha384": "None",
        "new_sha256": "None",
        "processed": False,
        "error_msg": "None",
        "error_type": "None",
        "passed_md5": False,
        "passed_sha512": False,
        "passed_sha384": False,
        "passed_sha256": False,
        'passed_all': False,
        "collision_detected": False,
    }


def create_from_result(result_dict):
    rtn_dict = create_dict_template()
    rtn_dict["name"] = result_dict["name"]
    rtn_dict["full_name"] = result_dict["full_name"]
    rtn_dict["original_md5"] = result_dict["md5"]
    rtn_dict["original_sha512"] = result_dict["sha512"]
    rtn_dict["original_sha384"] = result_dict["sha384"]
    rtn_dict["original_sha256"] = result_dict["sha256"]
    rtn_dict["original_error_msg"] = result_dict["error_msg"]
    rtn_dict["original_error_type"] = result_dict["error_type"]
    return rtn_dict


def create_new_hashes(f_dict, content):
    f_dict['new_md5'] = hashlib.md5(content).hexdigest()
    f_dict['new_sha512'] = hashlib.sha512(content).hexdigest()
    f_dict['new_sha384'] = hashlib.sha384(content).hexdigest()
    f_dict['new_sha256'] = hashlib.sha256(content).hexdigest()
    return f_dict


def verify_hashes(f_dict):
    f_dict["passed_md5"] = f_dict['new_md5'] == f_dict['original_md5']
    f_dict["passed_sha512"] = f_dict['new_sha512'] == f_dict['original_sha512']
    f_dict["passed_sha384"] = f_dict['new_sha384'] == f_dict['original_sha384']
    f_dict["passed_sha256"] = f_dict['new_sha256'] == f_dict['original_sha256']
    f_dict['passed_all'] = (f_dict["passed_md5"] and f_dict["passed_sha512"] and
                            f_dict["passed_sha384"] and f_dict["passed_sha256"])
    f_dict['collision_detected'] = (not f_dict['passed_all']) and (f_dict["passed_md5"] or
                                                                   f_dict["passed_sha512"] or
                                                                   f_dict["passed_sha384"] or
                                                                   f_dict["passed_sha256"])
    return f_dict


def process_dict(f_dict):
    if os.path.exists(f_dict['full_name']):
        try:
            with open(f_dict['full_name'], "rb") as file_in:
                f_dict = create_new_hashes(f_dict, file_in.read())
            f_dict['processed'] = True
        except Exception as e:
            f_dict['processed'] = False
            f_dict['error_msg'] = e.message
            f_dict['error_type'] = e.__class__.__name__
    else:
        f_dict['processed'] = False
        f_dict['error_msg'] = "File Not Found"
        f_dict['error_type'] = "Missing"

    f_dict = verify_hashes(f_dict)
    return f_dict


if __name__ == "__main__":
    with open("results.json", "r") as results_in:
        structure = json.loads(results_in.read())

    results = {
        "time_stamp": str(datetime.datetime.now()),
        "files_processed": []}

    for f in structure['files_processed']:
        f_result = create_from_result(f)
        results["files_processed"].append(process_dict(f_result))

    walked_files = []
    for root, dirs, files in os.walk(structure['root_dir'], topdown=True):
        for f in files:
            walked_files.append(os.path.abspath(os.path.join(root, f)))

    new_files = set(walked_files).difference([f['full_name'] for f in results["files_processed"]])
    for f in new_files:
        f_new = create_dict_template()
        f_new['name'] = f.split("/")[-1]
        f_new['full_name'] = f
        f_new["original_error_msg"] = "FILE DID NOT EXIST DURING PREVIOUS VALIDATION"
        f_new["original_error_type"] = "NEW_FILE"
        results["files_processed"].append(process_dict(f_new))

    results_name_base = "hash_validation_" + str(datetime.date.today())
    with open(results_name_base + ".json", "w") as file_out:
        file_out.write(json.dumps(results))

    for f_dict in results['files_processed']:
        for key in f_dict.keys():
            if type(f_dict[key]) == str:
                f_dict[key] = f_dict[key].replace(",", " ")

    keys = ["name","full_name","original_md5","original_sha512","original_sha384","original_sha256",
            "original_error_msg","original_error_type","new_md5","new_sha512","new_sha384","new_sha256","processed",
            "error_msg","error_type","passed_md5","passed_sha512","passed_sha384","passed_sha256",'passed_all',
            "collision_detected",]

    with open(results_name_base + ".csv", "w") as file_out:
        file_out.write(",".join(keys) + "\n")
        for f_dict in results['files_processed']:
            file_out.write(",".join([str(f_dict[key]) for key in keys]) + "\n")
