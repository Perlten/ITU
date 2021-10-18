#include <fstream>
#include <iostream>
#include <istream>
#include <limits>
#include <numeric>
#include <regex>
#include <string>
#include <unordered_set>
#include <vector>

std::string ltrim(const std::string &s) { return std::regex_replace(s, std::regex("^\\s+"), std::string("")); }

std::string rtrim(const std::string &s) { return std::regex_replace(s, std::regex("\\s+$"), std::string("")); }

std::string trim(const std::string &s) { return ltrim(rtrim(s)); }

std::vector<std::string> splitLine(const std::string &line, std::string delimiter = " ") {
    size_t last = 0;
    size_t next = 0;

    std::vector<std::string> splittedLine = {};

    while ((next = line.find(delimiter, last)) != std::string::npos) {
        std::string subStr = trim(line.substr(last, next - last));
        splittedLine.push_back(subStr);
        last = next + 1;
    }

    if ((next = line.find(delimiter, last - 1)) != std::string::npos) {
        std::string subStr = trim(line.substr(last, next - last));
        splittedLine.push_back(subStr);
    }

    return splittedLine;
}

std::string readLine(std::istream &inputStream) {
    std::string line;
    std::getline(inputStream, line);
    return line;
}

std::vector<std::vector<int>> readData(std::istream &inputStream) {
    std::vector<std::string> metaSplit = splitLine(readLine(inputStream));
    int n = std::stoi(metaSplit[0]);
    int m = std::stoi(metaSplit[1]);

    std::vector<std::vector<int>> G((n * 2) + 2, std::vector<int>((n * 2) + 2, 0));

    for (int i = 1; i <= n; i++) {
        G[0][i] = 1;
    }

    int sinkEdge = G[0].size() - 1;
    for (int i = 0; i < m; i++) {
        std::vector<std::string> lineSplit = splitLine(readLine(inputStream));
        int p1 = std::stoi(lineSplit[0]);
        int p2 = std::stoi(lineSplit[1]);

        G[p1][p2 + n] = 1;
        G[p1 + n][sinkEdge] = 1;

        G[p2][p1 + n] = 1;
        G[p2 + n][sinkEdge] = 1;
    }
    return G;
}

std::vector<std::vector<int>> getInputData(int argc, char **argv) {
    if (argc > 1) {
        std::string fileName = argv[1];
        std::ifstream ifile(fileName);
        return readData(ifile);
    } else {
        return readData(std::cin);
    }
}

std::vector<int> bfs(const std::vector<std::vector<int>> &G, int source, int sink) {
    std::vector<int> queue = {source};

    std::unordered_map<int, int> traceback;
    std::unordered_set<int> seenNodes = {source};

    while (queue.size() > 0) {
        int currentNode = queue[0];
        queue.erase(queue.begin());

        seenNodes.insert(currentNode);

        if (currentNode == sink) {
            std::vector<int> path = {sink};

            int currentTracebackNode = traceback[sink];
            while (currentTracebackNode != source) {
                path.push_back(currentTracebackNode);
                currentTracebackNode = traceback[currentTracebackNode];
            }

            path.push_back(source);
            std::reverse(path.begin(), path.end());
            return path;
        }

        for (int i = 0; i < G[currentNode].size(); i++) {
            if (G[currentNode][i] == 0 || seenNodes.find(i) != seenNodes.end()) continue;
            queue.push_back(i);
            traceback[i] = currentNode;
        }
    }
    return {};
}

void solve(std::vector<std::vector<int>> &G) {
    int n = (G.size() - 1) / 2;

    auto path = bfs(G, 0, G.size() - 1);

    std::unordered_map<int, int> whoShotWho = {};

    while (path.size() > 0) {
        for (int i = 0; i < path.size() - 1; i++) {
            int current = path[i];
            int next = path[i + 1];

            if (current > 0 && current <= n) whoShotWho[current] = next - n;

            G[current][next] -= 1;
            G[next][current] += 1;
        }

        path = bfs(G, 0, G.size() - 1);
    }

    int totalFlow = std::accumulate(G[G.size() - 1].begin(), G[G.size() - 1].end(), 0);

    if (totalFlow != n) {
        std::cout << "Impossible" << std::endl;
    } else {
        for (int i = 1; i <= n; i++) {
            std::cout << whoShotWho[i] << std::endl;
        }
    }
}

int main(int argc, char **argv) {
    auto G = getInputData(argc, argv);
    solve(G);

    return 0;
}
