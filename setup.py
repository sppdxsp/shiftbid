from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="shift-bid-engine",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A web application for managing shift bidding and assignments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/shift-bid-engine",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Flask>=3.0.2",
        "pandas>=2.2.0",
        "python-dotenv>=1.0.1",
        "Werkzeug>=3.0.1",
        "Flask-WTF>=1.2.1",
        "pytz>=2024.1",
    ],
    extras_require={
        "dev": [
            "pytest>=8.0.2",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "shift-bid-engine=bid_engine.web.app:main",
        ],
    },
) 