//BrainStem2Example.cpp : Defines the entry point for the console application.
//
/////////////////////////////////////////////////////////////////////
//                                                                 //
// Copyright (c) 2018 Acroname Inc. - All Rights Reserved          //
//                                                                 //
// This file is part of the BrainStem release. See the license.txt //
// file included with this package or go to                        //
// https://acroname.com/software/brainstem-development-kit         //
// for full license details.                                       //
/////////////////////////////////////////////////////////////////////

#include <iostream>
#include "BrainStem2/BrainStem-all.h"

//The command line arguments are parsed using the open source cxxopts.hpp header
//implementation. The original source of this file can be found at:
//https://github.com/jarro2783/cxxopts
//FYI: Windows Users std::min() and std::max() are used by cxxopts.hpp.  This 
//     can cause an issues when including windows.h which defines these as macros.
//     To combate this I added NOMINMAX to the preprocessor defines for this project.
//     Debug -> BrainStem2Example Proprities -> Configuration Properties -> C/C++ -> preprocessor
#include "cxxopts.hpp"

int main(int argc, char* argv[])
{
    unsigned long serialNumber = 0;
    linkSpec* spec = NULL;
    int port = 0;
    int enable = 0;

    //Prints out the passed in arguments.
    std::cout << "Arguments: ";
    for (int x = 0; x < argc; x++) { std::cout << argv[x] << " ";  }
    std::cout << std::endl;

    //Create cxxopts options object
    cxxopts::Options options("BrainStem2Example.exe", " BrainStem2Example.exe - BrainStem Command Line Tool.");
    try
    {
        options
            .positional_help("[<Port> <Enable>]")
            .show_positional_help();

        options.add_options()
            ("h, help", "Prints Help usage")
            ("p, port", "The port in which this command will affect", cxxopts::value<int>())
            ("e, enable", "Disable or Enable the port (0 or 1)", cxxopts::value<int>())
            ("d, device", "Device Serial Number (in Hex).", cxxopts::value<std::string>()->default_value("0"))
            ("a, power", "Apply command to power lines")
            ("b, data", "Apply command to data lines");

        options.parse_positional({"port", "enable"});

        auto result = options.parse(argc, argv);
        

        //Parser - Help
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        if (result.count("help")) {
            std::cout << options.help() << std::endl;
            return 1;
        }
        ///////////////////////////////////////////////////////////////////////////////////////////////////


        //Parser - Device
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        if (result.count("device")) {

            serialNumber = std::stoul(result["d"].as<std::string>(), nullptr, 16);
            if (serialNumber == 0)  { spec = aDiscovery_FindFirstModule(USB); }
            else                    { spec = aDiscovery_FindModule(USB, (uint32_t)serialNumber); }

            if (spec == NULL) {
                std::cout << "Could not find any BrainStem Devices" << std::endl;
                std::cout << options.help() << std::endl;
                return 1;
            }
        }
        else {
            spec = aDiscovery_FindFirstModule(USB);
            if (spec == NULL) {
                std::cout << "Could not find any BrainStem Devices" << std::endl;
                std::cout << options.help() << std::endl;
                return 1;
            }
        }
        ///////////////////////////////////////////////////////////////////////////////////////////////////


        //Parser - Port - We need to check the range based on the device type
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        if (result.count("port")) {
            port = result["port"].as<int>();
            if (spec->model == aMODULE_TYPE_USBHub3p) {
                if ((port > 7) || (port < 0)) {
                    std::cout << "Incorrect port value: " << port << std::endl;
                    std::cout << "The USBHub3p ports range from 0-7" << std::endl;
                    std::cout << options.help() << std::endl;
                    aLinkSpec_Destroy(&spec);
                    return 1;
                }
            } 
            else if (spec->model == aMODULE_TYPE_USBHub2x4) {
                if ((port > 3) || (port < 0)) {
                    std::cout << "Incorrect port value: " << port << std::endl;
                    std::cout << "The USBHub2x4 ports range from 0-3" << std::endl;
                    std::cout << options.help() << std::endl;
                    aLinkSpec_Destroy(&spec);
                    return 1;
                }
            } 
            else { 
                std::cout << "The device that was found is not a hub. Model: " << spec->model << std::endl; 
                std::cout << options.help() << std::endl;
                aLinkSpec_Destroy(&spec);
                return 1;
            }
        }
        ///////////////////////////////////////////////////////////////////////////////////////////////////


        //Parser - Enable - We need to check the value is within range.
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        if (result.count("enable")) {
            enable = result["enable"].as<int>();
            if ((enable != 1) && (enable != 0)) {
                std::cout << "Incorrect value for enable" << std::endl;
                std::cout << "Acceptable values are 0 for false and 1 for true" << std::endl;
                std::cout << options.help() << std::endl;
                aLinkSpec_Destroy(&spec);
                return 1;
            }
        }
        ///////////////////////////////////////////////////////////////////////////////////////////////////

        //Parser - Power
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        //Nothing specific needs to be handled or tested. Option will be checked in "work".
        ///////////////////////////////////////////////////////////////////////////////////////////////////


        //Parser - Data
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        //Nothing specific needs to be handled or tested. Option will be checked in "work".
        ///////////////////////////////////////////////////////////////////////////////////////////////////


        //Work
        ///////////////////////////////////////////////////////////////////////////////////////////////////
        aErr err;

        if (spec->model == aMODULE_TYPE_USBHub3p) {

            aUSBHub3p hub;
            err = hub.connectFromSpec(*spec);

            if (err != aErrNone) { std::cout << "Error connecting to the device. Error: " << err << std::endl; }
            else { 
                std::cout << "Succefully connected to a USBHub3p. SN: 0x" << std::hex << spec->serial_num <<  std::endl; 
            
                if (enable) { 
                    if     ((result.count("power")) && (result.count("data")))  { err = hub.usb.setPortEnable(port); }
                    else if (result.count("power"))                             { err = hub.usb.setPowerEnable(port); }
                    else if (result.count("data"))                              { err = hub.usb.setDataEnable(port); }
                    else                                                        { err = hub.usb.setPortEnable(port); }
                }
                else {
                    if     ((result.count("power")) && (result.count("data")))  { err = hub.usb.setPortDisable(port); }
                    else if (result.count("power"))                             { err = hub.usb.setPowerDisable(port); }
                    else if (result.count("data"))                              { err = hub.usb.setDataDisable(port); }
                    else                                                        { err = hub.usb.setPortDisable(port); }
                }

                if (err != aErrNone)    { std::cout << "There was an error (" << err << ") " << (enable ? "enabling" : "disabling") << " Port: " << port << std::endl; }
                else                    { std::cout << "Port: " << port << " was succefully " << (enable ? "Enabled." : "Disabled.") << std::endl; }
            }
            hub.disconnect();
        }

        else if (spec->model == aMODULE_TYPE_USBHub2x4) {

            aUSBHub2x4 hub;
            err = hub.connectFromSpec(*spec);

            if (err != aErrNone) { std::cout << "Error connecting to the device. Error: " << err << std::endl; }
            else { 
                std::cout << "Succefully connected to a USBHub2x4. SN: 0x" << std::hex << spec->serial_num << std::endl; 

                if (enable) {
                    if     ((result.count("power")) && (result.count("data")))  { err = hub.usb.setPortEnable(port); }
                    else if (result.count("power"))                             { err = hub.usb.setPowerEnable(port); }
                    else if (result.count("data"))                              { err = hub.usb.setDataEnable(port); }
                    else                                                        { err = hub.usb.setPortEnable(port); }
                }
                else {
                    if     ((result.count("power")) && (result.count("data")))  { err = hub.usb.setPortDisable(port); }
                    else if (result.count("power"))                             { err = hub.usb.setPowerDisable(port); }
                    else if (result.count("data"))                              { err = hub.usb.setDataDisable(port); }
                    else                                                        { err = hub.usb.setPortDisable(port); }
                }

                if (err != aErrNone)    { std::cout << "There was an error (" << err << ") " << (enable ? "enabling" : "disabling") << " Port: " << port << std::endl; }
                else                    { std::cout << "Port: " << port << " was succefully " << (enable ? "Enabled." : "Disabled.") << std::endl; }
            }
            hub.disconnect();
        }

        else {
            std::cout << "This example is not capable of handing model: " << spec->model << std::endl;
            aLinkSpec_Destroy(&spec);
            return 1;
        }

        aLinkSpec_Destroy(&spec);
        ///////////////////////////////////////////////////////////////////////////////////////////////////

    }
    catch (const cxxopts::OptionException& e) {
        std::cout << "error parsing options: " << e.what() << std::endl;
        std::cout << options.help() << std::endl;
        return 1;
    }
    catch (...) {
        std::cout << "Unknown Exception Caught: " << std::endl;
        std::cout << options.help() << std::endl;
        return 1;
    }

    return 0;

}
