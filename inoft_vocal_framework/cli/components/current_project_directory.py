def prompt():
    # Local imports, to make sure we do not import unnecessary stuff, unless the prompt function is called.
    import os
    import click
    from pathlib import Path
    import inoft_vocal_engine
    from inoft_vocal_engine.inoft_vocal_framework.cli import CliCache

    def prompt_user_to_select_folderpath():
        return click.prompt(text="What is the root folder path of your project ? "
                                 "This is the default if you do not write anything :",
                            default=str(Path(os.path.dirname(os.path.realpath(inoft_vocal_engine.__file__))).parent))

    changed_root_folderpath = False
    app_project_root_folderpath = CliCache.cache().get("lastAppProjectRootFolderpath").to_str(default=None)

    if app_project_root_folderpath is None:
        app_project_root_folderpath = prompt_user_to_select_folderpath()
        changed_root_folderpath = True
    else:
        if not click.confirm(f"Do you want to deploy the project that is present in the following folder : {app_project_root_folderpath}"):
            app_project_root_folderpath = prompt_user_to_select_folderpath()
            changed_root_folderpath = True

    while not os.path.exists(app_project_root_folderpath):
        if click.confirm(text="The root folder path of the project has not been found."
                              "Do you want to select a new folderpath ? Otherwise the CLI will close."):
            app_project_root_folderpath = prompt_user_to_select_folderpath()
            changed_root_folderpath = True
        else:
            exit(200)

    if changed_root_folderpath is True:
        CliCache.cache().put("lastAppProjectRootFolderpath", app_project_root_folderpath)
        CliCache.save_cache_to_yaml()
        click.echo(f"Saved the folderpath of your project for {click.style(text='faster load next time', fg='blue')}")

    return app_project_root_folderpath
