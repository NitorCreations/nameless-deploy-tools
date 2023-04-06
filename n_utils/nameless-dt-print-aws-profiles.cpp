#include <fstream>
#include <iostream>
#include <string>
#include <unordered_set>

int main(int argc, const char* argv[]) {
    std::string prefix = "";
    std::unordered_set<std::string> ret;
    if (argc > 1) {
        prefix = argv[1];
    }
    if (!getenv("HOME")) {
        return 0;
    }
    std::string home = getenv("HOME");
    std::ifstream credentials(home + "/.aws/credentials", std::fstream::in);
    if (credentials) {
        std::string line;
        while (getline(credentials, line)) {
            if (line[0] != '[' || line[line.length() - 1] != ']') {
                continue;
            }
            std::string profile_name = line.substr(1, line.length() - 2);
            if (strncmp(profile_name.c_str(), prefix.c_str(), prefix.size()) == 0) {
                ret.insert(profile_name);
            }
        }
        credentials.close();
    }
    std::ifstream config(home + "/.aws/config", std::fstream::in);
    if (config) {
        std::string line;
        while (getline(config, line)) {
            if (line[0] != '[' || line[line.length() - 1] != ']') {
                continue;
            }
            std::string profile_name = line.substr(9, line.length() - 10);
            if (strncmp(profile_name.c_str(), prefix.c_str(), prefix.size()) == 0) {
                ret.insert(profile_name);
            }
        }
        config.close();
    }
    std::string res;
    for (auto profile : ret) {
        res.append(profile);
        res.push_back(' ');
    }
    std::cout << res << std::endl;
    return 0;
}
