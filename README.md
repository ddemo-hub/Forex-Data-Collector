# Forex-Data-Collector

## Description
### TBA
TBA

## Installation
### Dependencies
PostgreSQL 15 \
Python 3 \
Python packages used can be found in requirements.txt 

### Setup
* __On Linux:__
  - Run "make install" if Python 3 is not installed
  - Run "make init" to initialize a virtual environment with dependencies installed
  - You may use "make run" in order to run the main file

## Troubleshooting
### [SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED]
  - If [SSL: UNSAFE_LEGACY_RENEGOTIATION_DISABLED] exception is raised, run "export OPENSSL_CONF=openssl.cnf"
    + The cause of this exception is TCMB's EVDS system. 
    + WARNING: When enabling Legacy Unsafe Renegotiation, SSL connections will be vulnerable to the Man-in-the-Middle prefix attack as described in https://cve.mitre.org/cgi-bin/cvename.cgi?name=CAN-2009-3555 

## Future Work
  - Use Redis instead of the filesystem cache