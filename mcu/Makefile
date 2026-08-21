# SPDX-License-Identifier: Apache-2.0
#
# Cortex-M33 (STM32U585, the UNO Q's real-time brain) cross-build.
#
# The entire point of this directory: NONE of it needs the board. The dev kit
# does not ship until semi-finalists are announced, but a free toolchain gives
# real flash/RAM numbers today, and because the core is fixed-point with no
# float, no libm and no malloc, host and target output are bit-identical -- so
# the port can be *proved* correct months before the hardware arrives.
#
#   make size     real .text/.bss for the M33 -- the feasibility numbers
#   make parity   host vs target golden hash, byte for byte (needs QEMU)
#
# Toolchain (macOS):  brew install --cask gcc-arm-embedded && brew install qemu

CROSS   ?= arm-none-eabi-
CC      := $(CROSS)gcc
SIZE    := $(CROSS)size
CORE    := ../core
GRID_W  ?= 64
GRID_H  ?= 64

MCPU    := -mcpu=cortex-m33 -mthumb -mfloat-abi=soft
CFLAGS  := -std=c99 -Os -ffunction-sections -fdata-sections \
           -I$(CORE)/include -I$(CORE)/tests \
           -DEMBER_GRID_W=$(GRID_W) -DEMBER_GRID_H=$(GRID_H) \
           -Wall -Wextra -Wpedantic
SRC     := $(wildcard $(CORE)/src/*.c)
BUILD   := build

.PHONY: all size parity clean check-toolchain

check-toolchain:
	@command -v $(CC) >/dev/null 2>&1 || { \
	  echo "$(CC) not found."; \
	  echo "  macOS:  brew install --cask gcc-arm-embedded"; \
	  echo "  Debian: apt install gcc-arm-none-eabi"; \
	  echo "No board required -- this is a cross-compiler only."; exit 1; }

$(BUILD):
	@mkdir -p $(BUILD)

# Footprint of the integrator itself, with no runtime or BSP mixed in.
size: check-toolchain | $(BUILD)
	@for f in $(SRC); do \
	  $(CC) $(MCPU) $(CFLAGS) -c $$f -o $(BUILD)/$$(basename $$f .c).o || exit 1; done
	@echo ""
	@echo "ember core, Cortex-M33, -Os, $(GRID_W)x$(GRID_H) grid"
	@echo ""
	@$(SIZE) -t $(BUILD)/*.o
	@echo ""
	@echo "note: .bss above excludes the caller-allocated ember_grid."
	@printf "      sizeof(ember_grid) = "
	@$(CC) $(MCPU) $(CFLAGS) -S -o - -x c - <<< 'char s[sizeof(struct { char _[1]; })];' >/dev/null 2>&1 || true
	@cd $(CORE) && $(MAKE) -s golden GRID_W=$(GRID_W) GRID_H=$(GRID_H) | awk '{print $$3 " bytes ("$$3/1024" KB)"}'

# Bit-parity: same source, two architectures, identical hash.
parity: check-toolchain | $(BUILD)
	@command -v qemu-system-arm >/dev/null 2>&1 || { \
	  echo "qemu-system-arm not found (brew install qemu). Skipping."; exit 1; }
	@$(CC) $(MCPU) $(CFLAGS) --specs=rdimon.specs -Wl,--gc-sections \
	   $(SRC) $(CORE)/tests/golden_vec.c $(CORE)/tests/golden_main.c \
	   -o $(BUILD)/golden.elf -lrdimon
	@echo "host  : $$(cd $(CORE) && $(MAKE) -s golden GRID_W=$(GRID_W) GRID_H=$(GRID_H))"
	@echo "m33   : $$(qemu-system-arm -M mps2-an505 -cpu cortex-m33 -nographic \
	           -semihosting -kernel $(BUILD)/golden.elf 2>/dev/null | head -1)"
	@echo ""
	@echo "these two lines must match exactly."

clean:
	@rm -rf $(BUILD)
