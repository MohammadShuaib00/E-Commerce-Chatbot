from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    try:
        requirements_list = []
        with open(file_path, "r") as file:
            # Read the lines and strip each one, excluding '-e .' if present
            requirements_list = [req.strip() for req in file.readlines() if req.strip() != '-e .']
        return requirements_list
    except Exception as e:
        raise Exception(f"Error reading the requirements file: {e}")

setup(
    name="E-Commerce-AI-Chatbot",
    version="1.0",
    author="Mohammad Shuaib",
    author_email="mohammadshuaib3455@gmail.com",
    description="E-Commerce AI Chatbot",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
