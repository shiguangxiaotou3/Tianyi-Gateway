import requests
import json
import re


class network:
    def __init__(self, username, password, ip='192.168.1.1'):
        self.url = 'http://' + ip
        self.username = username
        self.password = password
        self.cookies = None
        self.login_success = False
        self.token = None

    def login(self):
        try:
            data = {'username': self.username, 'psd': self.password}
            response = requests.post(self.url + "/cgi-bin/luci/", data=data, allow_redirects=False)
            print(response.cookies)
            if response.status_code == 302 and response.cookies:
                self.login_success = True
                self.cookies = response.cookies
                try:
                    res = requests.get(self.url + "/cgi-bin/luci/", cookies=self.cookies)
                    match = re.search(r"token:\s*'([^']+)'", res.text)
                    if match:
                        self.token = match.group(1)
                        print(self.token)
                    else:
                        print("未找到匹配的 token 值")
                except Exception as e:
                    print("An error occurred:", e)

            return True
        except Exception as e:
            print("An error occurred:", e)
            return False

    def logout(self):
        if self.login_success:
            response = requests.post(self.url + '/cgi-bin/luci/admin/logout', data={'token': self.token},
                                     allow_redirects=False)

    def network_reboot(self):
        response = requests.post(self.url + '/cgi-bin/luci/admin/reboot', data={'token': self.token},
                                 allow_redirects=False)
        print(response.text)
        return json.loads(response.text)

    def get_device_list(self):
        """获取联网设备"""
        if self.login_success:
            response = requests.get(self.url + "/cgi-bin/luci/admin/allInfo", cookies=self.cookies)
            return json.loads(response.text)

    def get_network_device_info(self):
        """获取网关信息"""
        if self.login_success:
            response = requests.get(self.url + "/cgi-bin/luci/admin/settings/gwinfo?get=all", cookies=self.cookies)
            return json.loads(response.text)

    def get_network_info(self):
        """获取网关信息"""
        if self.login_success:
            response = requests.get(self.url + "/cgi-bin/luci/admin/settings/gwinfo?get=part", cookies=self.cookies)
            return json.loads(response.text)

    def get_mapping_list(self):
        """获取端口映射列表"""
        if self.login_success:
            response = requests.get(self.url + "/cgi-bin/luci/admin/settings/pmDisplay", cookies=self.cookies)
            return json.loads(response.text)

    def on_mapping_record(self, srvname):
        """开启端口映射"""
        data = {
            "token": self.token,
            "op": "enable",
            "srvname": srvname
        }
        response = requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetSingle", data=data, cookies=self.cookies)
        return json.loads(response.text)

    def off_mapping_record(self, srvname):
        """关闭端口映射"""
        data = {
            "token": self.token,
            "op": "disable",
            "srvname": srvname
        }
        response = requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetSingle", data=data, cookies=self.cookies)
        return json.loads(response.text)

    def del_mapping_record(self, srvname):
        """先增端口映射"""
        data = {
            "token": self.token,
            "op": "del"
        }
        response = requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetSingle", data=data, cookies=self.cookies)
        return json.loads(response.text)

    def on_mapping_record_all(self):
        """开启全部端口映射"""
        data = {
            "token": self.token,
            "op": "enable"
        }
        requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetAll", data=data, cookies=self.cookies)

    def off_mapping_record_all(self):
        """关闭全部端口映射"""
        data = {
            "token": self.token,
            "op": "disable"
        }
        requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetAll", data=data, cookies=self.cookies)

    def del_mapping_record_all(self):
        """删除端口映射"""
        data = {
            "token": self.token,
            "op": "del"
        }
        requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetAll", data=data, cookies=self.cookies)

    def add_mapping_record(self, srvname, internal_ip, ex_port, in_port, protocol='TCP'):
        """新增端口映射"""
        data = {
            "token": self.token,
            "op": "add",
            "srvname": srvname,
            "client": internal_ip,
            "protocol": protocol,
            "exPort": ex_port,
            "inPort": in_port
        }
        response = requests.post(self.url + "/cgi-bin/luci/admin/settings/pmSetSingle", data=data, cookies=self.cookies)
        return json.loads(response.text)

    def get_network_status(self):
        """获取网关运行状态"""
        if self.login_success:
            response = requests.get(self.url + "/cgi-bin/luci/admin/settings/gwstatus", cookies=self.cookies)
            return json.loads(response.text)

    def resetting_network(self):
        """重置网关"""
        if self.login_success:
            response = requests.post(self.url + "/cgi-bin/luci/admin/settings/doRestore", data={'token': self.token},
                                     cookies=self.cookies)
            return json.loads(response.text)

    def update_wifi_config(self, ssid, password):
        """修改名称密码"""
        if self.login_success:
            data = {
                "token": self.token,
                "dualBand": 0,
                "wifi_2G_SSID": ssid,  # 名称
                "wifi_2G_switch": 1,  # 开启
                "wifi_2G_strength": 3,  # 信号强度
                "wifi_2G_auth": "WPA2",
                "wifi_2G_password": password,
                "wifi_5G_SSID": "",
                "wifi_5G_switch": 1,
                "wifi_5G_strength": 3,
                "wifi_5G_auth": "Open",
                "wifi_5G_password": "",
            }
            response = requests.post(self.url + "/cgi-bin/luci/admin/settings/doRestore", data={'token': self.token},
                                     cookies=self.cookies)
            return json.loads(response.text)

    def network_timed_start(self, switch, start_time, timing_switch):
        """修改名称密码"""
        if self.login_success:
            data = {
                "token": self.token,
                "wifi_start_time": start_time,
                "wifi_end_time": timing_switch,
                "wifi_timing_switch": switch,
            }
            response = requests.post(self.url + "/cgi-bin/luci/admin/wifi/wifiAdv", data=data,
                                     cookies=self.cookies)
            print(response.text)

    def change_admin_passwd(self, new_passwd):
        """修改网关后台密码"""
        if self.login_success:
            data = {
                "token": self.token,
                "old": self.password,
                "newPasswd": new_passwd
            }
            response = requests.post(self.url + "/cgi-bin/luci/admin/settings/change_passwd", data=data,
                                     cookies=self.cookies, allow_redirects=False)
            return json.loads(response.text)

    def get_public_ip(self):
        """获取公网ip"""
        data = self.get_network_info()
        if data['WANIP']:
            return data['WANIP']
        else:
            return None
