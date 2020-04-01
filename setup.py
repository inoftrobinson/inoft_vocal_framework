from setuptools import setup

setup(
    name='inoftvocal',
    version='0.61.0',
    packages=['inoft_vocal_framework', 'inoft_vocal_framework.cli', 'inoft_vocal_framework.utils',
              'inoft_vocal_framework.speechs', 'inoft_vocal_framework.databases',
              'inoft_vocal_framework.databases.dynamodb', 'inoft_vocal_framework.skill_builder',
              'inoft_vocal_framework.platforms_handlers', 'inoft_vocal_framework.platforms_handlers.alexa_v1',
              'inoft_vocal_framework.platforms_handlers.alexa_v1.response',
              'inoft_vocal_framework.platforms_handlers.simulator',
              'inoft_vocal_framework.platforms_handlers.simulator.request_samples',
              'inoft_vocal_framework.platforms_handlers.dialogflow_v1',
              'inoft_vocal_framework.platforms_handlers.samsungbixby_v1',
              'inoft_vocal_framework.platforms_handlers.endpoints_providers'],
    install_requires=["PyYAML", "cerberus", "boto3", "click"],
    entry_points={
        'console_scripts': [
            'inoft = inoft_vocal_framework.cli.cli_index:cli',
            'inoftvocal = inoft_vocal_framework.cli.cli_index:cli',
        ],
    },
    url='https://github.com/Robinson04/inoft_vocal_framework',
    download_url='https://github.com/Robinson04/inoft_vocal_framework/archive/0.6.0.tar.gz',
    license='MIT',
    author='Inoft',
    author_email='robinson@inoft.com',
    description='Create advanced cross-platform skills for Alexa, Google Assistant and Samsung Bixby',
)

