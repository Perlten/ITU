#include <fstream>
#include <iostream>
#include <istream>
#include <regex>
#include <string>
#include <unordered_map>
#include <vector>

std::string ltrim(const std::string &s) { return std::regex_replace(s, std::regex("^\\s+"), std::string("")); }

std::string rtrim(const std::string &s) { return std::regex_replace(s, std::regex("\\s+$"), std::string("")); }

std::string trim(const std::string &s) { return ltrim(rtrim(s)); }

std::unordered_map<char, int> charToBlosumIndex = {{'A', 0},  {'R', 1},  {'N', 2},  {'D', 3},  {'C', 4},  {'Q', 5},  {'E', 6},  {'G', 7},  {'H', 8},  {'I', 9},  {'L', 10}, {'K', 11},
                                                   {'M', 12}, {'F', 13}, {'P', 14}, {'S', 15}, {'T', 16}, {'W', 17}, {'Y', 18}, {'V', 19}, {'B', 20}, {'Z', 21}, {'X', 22}};
std::vector<std::vector<int>> BLOSUM = {
    {4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0, -2, -1, 0},
    {-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3, -1, 0, -1},
    {-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3, 3, 0, -1},
    {-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3, 4, 1, -1},
    {0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1, -3, -3, -2},
    {-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2, 0, 3, -1},
    {-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1},
    {0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3, -1, -2, -1},
    {-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3, 0, 0, -1},
    {-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3, -3, -3, -1},
    {-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1, -4, -3, -1},
    {-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2, 0, 1, -1},
    {-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1, -3, -1, -1},
    {-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1, -3, -3, -1},
    {
        -1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2, -2, -1, -2,
    },
    {1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2, 0, 0, 0},
    {0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0, -1, -1, 0},
    {-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3, -4, -3, -2},
    {-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1, -3, -2, -1},
    {0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4, -3, -2, -1},
    {-2, -1, 3, 4, -3, 0, 1, -1, 0, -3, -4, 0, -3, -3, -2, 0, -1, -4, -3, -3, 4, 1, -1},
    {-1, 0, 0, 1, -3, 3, 4, -2, 0, -3, -3, 1, -1, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1},
    {0, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 0, 0, -2, -1, -1, -1, -1, -1},
};

const int GAP_SCORE = -4;

std::tuple<std::unordered_map<std::string, std::string>, std::vector<std::string>> readData(std::istream &inputStream) {
    std::unordered_map<std::string, std::string> res;

    std::string line;
    std::getline(inputStream, line);

    std::vector<std::string> keyVector;

    while (line != "") {
        std::string species = trim(line.substr(1));
        std::string sequence = "";

        std::string tempSequence;
        std::getline(inputStream, tempSequence);

        while (tempSequence != "" && tempSequence.find(">") == std::string::npos) {
            sequence.append(tempSequence);
            std::getline(inputStream, tempSequence);
        }
        res[species] = sequence;
        keyVector.push_back(species);

        line = tempSequence;
    }

    return {res, keyVector};
}

void printMatrix(std::vector<std::vector<int>> &matrix) {
    for (int i = 0; i < matrix.size(); i++) {
        for (int j = 0; j < matrix[0].size(); j++) {
            std::cout << matrix[i][j] << " ";
        }
        std::cout << std::endl;
    }
    std::cout << "\n\n\n" << std::endl;
}

std::tuple<std::unordered_map<std::string, std::string>, std::vector<std::string>> getInputData(int argc, char **argv) {
    if (argc > 1) {
        std::string path = argv[1];
        std::ifstream ifile(path);
        return readData(ifile);
    } else {
        return readData(std::cin);
    }
}

int getMatrixValuePlusExtraScore(std::vector<std::vector<int>> &matrix, int i, int j, int extraScore) {
    int result = matrix[i][j];
    return result + extraScore;
}

enum class Direction { DIAGONAL, UP, LEFT, UNKOWN };

