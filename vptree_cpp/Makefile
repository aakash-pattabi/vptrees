CXX = g++
CPPFLAGS = --std=c++17
CXXFLAGS = -Wall -g
OBJS = vptest.o datareader.o utils.o vptree.o
TARGET = vptest

$(TARGET) : $(OBJS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $(TARGET) $(OBJS)

vptest.o: datareader.h utils.h vptree.h
datareader.o: utils.h
vptree.o: utils.h

clean:
	$(RM) *.o $(TARGET)
