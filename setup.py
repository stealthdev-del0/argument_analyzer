from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="argument-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Analyze argumentative structures in any text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/argument_analyzer",
    py_modules=[
        "preprocessing",
        "claim_detection",
        "emotion_analysis",
        "argument_classification",
        "structure_builder",
        "visualizer",
        "main",
        "app",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=[
        "nltk>=3.8.1",
        "networkx>=3.1",
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "streamlit>=1.28.0",
        "scikit-learn>=1.3.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)
