rm -rf CMakeFiles CMakeCache.txt
cp /home/inilabs/inilabs/roborace/caer/main_roborace.c main.c
cmake -DENABLE_FILE_INPUT=1 -DENABLE_STATISTICS=1 -DENABLE_VISUALIZER=1 .
make -j 4
