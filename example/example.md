# Spectre

Spectre is a tool developed based on Grey-box Fuzzing to generate points-to specifications for C/C++ library functions.

## Docker Environment Setup

To evaluate this artifact, a Linux machine with Docker installed is needed.

If Docker is not installed, install it by following the [Docker installation instructions](https://docs.docker.com/get-docker/).

1. Install the docker image.

    ```
    docker pull issta270/spectre
    ```
   
2. Start a container

   ```
   docker run -it issta270/spectre
   ```
3. Compile Spectre
   ```
   make all
   ```

Then you can run Spectre to generate points-to specifications for C/C++ library functions.Spean
