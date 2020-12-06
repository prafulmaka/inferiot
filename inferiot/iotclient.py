import pandas as pd
import requests
import datetime


class client(object):
    
    """
    This object class is used to interact with the SmartHub Infer IoT Center. 
    The SmartHub Infer IoT Center provides programmable REST APIs to integrate with your existing enterprise solution. 
    With this API facade, you can view various SmartHub Infer IoT devices, audit logs, notifications, device templates and metrics programmatically using Python.
    
    """
    
    # Import required libraries
    import requests 
    import pandas
    import datetime
    
    
    def __init__(self, url, username, password):
        
            self._url = url
            self._api_version = requests.get(self._url+'/api/versions').json()['currentApiVersion']
            self._header = {'Accept':'Application/json;api-version='+self._api_version,
                            'Content-Type': 'application/json'}
            self._token = requests.get(url+"/api/tokens", headers=self._header, auth=(username,password)).json()['accessToken']
            self._auth_headers = {'Authorization': f'Bearer {self._token}',**self._header}
        
        
    def get_devices(self, deviceid=None):
        
            """ 
            Gets a list of enrolled devices or a specific device using its deviceid.
            
            Parameters
            ----------
            deviceid : unique identification of the device entity in the Infer IoT Center
            
            """
            
            if deviceid is None:
                deviceid = ''
                print("These are all the enrolled devices:")
            
            device_info =  requests.get(self._url+'/api/devices/'+ deviceid, headers=self._auth_headers)
            return device_info.json()
            
    
    def get_audit_logs(self):
        
            """
            Gets audit logs for all enrolled devices.
            
            """
            
            device_logs = requests.get(self._url+'/api/audit-logs/', headers=self._auth_headers)
            return device_logs.json()
        
        
    def get_notifications(self, deviceid=None):
        
            """
            Gets a list of notifications for a specific deviceid.
            
            Parameters
            ----------
            deviceid : unique identification of the device entity in the Infer IoT Center
            
            """
        
            if deviceid is None:
                deviceid = ''
                
            notifications = requests.get(self._url+'/api/notification-definitions/'+ deviceid, headers=self._auth_headers)
            return notifications.json()
        
        
    def get_device_template(self, deviceid=None):
        
            """
            Gets the device template for a specific deviceid.
            The device template is the blueprint of the device that is to be registered on the SmartHub Infer IoT Center.
            This function can be used to view the the allowed metrics for a specific deviceid. 
            
            Parameters
            ----------
            deviceid : unique identification of the device entity in the Infer IoT Center
            
            """
            
            # This is the list of valid gateway device ids:
            valid_deviceids = ['b8744dac-d304-488e-aa01-51cb1c8b0c48', '464cd6fb-3b9c-4acc-bc89-295816a09bf2', 'cd9b0408-52a1-406d-88d8-90c6ddb33d03']
            
            if deviceid not in valid_deviceids:
                print("This is not a valid Gateway deviceid")
                
            else:
            
                device_template = requests.get(self._url+'/api/device-templates', headers=self._auth_headers)
                template = device_template.json()

                for temps in template['templates']:
                    if temps['id'] == deviceid:
                        print(pd.DataFrame(data = temps['allowedMetrics']))
                        
        
    def get_metrics(self, deviceid=None, metric=None, start_time=None, end_time=None):
            
            """
            Gets the device time series metric data by deviceid, metric name and time range. 
            This function can be used to query metrics for a specific deviceid.
            
            Parameters
            ----------
            deviceid : unique identification of the device entity in the Infer IoT Center
            metric : metric name for the time series data for a particular metric
            start_time : start time in milliseconds
            end_time : end time in milliseconds
            
            """
            
            device_metrics = requests.get(self._url+'/api/metrics/{0}/{1}?start_time_ms={2}&end_time_ms={3}'.format(deviceid, metric, start_time, end_time), headers=self._auth_headers)
            data = device_metrics.json()
            # Convert to dataframe    
            frame = pd.DataFrame(data['metricData']['tsData'])
            # Rename columns 
            frame.columns = [list(data['metricData']['tsData'][0].keys())[0],data['metricData']['name']]
                        
            # Convert epoch milliseconds to human-readable
            pdt_format = pd.to_datetime(frame['timeMs'], unit='ms')
            frame['timestamp'] = pdt_format+pd.Timedelta('-8:00:00')
            frame = frame[['timestamp', 'CPU-Utilization(DOUBLE)']]
    
            return frame
    
        # Use client('https://inst01.us01.infer.smarthub.ai','<Your Username>','<Your Password>')

        
