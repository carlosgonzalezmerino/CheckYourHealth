import xml.etree.ElementTree as ET
import json

class AppleHealth(object):
    """
    Parses and stores apple health information
    """
    def __init__(self, data_file, data_save_file):

        self.data_file = data_file
        self.data_save_file = data_save_file
        self.root = self.load_data()
        record_fields = ["sourceName", "unit", "startDate", "endDate", "value"]
        self.events = {"Me": {None: ["HKCharacteristicTypeIdentifierDateOfBirth",
                                     "HKCharacteristicTypeIdentifierBiologicalSex",
                                     "HKCharacteristicTypeIdentifierBloodType"]
                              },
                       "Record": {"HKQuantityTypeIdentifierHeight": record_fields,
                                  "HKQuantityTypeIdentifierBodyMass": record_fields,
                                  "HKQuantityTypeIdentifierHeartRate": record_fields,
                                  "HKQuantityTypeIdentifierStepCount": record_fields,
                                  "HKQuantityTypeIdentifierDistanceWalkingRunning": record_fields,
                                  "HKQuantityTypeIdentifierBasalEnergyBurned": record_fields,
                                  "HKQuantityTypeIdentifierActiveEnergyBurned": record_fields,
                                  "HKQuantityTypeIdentifierFlightsClimbed":  record_fields,
                                  "HKQuantityTypeIdentifierAppleExerciseTime":record_fields,
                                  "HKQuantityTypeIdentifierRestingHeartRate": record_fields,
                                  "HKQuantityTypeIdentifierWalkingHeartRateAverage": record_fields,
                                  "HKCategoryTypeIdentifierSleepAnalysis": record_fields
                                  }
                       }
        self.structured_info = {"Me": {None: []},
                                "Record": {"HKQuantityTypeIdentifierHeight": [],
                                           "HKQuantityTypeIdentifierBodyMass": [],
                                           "HKQuantityTypeIdentifierHeartRate": [],
                                           "HKQuantityTypeIdentifierStepCount": [],
                                           "HKQuantityTypeIdentifierDistanceWalkingRunning": [],
                                           "HKQuantityTypeIdentifierBasalEnergyBurned": [],
                                           "HKQuantityTypeIdentifierActiveEnergyBurned": [],
                                           "HKQuantityTypeIdentifierFlightsClimbed": [],
                                           "HKQuantityTypeIdentifierAppleExerciseTime": [],
                                           "HKQuantityTypeIdentifierRestingHeartRate": [],
                                           "HKQuantityTypeIdentifierWalkingHeartRateAverage": [],
                                           "HKCategoryTypeIdentifierSleepAnalysis": []
                                           }
                                }

    def extract_row_data(self, event, event_type, info):
        """
        Parses one record of data from apple information
        :param event:
        :param event_type:
        :param info:
        :return:
        """
        structured_info = {"data": {}}
        if self.events.get(event):
            fields_to_extract = self.events[event].get(event_type)
            if fields_to_extract:
                for field in fields_to_extract:
                    structured_info["data"][field] = info.attrib.get(field)
                return structured_info
        else:
            return None

    def load_data(self):
        """
        Parses apple data file
        :return:
        """
        tree = ET.parse(self.data_file)
        return tree.getroot()

    def save_data(self, data):
        """
        Stores Data
        :param data:
        :return:
        """
        f = open(self.data_save_file, 'w+')
        f.write(json.dumps(data, indent=4))
        f.close()

    def format_data(self):
        """
        Formats apple health data to a standard format
        :return:
        """
        for child in self.root:
            event = child.tag
            event_type = child.attrib.get('type')
            extracted_data = self.extract_row_data(event, event_type, child)
            if extracted_data:
                self.structured_info[event][event_type].append(extracted_data)
        self.save_data(self.structured_info)


if __name__ == '__main__':
    import os
    os.chdir('..')
    apple = AppleHealth('Data/export.xml', 'Data/saved_info.json')
    apple.format_data()