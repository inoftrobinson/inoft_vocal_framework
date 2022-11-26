import os

try:
    from serverlesspack import package_api
    config_filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'serverlesspack.config.yaml')
    package_api(target_os='linux', config_filepath=config_filepath, verbose=False)
except ModuleNotFoundError as e:
    print("serverlesspack library not found. Install it by following the instructions at : https://github.com/Robinson04/serverlesspack")
