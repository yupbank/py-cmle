import argparse
import subprocess
import logging
import tempfile
import os
import sys


def execute_command(command):
    if not command:
        raise ValueError('command is empty')
    logging.info('Running command: %s', ' '.join(command))
    subprocess.check_call(command)


def download_package(uri):
    file_name = os.path.split(uri)[-1]
    download_command = ['gsutil', '-q', 'cp', uri, file_name]
    logging.info('Downloading the file: %s', uri)
    execute_command(download_command)
    return file_name


def install_package(local_uri):
    install_command = [
        'pip', 'install', '--user', '--upgrade', '--force-reinstall',
        '--no-deps', local_uri
    ]
    logging.info('Installing package:{}'.format(local_uri))
    execute_command(install_command)


def exectue_module(module_name, args):
    module_command = [
        'python', '-m', module_name]
    module_command.extend(args)
    logging.info('Running py_module:{}'.format(module_name))
    execute_command(module_command)


def main():
    import logging
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(
        'Python based Cloud Machine Learning Engine - boot service')
    parser.add_argument('--package_uris', type=str, default='',
                        help='Package uris in gcs, seperated by semicomma')
    parser.add_argument('--module_name', type=str, help='entry moudule names')
    args, unknown = parser.parse_known_args()
    with tempfile.TemporaryDirectory() as directory:
        logging.info('Set working dir: %s', directory)
        os.chdir(directory)
        package_uris = filter(None, args.package_uris.split(','))
        for package_uri in package_uris:
            local_uri = download_package(package_uri)
            install_package(local_uri)

        if args.module_name:
            exectue_module(args.module_name, unknown)
        else:
            logging.info('There is nothing here, please ask for --help')


if __name__ == "__main__":
    main()
