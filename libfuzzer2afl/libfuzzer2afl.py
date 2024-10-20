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


def libfuzzer2afl(input_str):
    lines = input_str.splitlines()
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

    return '\n'.join(output_lines)
