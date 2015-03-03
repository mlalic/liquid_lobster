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
import sys
import os


def main():
    """
    Drops the file given as a command line argument to Dropbox under the
    directory named by the ``LLOBSTER_DROP_DIR`` environment variable
    within the ``LiquidLobster`` app's folder on Dropbox.

    The token which is used to authenticate with Dropbox should be found
    in the environment variable ``LLOBSTER_TOKEN``
    """
    file_to_deploy = sys.argv[1:]
    if not file_to_deploy:
        print 'You need to provide some files that should be deployed.'
        return
    file_name = file_to_deploy[0]

    # Read the config from environment variables
    if 'LLOBSTER_TOKEN' not in os.environ:
        print 'Missing the LLOBSTER_TOKEN environment variable'
        return
    token = os.environ['LLOBSTER_TOKEN']
    # If there is no directory, we assume the user wants the files to be
    # uploaded to the root of the LiquidLobster app directory.
    directory = os.environ.get('LLOBSTER_DROP_DIR', '')

    client = dropbox.client.DropboxClient(token)

    print 'Uploading ``' + file_name + '`` ...'
    with open(file_name, 'rb') as f:
        client.put_file(os.path.join(directory, file_name), f)


if __name__ == '__main__':
    main()
