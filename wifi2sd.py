#!/usr/bin/env python3
import argparse
import sys
import os

# https://linux.die.net/man/5/wpa_supplicant.conf
# https://www.raspberrypi.org/documentation/configuration/wireless/headless.md
# https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

CONFIG = {
    'PATH': '',                 # Path to Raspbian for Raspberry Pi SD location
    'WIFI_COUNTRY': '',         # WiFI country in which RPI is located in (ISO/IEC alpha2 code)
    'WIFI_SSID': '',            # WiFi network name
    'WIFI_PSK': '',             # WiFi network password
    'WIFI_KEY_MGMT': ''         # WiFi key management, default: WPA2
}

WIFI_CONFIG = 'wpa_supplicant.conf'
SSH_CONFIG = 'ssh'

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


def create_wifi_config():
    config = f"""ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country={CONFIG['WIFI_COUNTRY']}
       
network={{
    ssid="{CONFIG['WIFI_SSID']}"
    key_mgmt={CONFIG['WIFI_KEY_MGMT']}
    psk="{CONFIG['WIFI_PSK']}"
}}"""
    print('[+] creating wifi config file')
    write_config_file(os.path.join(CONFIG['PATH'], WIFI_CONFIG), config)


def create_ssh_config():
    print('[+] creating ssh config file')
    write_config_file(os.path.join(CONFIG['PATH'], SSH_CONFIG))


def write_config_file(f_path, content=''):
    with open(f_path, 'w') as f:
        f.write(content)


def path_exists(sd_path):
    return os.path.exists(sd_path)


if __name__ == "__main__":
    args_parser = argparse.ArgumentParser(description='Add WiFi config and enable SSH on a fresh Raspberry Pi SD')
    args_parser.add_argument('--p', type=str, help='Path to SD',
                             default=SCRIPT_PATH)
    args_parser.add_argument('--cc', type=str, help='Two letters country codes (ISO/IEC alpha2 code)',
                             default='PL')
    args_parser.add_argument('--ssid', type=str, help='WiFi SSID / name')
    args_parser.add_argument('--psk', type=str, help='WiFi password')
    args_parser.add_argument('--key', type=str, help='Key management; WPA-PSK for WPA2; NONE for no password',
                             default='WPA-PSK', choices=['WPA-PSK', 'NONE'])

    args = args_parser.parse_args()

    CONFIG['PATH'] = args.p
    CONFIG['WIFI_COUNTRY'] = args.cc
    CONFIG['WIFI_SSID'] = args.ssid
    CONFIG['WIFI_PSK'] = args.psk
    CONFIG['WIFI_KEY_MGMT'] = args.key

    if not path_exists(CONFIG['PATH']):
        sys.exit(f"No such directory: {CONFIG['PATH']}")

    create_ssh_config()
    create_wifi_config()

    sys.exit()
