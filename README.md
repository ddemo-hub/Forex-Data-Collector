# Forex-Data-Collector

## Description
### Project
- A data collector and data provider module that operates on the foreign exchange rates of the Turkish Lira brokered by several banks & exchanges in the Republic of Türkiye.
- Foreign exchange rates are collected by scraping the data provided by the exchanges at regular intervals as frequently as possible without getting blocked.
- The data provider module supports WebHook and WebSocket protocols. Every time a change is detected at the forex rates, the change is broadcasted to the hooks & sockets and it is saved into the database. 
- Currently supported exchanges are: 
    * Central Bank of the Republic of Türkiye 
    * Yapı Kredi 
    * Ziraat Bankası
    * Altınkaynak
    * Kapalı Çarşı

## Installation
### Dependencies
PostgreSQL 15 \
Python 3 

### Setup
* Fill in the configuration parameters in .yaml files located at 'data_collector/src/configs/' with the required information
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
