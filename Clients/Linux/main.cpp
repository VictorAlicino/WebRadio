#include <iostream>
#include <thread>
#include <fstream>

#include "lib/libvlcpp/vlcpp/vlc.hpp" //VLC Library

bool is_running = false;

int main() {
    //Capture the default configuration
    std::string mqtt_server, mqtt_port, mqtt_user, mqtt_pass, mqtt_topic;
    std::ifstream config("config.acn");
    if(config.peek() == std::ifstream::traits_type::eof()){
        std::cout << "Configuration file is empty.\n";
        return 1;
    }
    else{
        std::getline(config, mqtt_server);
        std::getline(config, mqtt_port);
        std::getline(config, mqtt_user);
        std::getline(config, mqtt_pass);
        std::getline(config, mqtt_topic);
    }

    while(is_running){

    }
    std::cout << "Hello, World!" << std::endl;
    return 0;
}
