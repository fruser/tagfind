class Tags(object):
    global_count = 0

    def __init__(self, tag_name):
        self.tag_name = tag_name

        self.feature_global = False
        self.scenario_outline_global = False
        self.scenario_outline_local = False

        self.test_count = 0


def main():
    pass

if __name__ == '__main__':
    main()