from setuptools import setup

setup(
    name="task_helper",
    version="0.0.1",
    entry_points={"console_scripts": ["task_helper=task_helper.main:main"]},
)
