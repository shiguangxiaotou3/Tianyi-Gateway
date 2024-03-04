# Tianyi-Gateway
快速操作电信智能网关

### Install
```bash
pip install requests
拷贝network.py
```


### Example
```python
import network
net = network.network('useradmin', '****')
net.login()
# 获取公网ip
print(net.get_public_ip())
# 获取联网设备
print(net.get_device_list())
# 获取端口映射
print(net.get_mapping_list())
# 新增端口映射
print(net.add_mapping_record( "web", "192.168.1.2", 3389, 3389)
# 定时重启
print(net.network_timed_start( 1, "6:00", "23:30")
# 修改wifi密码
print(net.update_wifi_config( "wifi-name", "pwssword"))
# 重启
net.network_reboot()
```
