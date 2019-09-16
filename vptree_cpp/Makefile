CC = g++
CFLAGS = --std=c++11 -Wall -g
TARGET = vptest
DEP = vptree

$(TARGET): $(TARGET).o $(DEP).o
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).o $(DEP).o

$(TARGET).o: $(TARGET).cpp $(DEP).h 
	$(CC) $(CFLAGS) -c $(TARGET).cpp

$(DEP).o: $(DEP).cpp
	$(CC) $(CFLAGS) -c $(DEP).cpp

clean:
	$(RM) $(TARGET)

