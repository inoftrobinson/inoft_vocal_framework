import os

from serverlesspack.cli import package_api

ab = os.path.relpath('../inoft_vocal_framework')
package_api(target_os='linux', config_filepath='serverlesspack.config.yaml', verbose=False)
