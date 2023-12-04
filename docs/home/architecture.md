# Architecture

The framework is built to be modular. Every part of the resume document inherits 
from the base class `Component`. This makes it possible to just define a list of 
components in the configuration file. 

As starting point we have the following requirements:
1. As an user, you need to be able to create your own components. These components should be 
   plug-and-play. Meaning that having the python file in the same directory, we should be able to point to
   a class in that file by just specifying it in the config file. No other installing needed.
2. The configuration file needs to be modular
   * The definition of the layout and the contents itself in the configuration needs to be separated
   * We should be able to link multiple configuration files from the main file, this way we can split
     layout from contents if desired

## Choice of configuration file

For the configuration file the yaml format has been chosen. The yaml format is easily human-readable
and allows for multiple layers of nesting. 

## Building blocks of the framework

The framework uses the library Pydantic as data class. 