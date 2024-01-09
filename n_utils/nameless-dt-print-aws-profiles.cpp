#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <set>
#include <string_view>

/// Print all unique AWS profile names found from config.
int main(const int argc, const char* argv[]) {
    const auto home = std::getenv("HOME");
    if (!home) {
        return 0;
    }

    std::string_view prefix;
    std::set<std::string> profiles;
    if (argc > 1) {
        prefix = argv[1];
    }

    // Lambda function to extract aws profile names from a file
    auto get_aws_profiles = [&](const std::filesystem::path& path, const size_t profile_name_start_offset, const size_t profile_name_end_offset) {
        std::ifstream file(path, std::fstream::in);
        if (file) {
            std::string line;
            while (std::getline(file, line)) {
                if (!line.starts_with('[') || !line.ends_with(']')) {
                    continue;
                }
                auto profile_name = std::string_view(line).substr(profile_name_start_offset, line.length() - profile_name_end_offset);
                if (!profile_name.empty() && profile_name.starts_with(prefix)) {
                    profiles.insert(std::string(profile_name));
                }
            }
        }
    };

    const auto credentials_path = std::filesystem::path(home) / ".aws" / "credentials";
    get_aws_profiles(credentials_path, 1, 2);

    const auto config_path = std::filesystem::path(home) / ".aws" / "config";
    get_aws_profiles(config_path, 9, 10);

    for (const auto& profile : profiles) {
        std::cout << profile << ' ';
    }
    std::cout << std::endl;
    return 0;
}
