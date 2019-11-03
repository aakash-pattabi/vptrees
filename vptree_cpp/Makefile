CXX = g++
CPPFLAGS = --std=c++17
CXXFLAGS = -Wall -g
OBJS = utils.o datareader.o vptest.o
TARGET = vptest

$(TARGET) : $(OBJS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -o $(TARGET) $(OBJS)

vptest.o: datareader.h utils.h
datareader.o: utils.h

clean:
	$(RM) *.o $(TARGET)
