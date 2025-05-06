import os

class Reader:
    def __init__(self, xml_dir):
        self.xml_dir = xml_dir

    def get_xml_files(self):
        xml_files = []

        for root, _, files in os.walk(self.xml_dir):
            for file in files:
                if file.endswith(".xml"):
                    file_path = os.path.join(root, file)
                    file_path = os.path.relpath(file_path, start=self.xml_dir)
                    xml_files.append(file_path)
  
        return xml_files

    @staticmethod
    def get_classes(file):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), file), mode="r", encoding="utf8") as f:
            lines = f.readlines()

        return {value: key for (key, value) in enumerate(list(map(lambda x: x.strip(), lines)))}
