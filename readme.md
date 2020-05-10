# Python J-Link scripting

## Dependencies

* <https://github.com/square/pylink>
* <https://github.com/posborne/cmsis-svd>
  => Currently do not use the version from pip, as it does not contain SVDParser.for_mcu but install from repo. Caution: On windows you have to copy the data directory to python\cmsis_svd directory as the symlink does not work correctly for installation
* <https://github.com/eliben/pyelftools>

### Target code dependencies
* <https://github.com/bblanchon/ArduinoJson>
* SeggerRTT <https://wiki.segger.com/RTT> (BufferSizeDown should be increased to something like 256, BufferSizeUp can be decreased to 256). If RTT needs to be used as print channel, use channel 1 for RPC.

## Features

* STM32CUBEMX file parsing (\*.ioc) for Pin config/names
* ELF-File parsing for finding symbol names/sizes
* Arbitrary register access by name
* All j-link functionalities (flashing, writing/reading memory, ...)
* GPIO sampling and plotting via JLink Memory Access
* rpc via RTT and json strings

## Feature Backlog

* Ram code execution
* Automatic controller detection (Seems not to be possible)
* IOC parser: Analog signal sorting
