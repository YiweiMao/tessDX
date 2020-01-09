# the compiler:
CC = g++

# compiler flags:
CFLAGS = -Wall -Wextra -pedantic # -std=c99

SRC_DIR = src
OBJ_DIR = obj
_DEPS = tessellator.hpp
_OBJS = tess_exp.o tessellator.o
DEPS = $(patsubst %,$(SRC_DIR)/%,$(_DEPS))
OBJS = $(patsubst %,$(OBJ_DIR)/%,$(_OBJS))

# link libraries
LIBS = 

# the build target executable:
TARGET = tess_exp

# Builds all object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# Links and compiles all the object files into executable
$(TARGET): $(OBJS)
	$(CC) -o $@ $(OBJS) $(CFLAGS) $(LIBS) -static

all: $(TARGET)


.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)

run:
	clear
	./$(TARGET)
memcheck:
	clear
	valgrind --leak-check=yes --track-origins=yes ./$(TARGET)