# SPDX-License-Identifier: Apache-2.0
# Host build + test runner for the ember core.
#
# The core is portable C99 with no float, no libm and no malloc, so this same
# source cross-compiles unchanged for Cortex-M33 (see ../mcu/Makefile).

CC      ?= cc
GRID_W  ?= 64
GRID_H  ?= 64

CFLAGS  := -std=c99 -O2 -Iinclude \
           -Wall -Wextra -Wpedantic -Wshadow -Wconversion -Wsign-conversion \
           -Wstrict-prototypes -Wmissing-prototypes -Wcast-qual \
           -DEMBER_GRID_W=$(GRID_W) -DEMBER_GRID_H=$(GRID_H)

SRC       := $(wildcard src/*.c)
TEST_SRC  := tests/main.c tests/test_fixed.c tests/test_event.c \
             tests/test_node.c tests/test_grid.c tests/golden_vec.c
BUILD     := build
GOLDEN_TXT:= tests/golden.txt

# Pin the golden hash if one has been recorded.
GOLDEN := $(shell [ -f $(GOLDEN_TXT) ] && cat $(GOLDEN_TXT) || echo 0)

.PHONY: all test golden pin clean

all: $(BUILD)/ember_tests $(BUILD)/ember_golden

$(BUILD):
	@mkdir -p $(BUILD)

# Tests are compiled without -Wconversion: the harness does deliberate casts
# for reporting. The library itself is held to the strict flags above.
$(BUILD)/ember_tests: $(SRC) $(TEST_SRC) | $(BUILD)
	$(CC) -std=c99 -O2 -Iinclude -Itests -Wall -Wextra \
	      -DEMBER_GRID_W=$(GRID_W) -DEMBER_GRID_H=$(GRID_H) \
	      -DEMBER_GOLDEN_EXPECTED=$(GOLDEN)u $^ -o $@

$(BUILD)/ember_golden: $(SRC) tests/golden_vec.c tests/golden_main.c | $(BUILD)
	$(CC) -std=c99 -O2 -Iinclude -Itests -Wall -Wextra \
	      -DEMBER_GRID_W=$(GRID_W) -DEMBER_GRID_H=$(GRID_H) $^ -o $@

# Strict compile of the library alone -- warnings here are real.
lint: | $(BUILD)
	@for f in $(SRC); do $(CC) $(CFLAGS) -Werror -c $$f -o /dev/null || exit 1; done
	@echo "lint: clean under -Wall -Wextra -Wpedantic -Wconversion -Werror"

test: lint $(BUILD)/ember_tests
	@./$(BUILD)/ember_tests

golden: $(BUILD)/ember_golden
	@./$(BUILD)/ember_golden

# Record the current golden hash so future runs (and the MCU parity check)
# are compared against it.
pin: $(BUILD)/ember_golden
	@./$(BUILD)/ember_golden | awk '{print "0x"$$1}' > $(GOLDEN_TXT)
	@echo "pinned golden hash: $$(cat $(GOLDEN_TXT))"

clean:
	@rm -rf $(BUILD)
