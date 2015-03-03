"""
Quick-and-dirty script to suport a CodeShip "deployment" by uploading build
artifacts to Dropbox.

The artifacts, given as CLI parameters to the script, will be uploaded under
the app's Dropbox folder.  Additionally, if the ``LLOBSTER_DROP_DIR``
environment variable is defined, the artifacts will be put into the
corresponding subdirectory.

The script depends on the user already having authorized LiquidLobster to
access their Dropbox and having placed the generated authorization token
into the ``LLOBSTER_TOKEN`` environment variable.
"""
import dropbox
import click
import sys
import os


@click.command()
@click.argument('file_name', type=click.Path(exists=True))
@click.option('--destname',
              help='The name the file will have in the Dropbox directory',
              default='')
def drop(file_name, destname):
    """
    Drops the file given as a command line argument to Dropbox under the
    directory named by the ``LLOBSTER_DROP_DIR`` environment variable
    within the ``LiquidLobster`` app's folder on Dropbox.

    The token which is used to authenticate with Dropbox should be found
    in the environment variable ``LLOBSTER_TOKEN``
    """
    # If the destination name is not provided, we simply use the one the
    # file has...
    if not destname:
        destname = os.path.split(file_name)[-1]
    # Read the config from environment variables
    if 'LLOBSTER_TOKEN' not in os.environ:
        click.echo('Missing the LLOBSTER_TOKEN environment variable')
        return
    token = os.environ['LLOBSTER_TOKEN']
    # If there is no directory, we assume the user wants the files to be
    # uploaded to the root of the LiquidLobster app directory.
    directory = os.environ.get('LLOBSTER_DROP_DIR', '')

    client = dropbox.client.DropboxClient(token)

    click.echo('Uploading ``' + file_name + '`` ...')
    with open(file_name, 'rb') as f:
        client.put_file(os.path.join(directory, destname), f)


if __name__ == '__main__':
    drop()
