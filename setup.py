from setuptools import setup, find_packages

# Read content from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='Urkal',
    version='0.1.0',
    author='Alex Bard',
    author_email='nycbard@gmail.com',
    description='A brief description of the project',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/BardsWork/urkal',
    packages=find_packages(),
    install_requires=requirements,  # Use the list read from requirements.txt
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'your_script=yourpackage.module:main_function',
        ],
    },
)
