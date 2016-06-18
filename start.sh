docker run -v $(pwd):/home/openga -ti openga:latest /bin/bash -c 'cd /home/openga; echo "Welcome to OpenGA! Please have a look on the README file or access www.openga.org."; exec "${SHELL:-sh}"'
