#include <fstream>
#include <iostream>
#include <istream>
#include <string>
#include <vector>

std::vector<int> readData(std::istream &inputStream) {
    std::string line;
    std::getline(inputStream, line);

    int n = std::stoi(line);
    std::vector<int> valueVector{};

    for (int i = 0; i < n; i++) {
        int a = 0;
        inputStream >> a;
        valueVector.push_back(a);
    }

    return valueVector;
}

std::vector<int> getInputData(int argc, char **argv) {
    if (argc > 1) {
        std::ifstream ifile(argv[1]);
        return readData(ifile);
    } else {
        return readData(std::cin);
    }
}

int greedyApproach(std::vector<int> &coins, int amount, int stopAt) {
    int counter = 0;
    while (amount > 0) {
        for (int i = coins.size() - 1; i >= 0; i--) {
            int coin = coins[i];
            if (coin <= amount) {
                amount -= coin;
                counter++;

                if(counter > stopAt) {
                    return counter;
                }
                
                break;
            }
        }
    }
    return counter;
}

std::vector<int> dynamicApproach(std::vector<int> &coins, int amount) {
    std::vector<int> M(amount + 1, 0);

    for (int coin : coins) {
        for (int currentAmount = 1; currentAmount < amount + 1; currentAmount++) {
            if (coin <= currentAmount) {
                int leftover = currentAmount - coin;
                int coinUsedForLeftover = M[leftover];

                if (M[currentAmount] == 0) {
                    M[currentAmount] = coinUsedForLeftover + 1;
                } else {
                    M[currentAmount] = std::min(coinUsedForLeftover + 1, M[currentAmount]);
                }
            }
        }
    }
    return M;
}

void solve(std::vector<int> &coins) {
    int upperBound = coins[coins.size() - 1] + coins[coins.size() - 2];
    int lowerBound = coins[coins.size() - 3];

    auto dynamicResult = dynamicApproach(coins, upperBound);

    for (int i = upperBound; i >= lowerBound; i--) {
        if (greedyApproach(coins, i, dynamicResult[i]) != dynamicResult[i]) {
            std::cout << "non-canonical" << std::endl;
            return;
        }
    }
    std::cout << "canonical" << std::endl;
}

int main(int argc, char **argv) {
    auto coins = getInputData(argc, argv);
    solve(coins);
}
