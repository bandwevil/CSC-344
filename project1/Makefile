# Generic Makefile for C programs, builds an executable from
# all of the .c files present in the current directory

EXECUTABLE = arrange

CC = gcc
CFLAGS = -Wall -g -pedantic
LINK = -lsndfile
OBJECTS := $(patsubst %.c,%.o,$(wildcard *.c))

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LINK)

%.o:%.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(EXECUTABLE) $(OBJECTS)
