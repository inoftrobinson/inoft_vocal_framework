try:
    from serverlesspack.cli import package_api
    package_api(target_os='linux', config_filepath='serverlesspack.config.yaml', verbose=False)
except ModuleNotFoundError as e:
    print("serverlesspack library not found. Install it by following the instructions at : https://github.com/Robinson04/serverlesspack")
