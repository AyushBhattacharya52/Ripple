# utils/app_config.py - Configuration for production deployment
import os
from typing import Dict, Any

class AppConfig:
    """Configuration management for Ripple Events app"""
    
    # App Information
    APP_NAME = "Ripple Events"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Discover and create local events in your community"
    
    # Performance Settings
    MAX_EVENTS_PER_LOAD = 50
    LOCATION_UPDATE_INTERVAL = 300  # 5 minutes
    CACHE_EXPIRY_TIME = 600  # 10 minutes
    DEFAULT_SEARCH_RADIUS = 50  # kilometers
    
    # Data Limits
    MAX_EVENT_TITLE_LENGTH = 100
    MAX_EVENT_DESCRIPTION_LENGTH = 1000
    MAX_EVENTS_PER_USER = 10
    MAX_PARTICIPANTS_PER_EVENT = 500
    
    # Location Settings
    ENABLE_GPS = True
    ENABLE_NETWORK_LOCATION = True
    GPS_TIMEOUT = 15  # seconds
    LOCATION_ACCURACY_THRESHOLD = 1000  # meters
    
    # Storage Settings
    DATA_RETENTION_DAYS = 365
    AUTO_CLEANUP_ENABLED = True
    MAX_DATA_SIZE_MB = 100
    
    # Security Settings
    PASSWORD_MIN_LENGTH = 6
    SESSION_TIMEOUT = 3600  # 1 hour
    ENABLE_DATA_ENCRYPTION = False  # Set to True for production
    
    # UI Settings
    THEME_PRIMARY_COLOR = (0.3, 0.4, 0.8, 1)  # Blue
    THEME_SECONDARY_COLOR = (0.2, 0.7, 0.5, 1)  # Green
    THEME_ACCENT_COLOR = (1, 0.6, 0.2, 1)  # Orange
    ANIMATION_DURATION = 0.3
    
    # Feature Flags
    ENABLE_PUSH_NOTIFICATIONS = True
    ENABLE_SOCIAL_SHARING = True
    ENABLE_EVENT_CHAT = False  # Future feature
    ENABLE_PAYMENT_INTEGRATION = False  # Future feature
    ENABLE_ANALYTICS = True
    
    # API Settings (for future backend integration)
    API_BASE_URL = ""
    API_TIMEOUT = 30
    ENABLE_OFFLINE_MODE = True
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        config = {}
        for attr in dir(cls):
            if not attr.startswith('_') and not callable(getattr(cls, attr)):
                config[attr] = getattr(cls, attr)
        return config
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment"""
        return os.environ.get('RIPPLE_ENV') == 'production'
    
    @classmethod
    def get_data_dir(cls) -> str:
        """Get data directory path"""
        if cls.is_production():
            # Use app-specific data directory in production
            return os.path.join(os.path.expanduser('~'), '.ripple_events')
        else:
            return 'data'
    
    @classmethod
    def get_log_level(cls) -> str:
        """Get logging level"""
        return 'INFO' if cls.is_production() else 'DEBUG'

# App Store Metadata
APP_STORE_CONFIG = {
    'ios': {
        'bundle_id': 'com.rippleevents.app',
        'team_id': 'YOUR_TEAM_ID',
        'version': AppConfig.APP_VERSION,
        'build': '1',
        'minimum_ios_version': '12.0',
        'supported_devices': ['iphone', 'ipad'],
        'categories': ['lifestyle', 'social_networking'],
        'keywords': ['events', 'local', 'community', 'social', 'meetup'],
        'privacy_url': 'https://your-website.com/privacy',
        'support_url': 'https://your-website.com/support'
    },
    'android': {
        'package_name': 'com.rippleevents.app',
        'version_code': 1,
        'version_name': AppConfig.APP_VERSION,
        'min_sdk_version': 21,  # Android 5.0
        'target_sdk_version': 33,  # Android 13
        'compile_sdk_version': 33,
        'categories': ['SOCIAL', 'LIFESTYLE'],
        'permissions': [
            'ACCESS_FINE_LOCATION',
            'ACCESS_COARSE_LOCATION',
            'INTERNET',
            'ACCESS_NETWORK_STATE',
            'WRITE_EXTERNAL_STORAGE',
            'READ_EXTERNAL_STORAGE'
        ],
        'features': [
            'android.hardware.location',
            'android.hardware.location.gps'
        ]
    }
}

# Performance monitoring configuration
PERFORMANCE_CONFIG = {
    'enable_monitoring': True,
    'track_screen_time': True,
    'track_user_interactions': True,
    'track_crashes': True,
    'track_performance_metrics': True,
    'sample_rate': 0.1 if AppConfig.is_production() else 1.0
}

# Privacy and GDPR compliance
PRIVACY_CONFIG = {
    'enable_data_collection': True,
    'enable_crash_reporting': True,
    'enable_analytics': True,
    'data_retention_days': 365,
    'allow_data_export': True,
    'allow_data_deletion': True,
    'require_consent': True,
    'privacy_policy_url': 'https://your-website.com/privacy',
    'terms_of_service_url': 'https://your-website.com/terms'
}

# Monetization configuration (for future use)
MONETIZATION_CONFIG = {
    'enable_ads': False,
    'enable_premium_features': False,
    'enable_in_app_purchases': False,
    'premium_price_usd': 4.99,
    'ad_frequency': 0,  # ads per session
    'premium_features': [
        'unlimited_events',
        'advanced_search',
        'event_analytics',
        'custom_themes'
    ]
}