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

std::unordered_map<std::string, std::string> readData(std::istream &inputStream) {
    std::unordered_map<std::string, std::string> res;

    std::string line;
    std::getline(inputStream, line);

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

        line = tempSequence;
    }

    return res;
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

std::unordered_map<std::string, std::string> getInputData(int argc, char **argv) {
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

std::tuple<int, std::vector<std::vector<int>>> solve(std::string seq1, std::string seq2) {
    std::vector<std::vector<int>> matrix(seq1.size() + 1, std::vector<int>(seq2.size() + 1, 0));

    for (int i = 1; i < seq2.size() + 1; i++) {
        matrix[0][i] = i * GAP_SCORE;
    }

    for (int i = 1; i < seq1.size() + 1; i++) {
        matrix[i][0] = i * GAP_SCORE;
    }

    for (int i = 1; i < seq1.size() + 1; i++) {
        for (int j = 1; j < seq2.size() + 1; j++) {
            int seq1Index = charToBlosumIndex[seq1[i - 1]];
            int seq2Index = charToBlosumIndex[seq2[j - 1]];

            int diagonally = getMatrixValuePlusExtraScore(matrix, i - 1, j - 1, BLOSUM[seq1Index][seq2Index]);
            int left = getMatrixValuePlusExtraScore(matrix, i, j - 1, GAP_SCORE);
            int above = getMatrixValuePlusExtraScore(matrix, i - 1, j, GAP_SCORE);

            matrix[i][j] = std::max(std::max(diagonally, left), above);
        }
    }
    return {matrix[seq1.size()][seq2.size()], matrix};
}

std::string getTracebackDirection(std::vector<std::vector<int>> &matrix, int &i, int &j) {
    int value = matrix[i][j];
    int above = matrix[i - 1][j];
    int left = matrix[i][j - 1];

    if (above + GAP_SCORE == value) {
        i = i - 1;
        return "a";

    } else if (left + GAP_SCORE == value) {
        j = j - 1;
        return "l";

    } else {
        i = i - 1;
        j = j - 1;
        return "d";
    }
}

void createTraceback(std::vector<std::vector<int>> &matrix, std::string seq1, std::string seq2) {
    // KQRK
    // K-AK

    std::string seq1Res = "";
    std::string seq2Res = "";

    int seq1Index = 0;
    int seq2Index = 0;

    printMatrix(matrix);

    int i = matrix.size() - 1;
    int j = matrix[0].size() - 1;

    while (i != 0 && j != 0) {
        std::string direction = getTracebackDirection(matrix, i, j);

        if (direction == "l") {  // Above
            seq2Res += seq2[seq2Index];
            seq2Index++;

            seq1Res += "-";
        } else if (direction == "a") {  // Left
            seq1Res += seq1[seq1Index];
            seq1Index++;

            seq2Res += "-";
        } else {  // Diagonally
            seq1Res += seq1[seq1Index];
            seq1Index++;

            seq2Res += seq2[seq2Index];
            seq2Index++;
        }
    }

    int debug = 0;
}

int main(int argc, char **argv) {
    auto data = getInputData(argc, argv);

    std::string seq1 = data["Sphinx"];
    std::string seq2 = data["Bandersnatch"];

    auto [result, matrix] = solve(seq1, seq2);
    std::cout << "Result: " << result << std::endl;

    createTraceback(matrix, seq1, seq2);
}
