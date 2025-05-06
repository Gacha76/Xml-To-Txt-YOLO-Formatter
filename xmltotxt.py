import os
import sys
import argparse
from transformer import Transformer

def main():
    parser = argparse.ArgumentParser(description="Conversion from Pascal VOC XML to YOLO text format")
    parser.add_argument("-xml", help="Relative location of xml files directory", required=True)
    parser.add_argument("-out", help="Relative location of output txt files directory", default="out")
    parser.add_argument("-create", help="Create a new classes.txt file from the XML files (y/n)", default="n")
    parser.add_argument("-c", help="Relative path to classes file", default="classes.txt")
    args = parser.parse_args()

    xml_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.xml)
    out_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.out)
    class_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.c)
    create_classes = True if args.create.lower() == 'y' else False

    if not os.path.exists(xml_dir):
        print("Provide the correct directory for XML files.")
        sys.exit()

    if not os.path.exists(out_dir):
        while True:
            flag = input(f"Output directory '{args.out}' doesn't exist, create the directory? (y/Y/n/N): ").lower()
            
            if flag == 'n':
                print("Provide the correct output directory to proceed.")
                sys.exit()
            elif flag == 'y':
                break
        
        print(f"Creating output directory {args.out}.")
        os.makedirs(out_dir)

    if not os.access(out_dir, os.W_OK):
        print(f"{out_dir} directory is not writeable.")
        sys.exit()

    if args.create.lower() not in ['y', 'n']:
        print("Invalid -create argument. Acceptable arguments: 'y' 'n'")
        sys.exit()

    if create_classes:
        if args.c != "classes.txt":
            print(f"New class file creation enabled, ignoring provided class file '{args.c}'")
            class_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "classes.txt")        

    if not os.access(class_file, os.F_OK):
        if not create_classes:
            print(f"'{class_file}' file is missing.")
            sys.exit()

    if not os.access(class_file, os.R_OK):
        if not create_classes:
            print(f"'{class_file}' file is not readable.")
            sys.exit()
    
    transformer = Transformer(xml_dir=xml_dir, out_dir=out_dir, class_file=class_file, create_classes=create_classes)
    transformer.transform()

if __name__ == "__main__":
    main()
