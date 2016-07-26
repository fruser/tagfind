from arguments import get_arguments
from get_package import get_package
from datetime import datetime


def main():
    output, repo, domain = get_arguments()
    archive = 'https://{0}/{1}/archive/master.zip'.format(domain, repo)

    time_format = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    output = output + '/' + repo.replace('/','_') + '-' + time_format

    get_package(archive, output)


if __name__ == '__main__':
    main()