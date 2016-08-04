import argparse
import tempfile
import os
import warnings

def get_arguments():
    parser = argparse.ArgumentParser(description='\'TagFind\' script '
                                                 'used find specific tag information '
                                                 'within the GitHub repository.')

    parser.add_argument('-o',
                        '--output',
                        help='Provide output directory for storing zip archives.'
                             '\nDefault: Temp OS directory',
                        required=False,
                        default=tempfile.gettempdir())

    required_named = parser.add_argument_group('required arguments')

    required_named.add_argument('-r',
                        '--repo',
                        help = 'Enter GitHub repository URL',
                        required = True)

    required_named.add_argument('-d',
                                '--domain',
                                help = 'Enter GitHub custom domain',
                                required = False,
                                default='github.com')

    arguments = parser.parse_args()

    if not os.path.isdir(arguments.output):
        warnings.warn('Directory does not exists. Using OS Temp for now.')
        arguments.output = tempfile.gettempdir()

    return arguments.output, arguments.repo, arguments.domain


def main():
    pass

if __name__ == '__main__':
    main()