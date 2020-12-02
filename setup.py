from setuptools import setup, find_packages

"""
"inoft_vocal_framework.platforms_handlers.simulator",
"inoft_vocal_framework.platforms_handlers.simulator.request_samples",
"inoft_vocal_framework.platforms_handlers.simulator.request_samples.alexa",
"inoft_vocal_framework.platforms_handlers.simulator.request_samples.google",
"inoft_vocal_framework.platforms_handlers.simulator.request_samples.bixby"]
"""

# todo: fix the issue where when using the find_packages function, for some reasons the manifest
#  is not correctly used, and the yaml and json file of the request templates are not included.

setup(
    name="inoftvocal",
    version="0.90.5.7",
    packages=find_packages(),
    include_package_data=True,
    package_data={'inoftvocal': ['*.json', '*.yaml']},
    install_requires=["PyYAML", "pydantic", "boto3", "click", "inflect", "discord.py"],
    entry_points={
        "console_scripts": [
            "inoft = inoft_vocal_framework.cli.cli_index:cli",
            "inoftvocal = inoft_vocal_framework.cli.cli_index:cli",
        ],
    },
    url="https://github.com/Robinson04/inoft_vocal_framework",
    license="MIT",
    author="Inoft",
    author_email="robinson@inoft.com",
    description="Create advanced cross-platform skills for Alexa, Google Assistant and Samsung Bixby",
)

