import os

import click

from inoft_vocal_framework.cli.cli_cache import CliCache
from inoft_vocal_framework.databases.dynamodb.dynamodb import DynamoDbMessagesAdapter
from inoft_vocal_framework.speechs.ssml_builder_core import SpeechsList

""""
@click.command()
@click.argument("push")
def hello(push):
    click.echo("Hello, %s!" % push)

@click.command()
@click.argument('src', nargs=-1)
@click.argument('dst', nargs=1)
def copy(src, dst):
    for fn in src:
        click.echo('move %s to folder %s' % (fn, dst))
"""

@click.group()
def cli():
    pass

@cli.command("new")
def new():
    from inoft_vocal_framework.cli import new as new_module
    new_module.new()

@cli.group()
def codegen():
    pass

@cli.group()
def messages():
    pass

@messages.command()
@click.option('--file', prompt="Filepath of file containing the message to push", type=str,
              default=CliCache.cache().get("lastMessagesFilepath").to_str())
def push(file):
    CliCache.cache().put("lastMessagesFilepath", file)
    nice_quit()

    click.echo('Pushing the messages')
    if os.path.exists(file):
        import importlib
        import importlib.util
        spec = importlib.util.spec_from_file_location("messages", file)
        messages_module_file = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(messages_module_file)

        messages_db = DynamoDbMessagesAdapter(is_admin_mode=True, table_name="test_messages", region_name="eu-west-3")

        messages_file_vars_dict = vars(messages_module_file)
        for var_key, var_object in messages_file_vars_dict.items():
            if isinstance(var_object, SpeechsList):
                messages_db.post_new_speechs_list(speechs_list=var_object)
                click.echo(f"Posted speech category : {var_key}")
    else:
        if click.confirm("File did not exist, do you want to select a new one ?"):
            filepath = click.prompt("Filepath of the file")
            push(file=filepath)

    nice_quit()

def nice_quit():
    CliCache.save_cache_to_yaml()


if __name__ == '__main__':
    pass

