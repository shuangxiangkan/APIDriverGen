import argparse
import os

main_func_handle = '''
int main(int argc, char** argv) {
  FILE* file;
  file = fopen(argv[1], "r");
  if (!file) return 0;
  if (fseeko(file, 0, SEEK_END) != 0) {
    fprintf(stderr, "fseeko error!\\n");
    return 0;
  }
  size_t size = ftello(file);
  printf("size is %zu\\n", size);
  uint8_t* data;
  if (fseeko(file, 0, SEEK_SET) != 0) {
    fprintf(stderr, "fseeko error!\\n");
    return 0;
  }
  data = (uint8_t*)malloc(sizeof(char) * size + 1);
  size_t fread_len = fread(data, size, 1, file);
  printf("fread_len is %zu\\n", fread_len);
  
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, type=str)
    parser.add_argument("--output", "-o", required=True, type=str)

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    output_path = os.path.abspath(args.output)

    with open(input_path) as input_file:
        lines = input_file.readlines()
        output_lines = []
        meet_test_one = False
        meet_bracket = False
        for line in lines:
            if 'int LLVMFuzzerTestOneInput' in line and not line.strip().startswith('/'):
                output_lines.append(main_func_handle)
                meet_test_one = True
                if '{' in line:
                    meet_bracket = True
            else:
                if meet_test_one and not meet_bracket:
                    if '{' in line:
                        meet_bracket = True
                    continue
                output_lines.append(line)
        with open(output_path, 'w') as output_file:
            for line in output_lines:
                output_file.write(line)




if __name__ == "__main__":
    main()
