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
    {4, -1, -2, -2, 0, -1, -1, 0, -2, -1, -1, -1, -1, -2, -1, 1, 0, -3, -2, 0, -2, -1, 0, -4},
    {-1, 5, 0, -2, -3, 1, 0, -2, 0, -3, -2, 2, -1, -3, -2, -1, -1, -3, -2, -3, -1, 0, -1, -4},
    {-2, 0, 6, 1, -3, 0, 0, 0, 1, -3, -3, 0, -2, -3, -2, 1, 0, -4, -2, -3, 3, 0, -1, -4},
    {-2, -2, 1, 6, -3, 0, 2, -1, -1, -3, -4, -1, -3, -3, -1, 0, -1, -4, -3, -3, 4, 1, -1, -4},
    {0, -3, -3, -3, 9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1, -3, -3, -2, -4},
    {-1, 1, 0, 0, -3, 5, 2, -2, 0, -3, -2, 1, 0, -3, -1, 0, -1, -2, -1, -2, 0, 3, -1, -4},
    {-1, 0, 0, 2, -4, 2, 5, -2, 0, -3, -3, 1, -2, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1, -4},
    {0, -2, 0, -1, -3, -2, -2, 6, -2, -4, -4, -2, -3, -3, -2, 0, -2, -2, -3, -3, -1, -2, -1, -4},
    {-2, 0, 1, -1, -3, 0, 0, -2, 8, -3, -3, -1, -2, -1, -2, -1, -2, -2, 2, -3, 0, 0, -1, -4},
    {-1, -3, -3, -3, -1, -3, -3, -4, -3, 4, 2, -3, 1, 0, -3, -2, -1, -3, -1, 3, -3, -3, -1, -4},
    {-1, -2, -3, -4, -1, -2, -3, -4, -3, 2, 4, -2, 2, 0, -3, -2, -1, -2, -1, 1, -4, -3, -1, -4},
    {-1, 2, 0, -1, -3, 1, 1, -2, -1, -3, -2, 5, -1, -3, -1, 0, -1, -3, -2, -2, 0, 1, -1, -4},
    {-1, -1, -2, -3, -1, 0, -2, -3, -2, 1, 2, -1, 5, 0, -2, -1, -1, -1, -1, 1, -3, -1, -1, -4},
    {-2, -3, -3, -3, -2, -3, -3, -3, -1, 0, 0, -3, 0, 6, -4, -2, -2, 1, 3, -1, -3, -3, -1, -4},
    {-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4, 7, -1, -1, -4, -3, -2, -2, -1, -2, -4},
    {1, -1, 1, 0, -1, 0, 0, 0, -1, -2, -2, 0, -1, -2, -1, 4, 1, -3, -2, -2, 0, 0, 0, -4},
    {0, -1, 0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1, 1, 5, -2, -2, 0, -1, -1, 0, -4},
    {-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1, 1, -4, -3, -2, 11, 2, -3, -4, -3, -2, -4},
    {-2, -2, -2, -3, -2, -1, -2, -3, 2, -1, -1, -2, -1, 3, -3, -2, -2, 2, 7, -1, -3, -2, -1, -4},
    {0, -3, -3, -3, -1, -2, -2, -3, -3, 3, 1, -2, 1, -1, -2, -2, 0, -3, -1, 4, -3, -2, -1, -4},
    {-2, -1, 3, 4, -3, 0, 1, -1, 0, -3, -4, 0, -3, -3, -2, 0, -1, -4, -3, -3, 4, 1, -1, -4},
    {-1, 0, 0, 1, -3, 3, 4, -2, 0, -3, -3, 1, -1, -3, -1, 0, -1, -3, -2, -2, 1, 4, -1, -4},
    {0, -1, -1, -1, -2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -2, 0, 0, -2, -1, -1, -1, -1, -1, -4},
    {-4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, 1},
};

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

int getValueFromMatrixOrDefault(std::vector<std::vector<int>> &matrix, int i, int j, int extraScore) {
    if (i < 0 || j < 0) {
        return INT_MIN;
    }
    int result = matrix[i][j];
    return result + extraScore;
}

void solve(std::unordered_map<std::string, std::string> data) {
    int gapScore = -4;

    std::string seq1 = data["Snark"];
    std::string seq2 = data["Sphinx"];

    std::vector<std::vector<int>> matrix(seq1.size(), std::vector<int>(seq2.size(), 0));

    for (int i = 1; i < seq2.size(); i++) {
        matrix[0][i] = i * gapScore;
    }

    for (int i = 1; i < seq1.size(); i++) {
        for (int j = 0; j < seq2.size(); j++) {
           
            char seq1Char = seq1[i];
            char seq2Char = seq2[j];

            int seq1Index = charToBlosumIndex[seq1[i]];
            int seq2Index = charToBlosumIndex[seq2[j]];

            int scoreValue = BLOSUM[seq1Index][seq2Index];

            int diagonally = getValueFromMatrixOrDefault(matrix, i - 1, j - 1, scoreValue);

            int left = getValueFromMatrixOrDefault(matrix, i, j - 1, gapScore);

            int above = getValueFromMatrixOrDefault(matrix, i - 1, j, gapScore);

            int result = std::max(std::max(diagonally, left), above);

            matrix[i][j] = result;

            int debug = 0;
        }
    }
    printMatrix(matrix);
    return;
}

int main(int argc, char **argv) {
    auto data = getInputData(argc, argv);
    solve(data);
}
