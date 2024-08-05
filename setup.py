from setuptools import setup, find_packages

setup(
    name='context-check',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pydantic>=2.7.1',
        'pyyaml>=6.0.1',
        'openai>=1.30.1',
        'langchain_community>=0.2.4',
        'python-dotenv>=1.0.1',
        'pytest-dotenv>=0.5.2',
        'requests>=2.31.0',
        'jinja2>=3.1.4',
        'rich>=13.7.1',
        'loguru>=0.7.2',
        'pylint>=3.2.3',
        'black>=24.4.2',
        'isort>=5.13.2',
        'fsspec>=2024.3.1',
        'pre-commit>=3.7.1',
        'jsonschema>=4.23.0',
        'nltk>=3.8.1',
        'gensim>=4.3.3'

    ],
    python_requires='>=3.11',
    author='Volodymyr Kepsha',
    author_email='v.kepsha@addepto.com',
    description='ContextCheck package is a tool for RAG system testing and evaluation.',
    license='Apache 2.0',
    url='https://gitlab.com/addepto/contextcheck',
)