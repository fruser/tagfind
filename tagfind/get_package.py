from urllib import request
from zipfile import ZipFile


def get_package(archive, output):
    get_zip(archive, output + '.zip')
    extract_zip(output + '.zip', output)


def get_zip(archive, output):
    request.urlretrieve(archive, output)


def extract_zip(archive, output):
    with ZipFile(archive, 'r') as z:
        z.extractall(output)


def main():
    pass

if __name__ == '__main__':
    main()