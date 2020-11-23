import argparse
import json

def contains_trump_biden(line):
    return "trump" in line.lower() or "biden" in line.lower()

def clean(input_file, output_file):
    fr = open(input_file)
    with open(output_file, 'a') as fw:
        for line in fr:
            post_dict = json.loads(line)
            if contains_trump_biden(post_dict['title']):
                json.dump(post_dict, fw)
                fw.write("\n")
    fr.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file_to_clean', help='Path to input json file')
    parser.add_argument('output_file', help='Path to output json file')
    args = parser.parse_args()

    input_file = args.file_to_clean
    output_file = args.output_file

    clean(input_file, output_file)

if __name__ == '__main__':
    main()

