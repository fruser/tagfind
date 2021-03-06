from arguments import get_arguments
import utils
from datetime import datetime
from log_info import logger


def tag_verify(tag_list):
    filtered_list = []
    seen = set()

    for tag in tag_list:
        if tag in seen:
            utils.LOG.info('Skipping {0} tag due to duplicate record...'.format(tag))
        elif not tag.startswith('@'):
            utils.LOG.info('Skipping {0} tag due to incorrect format...'.format(tag))
        else:
            filtered_list.append(tag)
            seen.add(tag)

    return filtered_list


def main():
    output, repo, domain = get_arguments()
    archive = 'https://{0}/{1}/archive/master.zip'.format(domain, repo)

    time_format = datetime.now().strftime('%Y-%m-%d_%H.%M.%S')

    utils.LOG.info('Starting repository analysis...')

    output = output + '/' + repo.replace('/','_') + '-' + time_format
    utils.get_package(archive, output)

    feature_files = utils.get_feature_files(output)

    tag_ojb_list = utils.parse_files(feature_files)

    utils.stats_output(tag_ojb_list)

    utils.LOG.info('Finished...')


if __name__ == '__main__':
    main()