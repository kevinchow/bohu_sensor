# Install on Raspberry Pi HASS 设置
  - Download image for your pi [Pi 3 or B+ recommanded]
   [Image list](https://www.home-assistant.io/hassio/installation/)
  - Download and install Etcher
   [Etcher offical link](https://etcher.io/) 
  - Burn image to the SD card
  - After Pi's status light is green and LAN port light is on go to http://hassio.local:8123
  - Go to Add-on store http://hassio.local:8123/hassio/store

### UI configuration (UI 设置)
  - Install [Configurator](https://www.home-assistant.io/getting-started/configuration/) 
  - Follow instruction and change password > click save
  - Click "start" > "Open web ui" > type in your username and password > Click top left folder icon
  - Select "configuration.yaml"
  - Add following to file
    ```
    // Add configurator to homepage slidbar
    panel_iframe:
    configurator:
      title: Configurator
      icon: mdi:wrench
      url: http://hassio.local:3218
    ```
  - Click top right icon > restart HASS
  - Go to homepage > configurator > click folder icon > click "New Folder"
  - Enter "custom_components"
  - go into "custom_components" > click folder icon > click "New Folder"
  - Enter "sensor"
  - Go into "sensor" > click folder icon > click "New File"
  - Enter "bohu.py"
  - Copy the content from bohu.py in to the editor > save
  - Update "latitude", "longitude", "elevation" in "configuration.yaml"
  - Create account in [darksky](https://darksky.net) for api key
  - Add API key to secrets.yaml
  - 添加传感器
   ```
       // [CONF_PATH]/configuration.yaml
      sensor:
        - platform: darksky
          name: Outdoor
          scan_interval: 300
          api_key: !secret darksky_apikey
          monitored_conditions:
            - temperature
            - humidity
            - wind_bearing
            - cloud_cover
            - precip_probability
            - wind_speed
        - platform: bohu
          name: Temperature
          host: 47.92.89.72
          port: 9001
          payload: '{"method":"readdata","did":"YOUR_DID_GO_HERE"}'
          scan_interval: 300
          json_attributes:
            - TEMP
            - PM25
            - PM1
            - PM10
            - CO2
            - HCHO
            - HUM
            - AQI
            - VOC
            - ILL
          value_template: '{{  value_json["TEMP"] }}'
          unit_of_measurement: "°C"
        - platform: template
          scan_interval: 300
          sensors:
            pm25:
               friendly_name: "PM2.5"
               value_template: '{{ states.sensor.Temperature.attributes.PM25 }}'
               unit_of_measurement: "ug/m³"
            pm1:
               friendly_name: "PM1"
               value_template: '{{ states.sensor.Temperature.attributes.PM1 }}'
               unit_of_measurement: "ug/m³"
            pm10:
               friendly_name: "PM10"
               value_template: '{{ states.sensor.Temperature.attributes.PM10 }}'
               unit_of_measurement: "ug/m³"
            co2:
               friendly_name: "CO2"
               value_template: '{{ states.sensor.Temperature.attributes.CO2 }}'
               unit_of_measurement: "ppm"
            hcho:
               friendly_name: "HCHO"
               value_template: '{{ states.sensor.Temperature.attributes.HCHO }}'
               unit_of_measurement: "mg/m³"
            him:
               friendly_name: "Humidity"
               value_template: '{{ states.sensor.Temperature.attributes.HUM }}'
               unit_of_measurement: "%"
            aqi:
               friendly_name: "AQI"
               value_template: '{{ states.sensor.Temperature.attributes.AQI }}'
            voc:
               friendly_name: "VOC"
               value_template: '{{ states.sensor.Temperature.attributes.VOC }}'
               unit_of_measurement: "mg/m³"
            ill:
               friendly_name: "ILL"
               value_template: '{{ states.sensor.Temperature.attributes.ILL}}'
               unit_of_measurement: "lux" 
    ```
  
### Command line configuration
  - Install [ssh server](https://www.home-assistant.io/addons/ssh/) > add ssh key
    ```
    ssh root@hassio.local
    ```
  - Change configuration
    ```
    vim /config/configuration.yaml
    ```
# 在Linux服务器上安装
  - 打开8123的防火墙点
  - 按照安装说明操作
  [安装说明](https://www.home-assistant.io/docs/installation/virtualenv/)
https://www.home-assistant.io/docs/installation/virtualenv/
 - 开始服务
   ```
   nohup hass &
   ```

# HASS 设置 LINUX
  - [CONF_PATH](https://www.home-assistant.io/docs/configuration/)
  - 改变时区
    ```
       // [CONF_PATH]/configuration.yaml
       // ~/.homeassistant/configuration.yaml <- LINUX
       time_zone: Asia/Shanghai
    ```
  - 添加传感器解析器
    ```
       // [CONF_PATH]/custom_components/sensor/bohu.py
       mkdir custom_components
       mkdir sensor
       [DOWNLOD bobu.py]
    ```
  - 添加传感器
      ```
       // [CONF_PATH]/configuration.yaml
      sensor:
        - platform: darksky
          name: Outdoor
          scan_interval: 300
          api_key: !secret darksky_apikey
          monitored_conditions:
            - temperature
            - humidity
            - wind_bearing
            - cloud_cover
            - precip_probability
            - wind_speed
        - platform: bohu
          name: Temperature
          host: 47.92.89.72
          port: 9001
          payload: '{"method":"readdata","did":"YOUR_DID_GO_HERE"}'
          scan_interval: 300
          json_attributes:
            - TEMP
            - PM25
            - PM1
            - PM10
            - CO2
            - HCHO
            - HUM
            - AQI
            - VOC
            - ILL
          value_template: '{{  value_json["TEMP"] }}'
          unit_of_measurement: "°C"
        - platform: template
          scan_interval: 300
          sensors:
            pm25:
               friendly_name: "PM2.5"
               value_template: '{{ states.sensor.Temperature.attributes.PM25 }}'
               unit_of_measurement: "ug/m³"
            pm1:
               friendly_name: "PM1"
               value_template: '{{ states.sensor.Temperature.attributes.PM1 }}'
               unit_of_measurement: "ug/m³"
            pm10:
               friendly_name: "PM10"
               value_template: '{{ states.sensor.Temperature.attributes.PM10 }}'
               unit_of_measurement: "ug/m³"
            co2:
               friendly_name: "CO2"
               value_template: '{{ states.sensor.Temperature.attributes.CO2 }}'
               unit_of_measurement: "ppm"
            hcho:
               friendly_name: "HCHO"
               value_template: '{{ states.sensor.Temperature.attributes.HCHO }}'
               unit_of_measurement: "mg/m³"
            him:
               friendly_name: "Humidity"
               value_template: '{{ states.sensor.Temperature.attributes.HUM }}'
               unit_of_measurement: "%"
            aqi:
               friendly_name: "AQI"
               value_template: '{{ states.sensor.Temperature.attributes.AQI }}'
            voc:
               friendly_name: "VOC"
               value_template: '{{ states.sensor.Temperature.attributes.VOC }}'
               unit_of_measurement: "mg/m³"
            ill:
               friendly_name: "ILL"
               value_template: '{{ states.sensor.Temperature.attributes.ILL}}'
               unit_of_measurement: "lux" 
    ```
# 在网站内检查HASS配置 
# 在网站内重启HASS 


