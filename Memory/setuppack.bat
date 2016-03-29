@echo off
rd /s/q dist
rd /s/q build
python setuppack.py py2exe
pause