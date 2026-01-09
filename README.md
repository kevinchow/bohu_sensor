# Instasll
  - 添加传感器解析器
    ```
       // [CONF_PATH]/custom_components/sensor/bohu.py
       mkdir custom_components
       mkdir sensor
       [DOWNLOD bobu.py, __init__.py, manifest.json]
    ```
  - 添加传感器
    ```
    # =========================
    # TCP AIR QUALITY SENSOR
    # =========================
    sensor:
      - platform: bohu
        name: Living Room CO2
        host: 47.92.89.72
        port: 9001
        payload: '{"method":"readdata","did":"CHANG_TO_YOUR_ID"}'
        scan_interval: 300
        unit_of_measurement: ppm
    
    # =========================
    # TEMPLATE SENSORS
    # =========================
    template:
      - sensor:
          # --- CO2 ---
          - name: "Living Room CO2"
            state: "{{ states('sensor.living_room_co2') }}"
            unit_of_measurement: "ppm"
            device_class: carbon_dioxide
            state_class: measurement
    
          # --- PM ---
          - name: "Living Room PM1"
            state: "{{ state_attr('sensor.living_room_co2', 'pm1') }}"
            unit_of_measurement: "µg/m³"
            state_class: measurement
    
          - name: "Living Room PM2.5"
            state: "{{ state_attr('sensor.living_room_co2', 'pm25') }}"
            unit_of_measurement: "µg/m³"
            state_class: measurement
    
          - name: "Living Room PM10"
            state: "{{ state_attr('sensor.living_room_co2', 'pm10') }}"
            unit_of_measurement: "µg/m³"
            state_class: measurement
    
          # --- ENV ---
          - name: "Living Room Temperature"
            state: "{{ state_attr('sensor.living_room_co2', 'temperature') }}"
            unit_of_measurement: "°C"
            device_class: temperature
            state_class: measurement
    
          - name: "Living Room Humidity"
            state: "{{ state_attr('sensor.living_room_co2', 'humidity') }}"
            unit_of_measurement: "%"
            device_class: humidity
            state_class: measurement
    
          # --- AIR QUALITY ---
          - name: "Living Room AQI"
            state: "{{ state_attr('sensor.living_room_co2', 'aqi') }}"
            state_class: measurement
    
          - name: "Living Room VOC"
            state: "{{ state_attr('sensor.living_room_co2', 'voc') }}"
            unit_of_measurement: "mg/m³"
            state_class: measurement
    
          - name: "Living Room HCHO"
            state: "{{ state_attr('sensor.living_room_co2', 'hcho') }}"
            unit_of_measurement: "mg/m³"
            state_class: measurement  
    ```



