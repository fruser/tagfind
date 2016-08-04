class Tags(object):
    global_count = 0

    def __init__(self, tag_name):
        self.tag_name = tag_name

        self.feature_global = False
        self.scenario_outline_global = False
        self.scenario_outline_local = False

        self.test_count = 0

    # def reset_tag(self):
    #     self.feature_global = False
    #     self.scenario_outline_global = False
    #     self.scenario_outline_local = False

    # def add_tag_count(self, feature, count):
    #     element_to_change = self.find_feature_element(feature)
    #     element_to_change['count'] += count
    #
    # def find_feature_element(self, feature):
    #     found_tag_obj = [element for element in self.appearance if element['feature'] == feature]
    #     return found_tag_obj[0] if found_tag_obj else None


def main():
    pass

if __name__ == '__main__':
    main()