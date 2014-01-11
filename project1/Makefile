# Generic Makefile for C programs, builds an executable from
# all of the .c files present in the current directory

EXECUTABLE = musicModifierThing

CC = gcc
CFLAGS = -Wall -g -pedantic
LINK =
OBJECTS := $(patsubst %.c,%.o,$(wildcard *.c))

all: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS)
	$(CC) $(CFLAGS) $(LINK) -o $@ $^

%.o:%.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f $(EXECUTABLE) $(OBJECTS)
