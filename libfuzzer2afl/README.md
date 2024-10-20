# libfuzzer2afl

convert libfuzzer harnesses into AFL harnesses

```bash
# example usage
mkdir test/out
python main.py -i test/json-libfuzzer.cc -o test/out/json-afl.cc
```
