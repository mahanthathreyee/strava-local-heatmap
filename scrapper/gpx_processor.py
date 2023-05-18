from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt

class GPXProcessor:
    ET.register_namespace("", "http://www.topografix.com/GPX/1/1")
    
    def __init__(self, file_path, start_time, km_splits):
        self.file_path = file_path
        self.start_time = start_time
        self.km_splits = km_splits
        self.tree, self.trkpts = self.read_gpx_file(self.file_path)
    
    @staticmethod
    def read_gpx_file(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        trkpts = root.findall(".//{http://www.topografix.com/GPX/1/1}trkpt")
        return tree, trkpts

    @staticmethod
    def haversine(lon1, lat1, lon2, lat2):
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 
        return c * r * 1000

    @staticmethod
    def add_seconds_to_time(iso_time, seconds):
        time_obj = datetime.fromisoformat(iso_time.replace("Z", "+00:00"))
        new_time_obj = time_obj + timedelta(seconds=seconds)
        return new_time_obj.isoformat().replace("+00:00", "Z")

    def add_time_data_to_gpx(self):
        current_time = self.start_time
        total_distance = 0
        km_distance = 0
        points_in_current_km = []
        gpx_points_per_km = {}
        
        for i in range(len(self.trkpts)):
            if i != 0:
                lat1, lon1 = map(float, (self.trkpts[i-1].attrib["lat"], self.trkpts[i-1].attrib["lon"]))
                lat2, lon2 = map(float, (self.trkpts[i].attrib["lat"], self.trkpts[i].attrib["lon"]))
                distance = self.haversine(lon1, lat1, lon2, lat2)
                total_distance += distance
                km_distance += distance

            points_in_current_km.append(self.trkpts[i])

            if km_distance >= 1000 or i == len(self.trkpts) - 1:
                km_number = int(total_distance // 1000)
                gpx_points_per_km[km_number] = points_in_current_km
                points_in_current_km = []
                km_distance %= 1000

        for km_number, points_in_current_km in gpx_points_per_km.items():
            split_time = self.km_splits.get(km_number)
            if split_time is not None:
                minutes, seconds = map(int, split_time.split(":"))
                time_to_add = minutes * 60 + seconds
                time_increment = time_to_add / len(points_in_current_km)
                for _, point in enumerate(points_in_current_km):
                    current_time = self.add_seconds_to_time(current_time, time_increment)
                    time_elem = ET.Element("{http://www.topografix.com/GPX/1/1}time")
                    time_elem.text = current_time
                    point.append(time_elem)

    def write_gpx_file(self, output_file_path):
        self.tree.write(output_file_path, default_namespace='')

#Usage
start_time = "2023-05-07T08:16:00Z"
km_splits = {
    1: "05:37",
    2: "04:45",
    3: "05:22",
    4: "05:19",
    5: "04:45",
    6: "04:43",
    7: "04:45",
    8: "04:49",
    9: "04:24",
    10: "04:34",
    0.25: "7.22"
}

gpx_processor = GPXProcessor("gpx_without_timestamp_2.gpx", start_time, km_splits)
gpx_processor.add_time_data_to_gpx()
gpx_processor.write_gpx_file("gpx_with_timestamps_2.gpx")

