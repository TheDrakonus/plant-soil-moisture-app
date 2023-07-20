import os
from peewee import *

DB_PATH = os.path.join(os.path.dirname(__file__), "./db_data/", 'db.sqlite3')
print(DB_PATH)
db = SqliteDatabase(DB_PATH)

class BaseModel(Model):
    class Meta:
        database = db

class Device(BaseModel):
    name = CharField()
    ip = CharField()
    mac = CharField()
    last_seen = DateTimeField()

class DeviceLog(BaseModel):
    device = ForeignKeyField(Device, backref='logs')
    timestamp = DateTimeField()
    action = CharField()

class DeviceSensorLog(BaseModel):
    device = ForeignKeyField(Device, backref='sensor_readings')
    timestamp = DateTimeField()

class TemperatureMoistureLog(DeviceSensorLog):
    temperature_celcius = FloatField()
    moisture = FloatField()


class MoistureLog(BaseModel):
    device = ForeignKeyField(Device, backref='moisture_logs')
    timestamp = DateTimeField()
    moisture = FloatField()

class TemperatureLog(BaseModel):
    device = ForeignKeyField(Device, backref='temperature_logs')
    timestamp = DateTimeField()
    temperature_celcius = FloatField()

class Database:
    def __init__(self):
        self.db = db
        self.db.connect()
        self.db.create_tables([Device, DeviceLog, TemperatureMoistureLog])
        self.db.close()
    
    def get_devices(self):      
        devices = []
        for device in Device.select():
            devices.append({
                'id': device.id,
                'name': device.name,
                'ip': device.ip,
                'mac': device.mac,
                'last_seen': device.last_seen
            })
        return devices
    
    def get_device_sensor_data(self, device_id):    
        try:
            device = Device.get_by_id(device_id)
        except DoesNotExist:
            device = None
        if device is None:
            return None
        return {
            'id': device.id,
            'name': device.name,
            'last_seen': device.last_seen,
            'moisture_logs': [{
                'timestamp': log.timestamp,
                'moisture': log.moisture
            } for log in device.moisture_logs],
            'temperature_logs': [{
                'timestamp': log.timestamp,
                'temperature_celcius': log.temperature_celcius
            } for log in device.temperature_logs]
        }
    
    def get_device_by_id(self, device_id):
        try:
            device = Device.get_by_id(device_id)
        except DoesNotExist:
            device = None
        return device
    
    def get_device_by_mac(self, mac):
        try:
            device = Device.get(Device.mac == mac)
        except DoesNotExist:
            device = None
        return device   

    def get_temperure_moisture_logs(self, device):
        logs = []
        for log in TemperatureMoistureLog.select().where(TemperatureMoistureLog.device == device):
            logs.append({
                'timestamp': log.timestamp,
                'temperature_celcius': log.temperature_celcius,
                'moisture': log.moisture
            })
        return logs


if __name__ == '__main__':
    def fill_sample_data(db):
        with db as conn: 
            conn.drop_tables([Device, DeviceLog, TemperatureMoistureLog])
            conn.create_tables([Device, DeviceLog, TemperatureMoistureLog])

            device_1 = Device.create(name='Device 1', ip='192.168.0.1', mac='00:00:00:00:00:00', last_seen='2021-01-01 00:00:00')
            device_2 = Device.create(name='Device 2', ip='192.168.0.2', mac='00:00:00:00:00:01', last_seen='2021-01-01 00:00:00')

            DeviceLog.create(device=device_1, timestamp='2021-01-01 00:00:00', action='connected')
            DeviceLog.create(device=device_1, timestamp='2021-01-01 00:00:01', action='disconnected')
            DeviceLog.create(device=device_2, timestamp='2021-01-01 00:00:02', action='connected')
            DeviceLog.create(device=device_2, timestamp='2021-01-01 00:00:03', action='disconnected')
            DeviceLog.create(device=device_2, timestamp='2021-01-01 00:00:04', action='connected')
            DeviceLog.create(device=device_2, timestamp='2021-01-01 00:00:05', action='disconnected')

            TemperatureMoistureLog.create(device=device_1, timestamp='2021-01-01 00:00:00', temperature_celcius=20.0, moisture=0.5)
            TemperatureMoistureLog.create(device=device_1, timestamp='2021-01-01 00:00:01', temperature_celcius=20.1, moisture=0.6)
            TemperatureMoistureLog.create(device=device_1, timestamp='2021-01-01 00:00:02', temperature_celcius=20.2, moisture=0.7)
            TemperatureMoistureLog.create(device=device_1, timestamp='2021-01-01 00:00:03', temperature_celcius=20.3, moisture=0.8)
            TemperatureMoistureLog.create(device=device_1, timestamp='2021-01-01 00:00:04', temperature_celcius=20.4, moisture=0.9)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:05', temperature_celcius=20.5, moisture=1.0)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:06', temperature_celcius=20.6, moisture=1.1)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:07', temperature_celcius=20.7, moisture=1.2)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:08', temperature_celcius=20.8, moisture=1.3)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:09', temperature_celcius=20.9, moisture=1.4)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:10', temperature_celcius=21.0, moisture=1.5)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:11', temperature_celcius=21.1, moisture=1.6)
            TemperatureMoistureLog.create(device=device_2, timestamp='2021-01-01 00:00:12', temperature_celcius=21.2, moisture=1.7)

    fill_sample_data(db)
