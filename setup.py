"""Setup configuration for India Politics Agent Pro."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements-new.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="india-politics-agent-pro",
    version="2.0.0",
    description="Production-grade AI agent for Indian political analysis and YouTube content generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="India Politics Agent Team",
    author_email="team@indiaagent.ai",
    url="https://github.com/yourusername/india_politics_agent_pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "pre-commit>=3.6.0",
        ],
        "redis": [
            "redis>=5.0.0",
            "hiredis>=2.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "india-agent=india_politics_agent.cli.main:app",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="politics ai agent gemini youtube content india",
)
