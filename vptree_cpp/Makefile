CC = g++
CFLAGS = --std=c++11 -Wall -g
TARGET = vptest
DEP = vptree
DATA = datareader
UTIL = utils

$(TARGET): $(TARGET).o $(DEP).o $(DATA).o
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).o $(DEP).o $(DATA).o

$(TARGET).o: $(TARGET).cpp $(DEP).h 
	$(CC) $(CFLAGS) -c $(TARGET).cpp

$(DEP).o: $(DEP).cpp $(UTIL).cpp
	$(CC) $(CFLAGS) -c $(DEP).cpp $(UTIL).cpp

$(DATA).o: $(DATA).cpp
	$(CC) $(CFLAGS) -c $(DATA).cpp

clean:
	$(RM) *.o $(TARGET)

