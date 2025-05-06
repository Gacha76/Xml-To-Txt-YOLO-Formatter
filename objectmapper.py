import os
import logging
import declxml as xml

class Annotation:
    def __init__(self):
        self.size = None
        self.objects = None
        self.filename = None

    def __repr__(self):
        return f"Annotation(size={self.size}, objects={self.objects}, filename={self.filename})"

class Size:
    def __init__(self):
        self.width = None
        self.height = None

    def __repr__(self):
        return f"Size(width={self.width}, height={self.height})"

class Object:
    def __init__(self):
        self.name = None
        self.bndbox = None

    def __repr__(self):
        return f"Object(name={self.name}, bndbox={self.bndbox})"

class Box:
    def __init__(self):
        self.xmin = None
        self.ymin = None
        self.xmax = None
        self.ymax = None

    def __repr__(self):
        return f"Box(xmin={self.xmin}, ymin={self.ymin}, xmax={self.xmax}, ymax={self.ymax})"

class ObjectMapper:
    def __init__(self):
        self.processor = xml.user_object("annotation", Annotation, [
            xml.user_object("size", Size, [
                xml.integer("width"),
                xml.integer("height"),
            ], alias="size"),
            xml.array(
                xml.user_object("object", Object, [
                    xml.string("name"),
                    xml.user_object("bndbox", Box, [
                        xml.integer("xmin"),
                        xml.integer("ymin"),
                        xml.integer("xmax"),
                        xml.integer("ymax"),
                    ], alias="bndbox")
                ]), alias="objects"
            ),
            xml.string("filename")
        ])

    def map_data(self, xml_file_path, xml_dir):
        annotation = xml.parse_from_file(root_processor=self.processor, xml_file_path=os.path.join(xml_dir, xml_file_path))
        annotation.filename = xml_file_path

        return annotation

    def map_files(self, xml_file_paths, xml_dir):
        result = []

        for xml_file_path in xml_file_paths:
            try:
                result.append(self.map_data(xml_file_path=xml_file_path, xml_dir=xml_dir))
            except Exception as e:
                logging.error(str(e))

        return result
