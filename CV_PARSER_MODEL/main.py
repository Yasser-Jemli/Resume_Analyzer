#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : main.py
# @Software: Vscode
# @Description: This module provides a command-line interface for the Resume Analyzer.
# @License : MIT License


# main.py

import argparse

# /**
#  * @author Firstname Lastname
#  * @version 1.0
#  * @since 2025-05-02
#  */

# **** Local Imports ****
from utilis.watchdog import Watchdog

# from parser.cv_parser import parse_cv
# from recommender.course_recommender import recommend_courses
# from analyzer.job_matcher import match_job

# *
HELP_TEXT = """
Resume Analyzer CLI

Usage:
    python main.py <action> --path <file_path> [--timeout <seconds>]

Actions:
    parse_cv     Parse the resume/CV and extract data
    recommend    Recommend courses based on the resume
    match        Match resume to job offers

Examples:
    python main.py parse_cv --path resume.pdf
    python main.py recommend --path resume.pdf --timeout 15
"""

def main():
    parser = argparse.ArgumentParser(description="Resume Analyzer CLI", add_help=False)
    parser.add_argument("action", nargs="?", choices=["parse_cv", "recommend", "match"], help="Action to perform")
    parser.add_argument("--path", help="Path to CV or job file")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds for the process")
    parser.add_argument("-h", "--help", action="store_true", help="Show help menu")

    args = parser.parse_args()

    if args.help or not args.action or not args.path:
        print(HELP_TEXT)
        return

    actions = {
        "parse_cv": parse_cv,
        "recommend": recommend_courses,
        "match": match_job
    }

    task_function = actions.get(args.action)
    watchdog = Watchdog(target=task_function, args=(args.path,), timeout=args.timeout)
    result = watchdog.start()
    print(result)

if __name__ == "__main__":
    main()
