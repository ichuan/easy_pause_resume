#!/bin/bash

echo -e 'y\n' | pip uninstall easy_pause_resume
rm -f dist/*
python setup.py sdist
pip install dist/*.gz

# upload
# python setup.py sdist bdist_wininst upload
