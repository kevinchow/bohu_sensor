# 在Linux服务器上安装
  - 打开8123的防火墙点
  - 按照安装说明操作
  [安装说明](https://www.home-assistant.io/docs/installation/virtualenv/)
https://www.home-assistant.io/docs/installation/virtualenv/
 - 开始服务
   ```
   nohup hass &
   ```

# HASS 设置
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


