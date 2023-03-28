import setuptools

VERSION = "0.0.1"  # PEP-440

NAME = "streamlit_openai"

INSTALL_REQUIRES = [
    "streamlit>=1.20.0",
    "openai",
    "tenacity"
]


setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Streamlit Connection for OpenAI.",
    url="https://github.com/sfc-gh-jcarroll/st-connection-prpr",
    project_urls={
        "Source Code": "https://github.com/sfc-gh-jcarroll/st-connection-prpr",
    },
    author="Joshua Carroll",
    author_email="joshua.carroll@snowflake.com",
    license="Apache License 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.10",
    ],
    # Snowpark requires Python 3.8
    python_requires=">=3.10.*",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["streamlit_openai"]
)