import streamlit as st
import socket
import platform  # For getting the operating system name
import subprocess  # For executing a shell command
from configparser import ConfigParser


def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def side() -> None:
    # ip_txt = st.empty()
    with st.sidebar:  # .container() ?
        pass
        # col1, col2 = st.columns(2)
        #
        # with col1:
        #     st.button("ip")
        #
        # with col2:
        #     st.button("hei")
        # st.number_input('Pick a number', 0, 10)
        # st.text_area('Text to translate')
        # st.date_input('Your birthday')
        # st.time_input('Meeting time')
        # st.file_uploader('Upload a CSV')


class App:
    def __init__(self):
        # Pages
        self.page_names_to_funcs = {
            "Home ": self.home,
            "Setup the robot": self.setup_the_robot,
        }
        self.demo_name = st.sidebar.selectbox("Choose a function", self.page_names_to_funcs.keys())

        # Config
        self.config_object = ConfigParser()
        self.userinfo = self.read_conf("USERINFO")
        self.ip = self.userinfo["ip"]

    def run(self):
        self.page_names_to_funcs[self.demo_name]()

    def home(self):
        st.title("Welcome")

        if self.ip is not None:
            st.sidebar.success(f"Robot Ip: {self.ip}")
        else:
            st.sidebar.error('Ip address is not set')

    def setup_the_robot(self):
        self.check_ip = st.text_input('Enter robots ip address: ')

        if validate_ip(self.check_ip):
            self.userinfo["ip"] = self.check_ip
            self.write_conf()

        elif self.check_ip is None:
            st.write('IP address: None')
        elif validate_ip(self.check_ip) is False:
            st.write("Invalid ip address format, pleas input a valid ip address")

    def ping(self, host):
        """
        Returns True if host (str) responds to a ping request.
        Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
        """

        # Option for the number of packets as a function of
        param = '-n' if platform.system().lower() == 'windows' else '-c'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', param, '1', host]

        return subprocess.call(command) == 0

    def write_conf(self) -> None:
        # userinfo["password"] = "newpassword"

        # Write changes back to file
        with open('config.ini', 'w') as conf:
            self.config_object.write(conf)

    def read_conf(self, value: str):
        self.config_object.read("config.ini")
        return self.config_object[value]

    def add_dict_to_config(self, var: str, value: dict):
        # config_object["ip"] = {
        #     "ipaddr": "None"
        # }
        # https://tutswiki.com/read-write-config-files-in-python/

        self.config_object[var] = value
        with open('config.ini', 'w') as conf:
            self.config_object.write(conf)


# ######################## Remove after test ##############
App().run()
