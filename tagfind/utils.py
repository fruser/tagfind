from urllib import request
from zipfile import ZipFile
import os
import fnmatch
import glob
import re
import tags as tg
from log_info import logger
from operator import itemgetter

LOG = logger()


def get_package(archive, output):
    get_zip(archive, output + '.zip')
    extract_zip(output + '.zip', output)


def get_zip(archive, output):
    LOG.info('Downloading Master zip file from {0}'.format(archive))
    request.urlretrieve(archive, output)


def extract_zip(archive, output):
    LOG.info('Extracting Master zip file into {0}'.format(output))
    with ZipFile(archive, 'r') as z:
        z.extractall(output)


def get_feature_files(directory):
    feature_files = []
    rootdir = glob.glob(directory + '/*/features/')[0]

    for subdir, dirs, files in os.walk(rootdir):
        for file in fnmatch.filter(files, '*.feature'):
            location = os.path.join(subdir, file)
            filename = os.path.split(os.path.dirname(location))[1] + '/' + os.path.splitext(file)[0]
            LOG.info('Adding {0} to the list of feature files'.format(file))
            feature_files.append({'file_name': filename,
                                  'location': location})

    return feature_files


def find_tag_obj(tag_list, tag_name):
    found_tag_obj = [tag for tag in tag_list if tag.tag_name == tag_name]
    return found_tag_obj[0] if found_tag_obj else None


def parse_files(files):
    LOG.info('Started parsing process...')
    tags_list = []

    for file in files:
        feature_global_count = 0

        with open(file['location'], 'r') as FileObj:
            feature = file['file_name']
            LOG.info('Working on {0} feature file'.format(feature))

            feature_tags = []
            current_tags = []

            scenario_outline_header_flag = False

            for line in FileObj:
                line = line.strip()
                if re.match(r'#', line):
                    continue

                elif re.match(r'@', line):
                    rgx = re.compile('(@[\w]+)')
                    line_tags = rgx.findall(line)
                    line_tags = [x.lower() for x in line_tags if not re.search('[0-9]', x)]

                    for line_tag in line_tags:
                        tag_obj = find_tag_obj(feature_tags, line_tag)

                        if not tag_obj:
                            tag_obj = tg.Tags(line_tag)
                            feature_tags.append(tag_obj)

                        current_tags.append(tag_obj)

                elif line.startswith('Feature:'):
                    for tag in feature_tags:
                        tag.feature_global = True

                elif line.startswith('Scenario Outline:'):
                    scenario_outline_header_flag = True
                    if current_tags:
                        for tag in current_tags:
                            if not tag.feature_global:
                                tag.scenario_outline_global = True
                                tag.scenario_outline_local = False
                        current_tags = []

                        for tag in feature_tags:
                            if not tag.feature_global:
                                tag.scenario_outline_global = True
                                tag.scenario_outline_local = False

                    else:
                        for tag in feature_tags:
                            if not tag.feature_global:
                                tag.scenario_outline_global = False
                                tag.scenario_outline_local = False

                elif line.startswith('Examples:'):
                    if not scenario_outline_header_flag:
                        for tag in feature_tags:
                            if tag.scenario_outline_local:
                                tag.scenario_outline_local = False

                    for tag in current_tags:
                        if not tag.feature_global or tag.scenario_outline_global:
                            tag.scenario_outline_local = True

                    current_tags = []

                elif line.startswith('|'):
                    if scenario_outline_header_flag:
                        scenario_outline_header_flag = False
                        continue
                    else:
                        feature_global_count += 1
                        for tag in feature_tags:
                            if tag.feature_global or tag.scenario_outline_global or tag.scenario_outline_local:
                                tag.test_count += 1

                elif line.startswith('Scenario:'):
                    feature_global_count += 1

                    for tag in feature_tags:
                        if tag.feature_global:
                            tag.test_count += 1
                        else:
                            tag.scenario_outline_global = False

                    if current_tags:
                        for tag in current_tags:
                            if tag.feature_global:
                                continue
                            else:
                                tag.test_count += 1
                        current_tags = []
                    else:
                        continue

        tags_list.append({'feature': feature,
                         'tags': feature_tags,
                         'tests_count': feature_global_count})

    return tags_list


def stats_output(tags_list):
    tags_list = sorted(tags_list, key = itemgetter('feature'))
    global_test_count = 0
    tag_stats = {}

    for tags in tags_list:
        global_test_count += tags['tests_count']
        print('')
        print('### "{0}" feature stats information: ###'.format(tags['feature']))
        for tag in tags['tags']:
            print('-', tag.tag_name + ':', str(tag.test_count))

            if tag.tag_name in tag_stats:
                tag_stats[tag.tag_name] += tag.test_count
            else:
                tag_stats[tag.tag_name] = tag.test_count

        print('Total number of tests: {0}'.format(tags['tests_count']))

    print('')
    print('--------------------------------------------------------------------------------')
    print('### Tag based statistics ###')
    for key, value in sorted(tag_stats.items(), key=lambda x:x[0]):
        print(key + ':', value)

    print('')
    print('--------------------------------------------------------------------------------')
    print('Global test count is {0}'.format(global_test_count))


def main():
    pass

if __name__ == '__main__':
    main()