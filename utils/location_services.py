# utils/location_service.py
import math
import threading
from typing import Dict, Optional, Callable
from kivy.logger import Logger

try:
    # For Android
    from plyer import gps
    GPS_AVAILABLE = True
except ImportError:
    GPS_AVAILABLE = False
    Logger.warning("LocationService: GPS not available - using fallback location")

try:
    # For network-based location (fallback)
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    Logger.warning("LocationService: Requests not available - location features limited")

class LocationService:
    def __init__(self):
        self.current_location = None
        self.location_callback = None
        self.is_gps_started = False
        
        # Fallback locations for major cities (for testing/demo)
        self.fallback_locations = {
            'default': {
                'latitude': 40.7128,
                'longitude': -74.0060,
                'city': 'New York',
                'country': 'United States'
            },
            'london': {
                'latitude': 51.5074,
                'longitude': -0.1278,
                'city': 'London',
                'country': 'United Kingdom'
            },
            'tokyo': {
                'latitude': 35.6762,
                'longitude': 139.6503,
                'city': 'Tokyo',
                'country': 'Japan'
            },
            'sydney': {
                'latitude': -33.8688,
                'longitude': 151.2093,
                'city': 'Sydney',
                'country': 'Australia'
            }
        }
    
    def get_location(self, callback: Callable[[Optional[Dict]], None]):
        """Get current location using GPS or fallback methods"""
        self.location_callback = callback
        
        if GPS_AVAILABLE:
            self._try_gps_location()
        else:
            self._try_network_location()
    
    def _try_gps_location(self):
        """Try to get location using GPS"""
        try:
            if not self.is_gps_started:
                gps.configure(
                    on_location=self._on_gps_location,
                    on_status=self._on_gps_status
                )
                gps.start(minTime=1000, minDistance=1)
                self.is_gps_started = True
                Logger.info("LocationService: GPS started")
            
            # Set a timeout for GPS
            threading.Timer(10.0, self._gps_timeout).start()
            
        except Exception as e:
            Logger.error(f"LocationService: GPS error - {e}")
            self._try_network_location()
    
    def _on_gps_location(self, **kwargs):
        """GPS location callback"""
        try:
            lat = kwargs.get('lat')
            lon = kwargs.get('lon')
            
            if lat and lon:
                Logger.info(f"LocationService: GPS location - {lat}, {lon}")
                
                # Get city name from coordinates
                location_data = {
                    'latitude': lat,
                    'longitude': lon,
                    'city': 'Unknown',
                    'country': 'Unknown'
                }
                
                # Try to get city name
                self._get_city_from_coordinates(lat, lon, location_data)
            
        except Exception as e:
            Logger.error(f"LocationService: GPS location processing error - {e}")
            self._try_network_location()
    
    def _on_gps_status(self, stype, status):
        """GPS status callback"""
        Logger.info(f"LocationService: GPS status - {stype}: {status}")
    
    def _gps_timeout(self):
        """Handle GPS timeout"""
        if not self.current_location:
            Logger.warning("LocationService: GPS timeout - trying network location")
            self._try_network_location()
    
    def _try_network_location(self):
        """Try to get location using network-based services"""
        if not REQUESTS_AVAILABLE:
            self._use_fallback_location()
            return
        
        def network_request():
            try:
                # Try IP-based location service
                response = requests.get('http://ip-api.com/json/', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status') == 'success':
                        location_data = {
                            'latitude': data.get('lat'),
                            'longitude': data.get('lon'),
                            'city': data.get('city', 'Unknown'),
                            'country': data.get('country', 'Unknown')
                        }
                        
                        self.current_location = location_data
                        Logger.info(f"LocationService: Network location - {location_data['city']}")
                        
                        if self.location_callback:
                            self.location_callback(location_data)
                        return
                
            except Exception as e:
                Logger.error(f"LocationService: Network location error - {e}")
            
            # If network location fails, use fallback
            self._use_fallback_location()
        
        # Run network request in separate thread
        threading.Thread(target=network_request, daemon=True).start()
    
    def _get_city_from_coordinates(self, lat: float, lon: float, location_data: Dict):
        """Get city name from coordinates using reverse geocoding"""
        if not REQUESTS_AVAILABLE:
            self._location_found(location_data)
            return
        
        def reverse_geocode():
            try:
                # Use OpenStreetMap Nominatim for reverse geocoding
                url = f"https://nominatim.openstreetmap.org/reverse"
                params = {
                    'lat': lat,
                    'lon': lon,
                    'format': 'json',
                    'addressdetails': 1
                }
                
                response = requests.get(url, params=params, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    address = data.get('address', {})
                    
                    # Extract city and country
                    city = (address.get('city') or 
                           address.get('town') or 
                           address.get('village') or 
                           address.get('hamlet') or 'Unknown')
                    
                    country = address.get('country', 'Unknown')
                    
                    location_data.update({
                        'city': city,
                        'country': country
                    })
                    
                    Logger.info(f"LocationService: Reverse geocoding - {city}, {country}")
                
            except Exception as e:
                Logger.error(f"LocationService: Reverse geocoding error - {e}")
            
            self._location_found(location_data)
        
        # Run reverse geocoding in separate thread
        threading.Thread(target=reverse_geocode, daemon=True).start()
    
    def _location_found(self, location_data: Dict):
        """Handle successful location retrieval"""
        self.current_location = location_data
        
        if self.location_callback:
            self.location_callback(location_data)
    
    def _use_fallback_location(self):
        """Use fallback location when GPS and network fail"""
        fallback = self.fallback_locations['default']
        Logger.info(f"LocationService: Using fallback location - {fallback['city']}")
        
        self.current_location = fallback
        
        if self.location_callback:
            self.location_callback(fallback)
    
    def stop_gps(self):
        """Stop GPS if running"""
        if GPS_AVAILABLE and self.is_gps_started:
            try:
                gps.stop()
                self.is_gps_started = False
                Logger.info("LocationService: GPS stopped")
            except Exception as e:
                Logger.error(f"LocationService: Error stopping GPS - {e}")
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points using Haversine formula"""
        if not all([lat1, lon1, lat2, lon2]):
            return float('inf')
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        
        return c * r