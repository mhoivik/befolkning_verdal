# Ganske standard makefile, hentet fra et annet prosjekt
CXX      := g++
CXXFLAGS := -std=c++17 -Wall -Wextra
TARGET   := montecarlo
SRC      := montecarlo.cpp

all: release

release: CXXFLAGS += -O3 -march=native -flto -DNDEBUG
release:
	@echo "Bygger RELEASE-versjon med maksimal optimalisering..."
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
	@echo "Ferdig! Kjør med: ./$(TARGET)"

debug: CXXFLAGS += -O0 -g3
debug:
	@echo "Bygger DEBUG-versjon..."
	$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)
	@echo "Ferdig! Du kan nå bruke gdb/lldb på: ./$(TARGET)"

clean:
	@echo "Renser opp..."
	rm -f $(TARGET)

.PHONY: all release debug clean
