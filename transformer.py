import os
import sys
from reader import Reader
from objectmapper import ObjectMapper

class Transformer:
    def __init__(self, xml_dir, out_dir, class_file, create_classes):
        self.xml_dir = xml_dir
        self.out_dir = out_dir
        self.class_file = class_file
        self.create_classes = create_classes

    def transform(self):
        reader = Reader(xml_dir=self.xml_dir)
        object_mapper = ObjectMapper()

        xml_files = reader.get_xml_files()
        annotations = object_mapper.map_files(xml_files, xml_dir=self.xml_dir)

        if self.create_classes:
            self.create_class_file(annotations=annotations)

        classes = reader.get_classes(self.class_file)
        self.write_to_txt(annotations, classes)

    def write_to_txt(self, annotations, classes):
        for annotation in annotations:
            output_path = os.path.join(self.out_dir, self.darknet_filename_format(annotation.filename))

            if not os.path.exists(os.path.dirname(output_path)):
                os.makedirs(os.path.dirname(output_path))

            with open(output_path, "w") as f:
                f.write(self.to_darknet_format(annotation, classes))

    def to_darknet_format(self, annotation, classes):
        result = []

        for obj in annotation.objects:
            if obj.name not in classes.keys():
                print(f"{obj.name} not found in {self.class_file}. Add it or use '-new' to create a new class file from the XML files.")
                sys.exit()
                
            x, y, width, height = self.get_object_params(obj, annotation.size)
            result.append(f"{classes[obj.name]} {x:.6f} {y:.6f} {width:.6f} {height:.6f}")

        return "\n".join(result)

    def create_class_file(self, annotations):
        classes = set()

        for annotation in annotations:
            for obj in annotation.objects:
                classes.add(obj.name)

        classes = sorted(list(classes))

        if os.path.exists(self.class_file):
            print(f"Specified file '{self.class_file}' already exists. Writing classes to './new_classes.txt' instead.")
            self.class_file = "new_classes.txt"

        with open(self.class_file, "w") as f:
            f.write("\n".join(classes))

    @staticmethod
    def get_object_params(obj, size):
        image_width = 1.0 * size.width
        image_height = 1.0 * size.height

        assert image_height > 0 and image_width > 0, "Invalid image width/height data"

        bndbox = obj.bndbox
        absolute_x = bndbox.xmin + 0.5 * (bndbox.xmax - bndbox.xmin)
        absolute_y = bndbox.ymin + 0.5 * (bndbox.ymax - bndbox.ymin)

        absolute_width = bndbox.xmax - bndbox.xmin
        absolute_height = bndbox.ymax - bndbox.ymin

        x = absolute_x / image_width
        y = absolute_y / image_height
        width = absolute_width / image_width
        height = absolute_height / image_height

        return x, y, width, height

    @staticmethod
    def darknet_filename_format(filename):
        pre, _ = os.path.splitext(filename)
        return f"{pre}.txt"
