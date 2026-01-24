# Makefile for Carl Neural Network Core

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -fPIC

# Directories
SRC_DIR = carl_core
BUILD_DIR = build
TARGET_DIR = lib

# Library name
TARGET = $(TARGET_DIR)/libcarl_core.so

# Source files and object files
SOURCES = $(wildcard $(SRC_DIR)/*.c)
OBJECTS = $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SOURCES))

# Default target
all: $(TARGET)

# Rule to build the shared library
$(TARGET): $(OBJECTS)
	@mkdir -p $(TARGET_DIR)
	$(CC) -shared -o $@ $^

# Rule to compile source files into object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
	rm -rf $(BUILD_DIR) $(TARGET_DIR)

.PHONY: all clean
