#include <iostream>
#include <vector>
#include <cmath>
#include <cstdint>
#include <stack>
#include <array>
#include <algorithm>

constexpr uint32_t createBitMask(int b) {
    return uint32_t(1) << b;
}

struct Square {
    int x, y, size;
};

static std::array<uint32_t, 33> BIT_PREFIXES;
static bool prefixes_initialized = false;

void initializePrefixes(int max_size) {
    BIT_PREFIXES[0] = 0;
    for (int i = 1; i <= max_size + 1; i++) {
        BIT_PREFIXES[i] = BIT_PREFIXES[i-1] | (1u << (i-1));
    }
    prefixes_initialized = true;
}

struct Board {
    int size;
    std::vector<uint32_t> cells;
    std::vector<Square> placed_squares;
    int minRow, minCol, maxRow, maxCol;

    Board(int n) : size(n), minRow(n), minCol(n), maxRow(-1), maxCol(-1), cells(n, 0) {
        if (!prefixes_initialized) {
            initializePrefixes(n);
        }
    }

    bool isOccupied(int row, int col) const {
        return (cells[row] & (1u << col)) != 0;
    }

    bool firstEmpty(int &x, int &y) {
        uint32_t fullRowMask = (1u << size) - 1;
        for (int i = 0; i < size; i++) {
            if (cells[i] != fullRowMask) {
                for (int j = 0; j < size; j++) {
                    if (!(cells[i] & (1u << j))) {
                        x = i;
                        y = j;
                        return true;
                    }
                }
            }
        }
        return false;
    }

    bool canPlace(int x, int y, int squareSize) const {
        if (x + squareSize > size || y + squareSize > size) return false;
        
        uint32_t mask = BIT_PREFIXES[y + squareSize] ^ BIT_PREFIXES[y];
        
        for (int i = x; i < x + squareSize; i++) {
            if (cells[i] & mask) return false;
        }
        return true;
    }

    void placeSquare(int x, int y, int squareSize) {
        uint32_t mask = BIT_PREFIXES[y + squareSize] ^ BIT_PREFIXES[y];
        
        for (int i = x; i < x + squareSize; i++) {
            cells[i] |= mask;
        }
        
        placed_squares.push_back({x, y, squareSize});
    }

    void removeSquare(int x, int y, int squareSize) {
        uint32_t mask = BIT_PREFIXES[y + squareSize] ^ BIT_PREFIXES[y];
        
        for (int i = x; i < x + squareSize; i++) {
            cells[i] &= ~mask;
        }
    }

    int emptyCellsCount() const {
        int count = 0;
        uint32_t fullRowMask = (1u << size) - 1;
        
        for (int i = 0; i < size; i++) {
            if (cells[i] == fullRowMask) continue;
            count += size - __builtin_popcount(cells[i]);
        }
        return count;
    }

    bool isRemainingSquare() {
        minRow = size + 1, minCol = size + 1, maxRow = -1, maxCol = -1;
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < size; ++j) {
                if (!isOccupied(i, j)) {
                    minRow = std::min(minRow, i);
                    minCol = std::min(minCol, j);
                    maxRow = std::max(maxRow, i);
                    maxCol = std::max(maxCol, j);
                }
            }
        }

        if (maxRow == -1) return false;

        int side = maxRow - minRow + 1;
        if (side != maxCol - minCol + 1) return false;

        return canPlace(minRow, minCol, side);
    }
};

int getMaxSquareSize(int n) {
    return (n/2) + 1;
}

void findSolution(Board initialBoard, int& minSquares, int targetCount, std::vector<Square>& bestSolution) {
    std::stack<Board> states;
    std::vector<Square> currentSolution;
    
    std::vector<Square> heuristic;
    heuristic.push_back({0, 0, initialBoard.size - 1});
    for (int i = 0; i < initialBoard.size; i++) heuristic.push_back({initialBoard.size - 1, i, 1});
    for (int i = 0; i < initialBoard.size - 1; i++) heuristic.push_back({i, initialBoard.size - 1, 1});
    
    if (heuristic.size() < bestSolution.size() || bestSolution.empty()) {
        bestSolution = heuristic;
        minSquares = heuristic.size();
    }
    
    int bestSide = getMaxSquareSize(initialBoard.size);
    Board tempBoard = initialBoard;
    tempBoard.placeSquare(0, 0, bestSide);
    tempBoard.placeSquare(0, bestSide, initialBoard.size - bestSide);
    tempBoard.placeSquare(bestSide, 0, initialBoard.size - bestSide);
    states.push(tempBoard);

    while (!states.empty()) {
        Board current = states.top();
        states.pop();
        
        int x, y;
        if (!current.firstEmpty(x, y)) {
            if (current.placed_squares.size() < bestSolution.size()) {
                bestSolution = current.placed_squares;
                minSquares = bestSolution.size();
            }
            continue;
        }
        
        if (current.placed_squares.size() >= bestSolution.size() || 
            current.placed_squares.size() > (size_t)targetCount) continue;
        
        int max_size = std::min({initialBoard.size - x, initialBoard.size - y});
        
        if (current.placed_squares.size() + current.emptyCellsCount() / (max_size * max_size) >= bestSolution.size()) 
            continue;
        
        while (max_size > 0 && !current.canPlace(x, y, max_size)) max_size--;
        
        for(int size = max_size; size >= 1; size--) {
            if (current.canPlace(x, y, size)) {
                current.placeSquare(x, y, size);
                states.push(current);
                current.placed_squares.pop_back();
                current.removeSquare(x, y, size);
            }   
        }
    }
}

void solve(int n, std::vector<Square>& bestResult) {
    Board board(n);
    int minSquares = n * n + 1;
    
    for (int targetCount = 1; targetCount <= minSquares; ++targetCount) {
        findSolution(board, minSquares, targetCount, bestResult);
        if (minSquares <= targetCount) break;
    }
}

int main() {
    int n;
    if (!(std::cin >> n)) return 0;
    if (n <= 1) {
        std::cout << "Неверное значение N" << std::endl;
        return 0;
    }

    if (n % 2 == 0) {
        int half = n / 2;
        std::vector<Square> solution = {
            {1, 1, half},
            {1, half + 1, half},
            {half + 1, 1, half},
            {half + 1, half + 1, half}
        };
        std::cout << solution.size() << "\n";
        for (const auto& square : solution) {
            std::cout << square.x << " " << square.y << " " << square.size << "\n";
        }
        return 0;
    }

    int divisor = n;
    for (int d = 2; d * d <= n; ++d) {
        if (n % d == 0) {
            divisor = d;
            break;
        }
    }

    int scale = n / divisor;

    std::vector<Square> smallResult;
    solve(divisor, smallResult);

    std::vector<Square> finalResult;
    finalResult.reserve(smallResult.size());
    for (const auto& square : smallResult) {
        finalResult.push_back({square.x * scale + 1, square.y * scale + 1, square.size * scale});
    }

    std::cout << finalResult.size() << "\n";
    for (const auto& square : finalResult) {
        std::cout << square.x << " " << square.y << " " << square.size << "\n";
    }

    return 0;
}