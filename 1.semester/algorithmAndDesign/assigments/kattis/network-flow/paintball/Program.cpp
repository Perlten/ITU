#include <chrono>
#include <fstream>
#include <iostream>
#include <numeric>
#include <regex>
#include <stack>
#include <string>
#include <unordered_set>
#include <vector>

std::string ltrim(const std::string &s) { return std::regex_replace(s, std::regex("^\\s+"), std::string("")); }

std::string rtrim(const std::string &s) { return std::regex_replace(s, std::regex("\\s+$"), std::string("")); }

std::string trim(const std::string &s) { return ltrim(rtrim(s)); }

std::chrono::steady_clock::time_point startTimer() {
    auto t = std::chrono::steady_clock::now();
    return t;
}
std::unordered_map<std::string, int> timetable(0);
void stopTimer(const std::string name, std::chrono::steady_clock::time_point preTime) {
    auto now = std::chrono::steady_clock::now();
    auto timeelapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - preTime).count();
    timetable[name] += timeelapsed;
}

void printTimer() {
    for (auto e : timetable) {
        std::cout << e.first << " " << e.second << std::endl;
    }
}
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

std::vector<std::vector<bool>> readData(std::istream &inputStream) {
    auto dataReadTimer = startTimer();
    int n, m;
    inputStream >> n >> m;

    std::vector<std::vector<bool>> G((n * 2) + 2, std::vector<bool>((n * 2) + 2, false));

    for (int i = 1; i <= n; i++) {
        G[0][i] = true;
    }

    int sinkEdge = G[0].size() - 1;
    int p1, p2;
    for (int i = 0; i < m; i++) {
        inputStream >> p1 >> p2;

        G[p1][p2 + n] = true;
        G[p1 + n][sinkEdge] = true;

        G[p2][p1 + n] = true;
        G[p2 + n][sinkEdge] = true;
    }

    stopTimer("dataRead", dataReadTimer);
    return G;
}

std::vector<std::vector<bool>> getInputData(int argc, char **argv) {
    if (argc > 1) {
        std::string fileName = argv[1];
        std::ifstream ifile(fileName);
        return readData(ifile);
    } else {
        return readData(std::cin);
    }
}

std::vector<int> dfs(const std::vector<std::vector<bool>> &G, int source, int sink) {
    auto dfsTimer = startTimer();
    int n = (G.size() - 1) / 2;

    std::stack<int> nodeStack;
    nodeStack.push(source);

    std::unordered_map<int, int> traceback;

    std::vector<bool> seenNodes(G.size());

    while (nodeStack.size() > 0) {
        int currentNode = nodeStack.top();
        nodeStack.pop();

        seenNodes[currentNode] = true;

        if (currentNode == sink) {
            auto traceBackTimer = startTimer();
            std::vector<int> path = {sink};

            int currentTracebackNode = traceback[sink];
            while (currentTracebackNode != source) {
                path.push_back(currentTracebackNode);
                currentTracebackNode = traceback[currentTracebackNode];
            }

            path.push_back(source);
            std::reverse(path.begin(), path.end());

            stopTimer("dfsTimer", dfsTimer);
            stopTimer("tracebackTimer", traceBackTimer);
            return path;
        }

        for (int i = 0; i < G[currentNode].size(); i++) {
            if (G[currentNode][i] == true && !seenNodes[i]) {
                nodeStack.push(i);
                traceback[i] = currentNode;
            }
        }
    }
    stopTimer("dfsTimer", dfsTimer);
    return {};
}

void solve(std::vector<std::vector<bool>> &G) {
    int n = (G.size() - 1) / 2;

    auto path = dfs(G, 0, G.size() - 1);

    std::unordered_map<int, int> whoShotWho = {};

    while (path.size() > 0) {
        auto solvetimer = startTimer();
        for (int i = 0; i < path.size() - 1; i++) {
            int current = path[i];
            int next = path[i + 1];

            if (current > 0 && current <= n) whoShotWho[current] = next - n;

            G[current][next] = false;
            G[next][current] = true;
        }

        stopTimer("solveTimer", solvetimer);

        path = dfs(G, 0, G.size() - 1);
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
    auto totalTimeStart = startTimer();

    auto G = getInputData(argc, argv);
    solve(G);

    stopTimer("total", totalTimeStart);
    printTimer();

    // dfs time 19625
    return 0;
}
