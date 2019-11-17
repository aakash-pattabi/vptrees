CXX = g++
CPPFLAGS = --std=c++17
CXXFLAGS = -Wall -g -Ofast
OBJS = datareader.o utils.o vptree.o vptest.o
TARGET = vptest

$(TARGET) : $(OBJS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $(TARGET) $(OBJS)

vptest.o: vptree.h utils.h datareader.h
vptree.o: utils.h
datareader.o: utils.h

clean:
	$(RM) *.o $(TARGET)
