from flask import Flask, request, jsonify
from apiclient.discovery import build
import os
from typing import Any, List, Dict

API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("No API_KEY set for Google Trends API")
SERVER = 'https://trends.googleapis.com'
API_VERSION = 'v1beta'
DISCOVERY_URL_SUFFIX = '/$discovery/rest?version=' + API_VERSION
DISCOVERY_URL = SERVER + DISCOVERY_URL_SUFFIX
MAX_QUERIES = 30


class Timeline:
    def __init__(self):
        self.service = self.get_client()
    
    def get_client(self) -> Any:
        return build('trends', API_VERSION, developerKey=API_KEY,
                     discoveryServiceUrl=DISCOVERY_URL)

    def get_search_volumes(
        self,
        terms: List[str], 
        start_date: str, 
        end_date: str, 
        frequency: str,
        geo_restriction: str,
        geo_restriction_option: str
    ) -> List[Dict[str, Any]]:
        if geo_restriction == 'country':
            req = self.service.getTimelinesForHealth(
                terms=terms, time_startDate=start_date,
                time_endDate=end_date,
                timelineResolution=frequency,
                geoRestriction_country=geo_restriction_option
            )
        elif geo_restriction == 'dma':
            req = self.service.getTimelinesForHealth(
                terms=terms,
                time_startDate=start_date,
                time_endDate=end_date,
                timelineResolution=frequency,
                geoRestriction_dma=geo_restriction_option
            )
        elif geo_restriction == 'region':
            req = self.service.getTimelinesForHealth(
                terms=terms,
                time_startDate=start_date,
                time_endDate=end_date,
                timelineResolution=frequency,
                geoRestriction_region=geo_restriction_option
            )

        response = req.execute()
        
        timeline_data = response.get('lines', [])
        
        data = []
        for line in timeline_data:
            term = line['term']
            for point in line['points']:
                data.append({
                    'term': term,
                    'date': point['date'],
                    'value': point['value']
                })
        
        return data
