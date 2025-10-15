"""
NWS API client for fetching weather alerts.
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .constants import NWS_API_BASE_URL, NWS_ALERTS_ENDPOINT, DEFAULT_HEADERS
from .exceptions import APIError, NetworkError, TimeoutError
from .data_types import CountyCode


class NWSAPIClient:
    """Client for interacting with the National Weather Service API."""
    
    def __init__(self, timeout: int = 10, max_workers: int = 10):
        """Initialize the API client."""
        self.timeout = timeout
        self.max_workers = max_workers
        self.logger = logging.getLogger(__name__)
        self._session: Optional[requests.Session] = None
    
    def _get_session(self) -> requests.Session:
        """Get or create HTTP session with optimizations."""
        if self._session is None:
            self._session = requests.Session()
            
            # Configure retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            
            adapter = HTTPAdapter(
                max_retries=retry_strategy,
                pool_connections=20,
                pool_maxsize=20
            )
            
            self._session.mount("http://", adapter)
            self._session.mount("https://", adapter)
            
            # Set default headers
            self._session.headers.update(DEFAULT_HEADERS)
        
        return self._session
    
    def fetch_county_alerts(self, county_code: CountyCode) -> Tuple[CountyCode, Optional[Dict]]:
        """Fetch alerts for a single county using modern NWS API practices."""
        # Use the modern alerts endpoint with proper parameters
        url = f"{NWS_API_BASE_URL}{NWS_ALERTS_ENDPOINT}"
        params = {
            'zone': county_code,
            'status': 'actual',      # Only get actual alerts, not test alerts
            'message_type': 'alert'  # Only get alert messages, not updates
        }
        
        try:
            session = self._get_session()
            response = session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            # Check for rate limiting
            if response.status_code == 429:
                self.logger.warning(f"Rate limited for {county_code}, retrying with backoff")
                time.sleep(1)
                response = session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
            
            self.logger.debug(
                "Checking for alerts in %s at URL: %s", 
                county_code, 
                response.url
            )
            
            data = response.json()
            
            # Validate response structure
            if not isinstance(data, dict) or 'features' not in data:
                self.logger.error(f"Invalid response structure for {county_code}")
                return county_code, None
                
            return county_code, data
            
        except requests.exceptions.Timeout:
            self.logger.error(f"Timeout fetching alerts for {county_code}")
            return county_code, None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {county_code}: {e}")
            return county_code, None
        except Exception as e:
            self.logger.error(f"Unexpected error fetching alerts for {county_code}: {e}")
            return county_code, None
    
    def fetch_alerts_for_counties(self, county_codes: List[CountyCode]) -> Dict[CountyCode, Optional[Dict]]:
        """Fetch alerts for multiple counties concurrently."""
        alerts_data = {}
        
        # Use ThreadPoolExecutor for concurrent requests
        with ThreadPoolExecutor(max_workers=min(len(county_codes), self.max_workers)) as executor:
            # Submit all requests concurrently
            future_to_county = {
                executor.submit(self.fetch_county_alerts, county_code): county_code
                for county_code in county_codes
            }
            
            # Process completed requests
            for future in as_completed(future_to_county):
                county_code, data = future.result()
                alerts_data[county_code] = data
        
        return alerts_data
    
    def close(self):
        """Close the HTTP session."""
        if self._session:
            self._session.close()
            self._session = None