std::tuple<int, Direction> pickDirection(int diagonally, int left, int above) {
    if (diagonally >= left && diagonally >= above) {
        return {diagonally, Direction::DIAGONAL};
    } else if (left >= diagonally && left >= above) {
        return {left, Direction::LEFT};
    } else {
        return {above, Direction::UP};
    }
}

std::tuple<int, std::vector<std::vector<Direction>>> solve(std::string seq1, std::string seq2) {
    std::vector<std::vector<int>> matrix(seq1.size() + 1, std::vector<int>(seq2.size() + 1, 0));
    std::vector<std::vector<Direction>> tracebackMatrix(seq1.size() + 1, std::vector<Direction>(seq2.size() + 1, Direction::UNKOWN));

    for (int i = 1; i < seq2.size() + 1; i++) {
        matrix[0][i] = i * GAP_SCORE;
        tracebackMatrix[0][i] = Direction::LEFT;
    }

    for (int i = 1; i < seq1.size() + 1; i++) {
        matrix[i][0] = i * GAP_SCORE;
        tracebackMatrix[i][0] = Direction::UP;
    }

    for (int i = 1; i < seq1.size() + 1; i++) {
        for (int j = 1; j < seq2.size() + 1; j++) {
            int seq1Index = charToBlosumIndex[seq1[i - 1]];
            int seq2Index = charToBlosumIndex[seq2[j - 1]];

            int diagonally = getMatrixValuePlusExtraScore(matrix, i - 1, j - 1, BLOSUM[seq1Index][seq2Index]);
            int left = getMatrixValuePlusExtraScore(matrix, i, j - 1, GAP_SCORE);
            int above = getMatrixValuePlusExtraScore(matrix, i - 1, j, GAP_SCORE);
            auto [bestScore, direction] = pickDirection(diagonally, left, above);

            matrix[i][j] = bestScore;
            tracebackMatrix[i][j] = direction;
        }
    }
    return {matrix[seq1.size()][seq2.size()], tracebackMatrix};
}

std::tuple<std::string, std::string> tracebackMatrixToString(std::vector<std::vector<Direction>> &tracebackMatrix, std::string &seq1, std::string &seq2) {
    std::string seq1Res = "";
    std::string seq2Res = "";

    int i = tracebackMatrix.size() - 1;
    int j = tracebackMatrix[0].size() - 1;
    Direction currentDirection = tracebackMatrix[i][j];
    do {
        if (currentDirection == Direction::DIAGONAL) {
            seq1Res.insert(0, 1, seq1[i - 1]);
            seq2Res.insert(0, 1, seq2[j - 1]);
            i -= 1;
            j -= 1;
        } else if (currentDirection == Direction::LEFT) {
            seq1Res.insert(0, 1, '-');
            seq2Res.insert(0, 1, seq2[j - 1]);
            j -= 1;
        } else {
            seq1Res.insert(0, 1, seq1[i - 1]);
            seq2Res.insert(0, 1, '-');
            i -= 1;
        }

        currentDirection = tracebackMatrix[i][j];
    } while (currentDirection != Direction::UNKOWN);

    return {seq1Res, seq2Res};
}

int main(int argc, char **argv) {
    auto [data, keyVector] = getInputData(argc, argv);

    // std::cout << kv.first << " " << kv2.first << std::endl;
    for (int i = 0; i < keyVector.size(); i++) {
        for (int j = i + 1; j < keyVector.size(); j++) {
            std::cout << keyVector[i] << " / " << keyVector[j] << std::endl;
            std::string seq1 = data[keyVector[i]];
            std::string seq2 = data[keyVector[j]];

            auto [result, tracebackMatrix] = solve(seq1, seq2);
            std::cout << "Result: " << result << std::endl;

            auto [seq1Res, seq2Res] = tracebackMatrixToString(tracebackMatrix, seq1, seq2);
            std::cout << seq1Res << std::endl << seq2Res << std::endl << std::endl;
        }
    }

    return 0;
}
