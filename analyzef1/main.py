#!/usr/bin/env python3
"""
Main analyzef1 script
"""

import subprocess


def main():
    # subprocess.run(['python3', '-m', 'streamlit', 'run', 'analyzef1/Home.py'])
    subprocess.run("python -m streamlit run analyzef1/Home.py", shell=True)


if __name__ == "__main__":
    main()
