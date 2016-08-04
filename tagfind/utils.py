from urllib import request
from zipfile import ZipFile
import os
import fnmatch
import glob
import re
import tags as tg


def get_package(archive, output):
    get_zip(archive, output + '.zip')
    extract_zip(output + '.zip', output)


def get_zip(archive, output):
    request.urlretrieve(archive, output)


def extract_zip(archive, output):
    with ZipFile(archive, 'r') as z:
        z.extractall(output)


def get_feature_files(directory):
    feature_files = []
    rootdir = glob.glob(directory + '/*/features/')[0]

    for subdir, dirs, files in os.walk(rootdir):
        for file in fnmatch.filter(files, '*.feature'):
            # print(os.path.join(subdir, file))
            # TODO: log this information
            feature_files.append({'file_name': os.path.splitext(file)[0],
                                  'location': os.path.join(subdir, file)})

    return feature_files


def find_tag_obj(tag_list, tag_name):
    found_tag_obj = [tag for tag in tag_list if tag.tag_name == tag_name]
    return found_tag_obj[0] if found_tag_obj else None


def parse_files(files):
    tag_list = []

    for file in files:
        with open(file['location'], 'r') as FileObj:
            feature = file['file_name']

            feature_tags = []
            current_tags = []

            scenario_outline_header_flag = False

            for line in FileObj:
                if re.match(r'\s', line) or re.match(r'#', line):
                    continue

                elif re.match(r'@', line):
                    rgx = re.compile('(@[\w]+)')
                    line_tags = rgx.findall(line)

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
                        tg.Tags.global_count += 1
                        for tag in feature_tags:
                            if tag.feature_global or tag.scenario_outline_global or tag.scenario_outline_local:
                                tag.test_count += 1

                elif line.startswith('Scenario:'):
                    tg.Tags.global_count += 1

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

        tag_list.append({'feature': feature,
                         'tags': feature_tags,
                         'test_count': tg.Tags.global_count})

    return tag_list



def main():
    pass

if __name__ == '__main__':
    main()