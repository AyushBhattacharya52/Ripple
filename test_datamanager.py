import json
import time
from datetime import datetime, timedelta
from utils.data_manager import DataManager

class DatabaseTestSuite:
    def __init__(self):
        self.dm = DataManager()
        self.test_results = []
        self.test_users = []
        self.test_events = []
        
    def log_test(self, test_name, success, message="", data=None):
        """Log test results for detailed reporting"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        
    def test_user_registration(self):
        """Test user registration with various scenarios"""
        print("\n=== TESTING USER REGISTRATION ===")
        
        # Test valid user registration
        test_users = [
            {
                "username": "alice_smith",
                "email": "alice@example.com",
                "password": "SecurePass123!",
                "full_name": "Alice Smith",
                "bio": "Software developer passionate about tech events"
            },
            {
                "username": "bob_johnson",
                "email": "bob.johnson@company.com",
                "password": "MyPassword456#",
                "full_name": "Bob Johnson",
                "bio": "Marketing manager and event organizer"
            },
            {
                "username": "charlie_dev",
                "email": "charlie@startup.io",
                "password": "DevLife789$",
                "full_name": "Charlie Wilson",
                "bio": "Full-stack developer and community builder"
            }
        ]
        
        for user_data in test_users:
            try:
                success = self.dm.register_user(user_data)
                if success:
                    self.test_users.append(user_data["username"])
                self.log_test(
                    f"Register user: {user_data['username']}", 
                    success, 
                    f"User registration {'successful' if success else 'failed'}",
                    user_data
                )
            except Exception as e:
                self.log_test(f"Register user: {user_data['username']}", False, str(e))
        
        # Test duplicate registration
        try:
            duplicate_user = test_users[0].copy()
            success = self.dm.register_user(duplicate_user)
            self.log_test(
                "Duplicate user registration", 
                not success, 
                "Should prevent duplicate registrations"
            )
        except Exception as e:
            self.log_test("Duplicate user registration", True, f"Correctly rejected: {str(e)}")
    
    def test_user_authentication(self):
        """Test user sign-in with valid and invalid credentials"""
        print("\n=== TESTING USER AUTHENTICATION ===")
        
        # Test valid login
        test_credentials = [
            {"username": "alice_smith", "password": "SecurePass123!"},
            {"email": "bob.johnson@company.com", "password": "MyPassword456#"}
        ]
        
        for creds in test_credentials:
            try:
                user = self.dm.authenticate_user(creds)
                success = user is not None
                self.log_test(
                    f"Login: {creds.get('username', creds.get('email'))}", 
                    success,
                    f"Authentication {'successful' if success else 'failed'}",
                    {"user_id": user.get("id") if user else None}
                )
            except Exception as e:
                self.log_test(f"Login: {creds.get('username', creds.get('email'))}", False, str(e))
        
        # Test invalid login
        invalid_credentials = [
            {"username": "alice_smith", "password": "WrongPassword"},
            {"username": "nonexistent_user", "password": "AnyPassword123"},
            {"email": "fake@email.com", "password": "FakePass456"}
        ]
        
        for creds in invalid_credentials:
            try:
                user = self.dm.authenticate_user(creds)
                success = user is None
                self.log_test(
                    f"Invalid login: {creds.get('username', creds.get('email'))}", 
                    success,
                    "Should reject invalid credentials"
                )
            except Exception as e:
                self.log_test(f"Invalid login: {creds.get('username', creds.get('email'))}", True, f"Correctly rejected: {str(e)}")

    def test_event_creation(self):
        """Test creating events with various scenarios"""
        print("\n=== TESTING EVENT CREATION ===")
        
        # Generate test events with different categories and dates
        base_date = datetime.now() + timedelta(days=1)
        test_events = [
            {
                "title": "Python Workshop for Beginners",
                "description": "Learn Python basics with hands-on coding exercises. Perfect for newcomers to programming.",
                "date": (base_date + timedelta(days=7)).strftime("%Y-%m-%d"),
                "time": "14:00",
                "location": "Tech Hub Downtown, Room 301",
                "category": "Technology",
                "max_participants": 25,
                "creator_id": "alice_smith",
                "creator_name": "Alice Smith"
            },
            {
                "title": "Digital Marketing Strategies 2025",
                "description": "Explore the latest trends in digital marketing, including AI-powered campaigns and social media strategies.",
                "date": (base_date + timedelta(days=14)).strftime("%Y-%m-%d"),
                "time": "10:00",
                "location": "Business Center, Conference Room A",
                "category": "Business",
                "max_participants": 50,
                "creator_id": "bob_johnson",
                "creator_name": "Bob Johnson"
            },
            {
                "title": "Community Coffee Chat",
                "description": "Casual networking event for local professionals. Come meet new people and share ideas over coffee.",
                "date": (base_date + timedelta(days=3)).strftime("%Y-%m-%d"),
                "time": "09:00",
                "location": "Central Café, Main Street",
                "category": "Networking",
                "max_participants": 30,
                "creator_id": "charlie_dev",
                "creator_name": "Charlie Wilson"
            },
            {
                "title": "React.js Advanced Patterns",
                "description": "Deep dive into advanced React patterns including hooks, context, and performance optimization.",
                "date": (base_date + timedelta(days=21)).strftime("%Y-%m-%d"),
                "time": "18:30",
                "location": "Innovation Lab, Building B",
                "category": "Technology",
                "max_participants": 20,
                "creator_id": "charlie_dev",
                "creator_name": "Charlie Wilson"
            },
            {
                "title": "Startup Pitch Night",
                "description": "Watch local entrepreneurs pitch their innovative ideas to a panel of investors and mentors.",
                "date": (base_date + timedelta(days=28)).strftime("%Y-%m-%d"),
                "time": "19:00",
                "location": "Entrepreneur Center Auditorium",
                "category": "Business",
                "max_participants": 100,
                "creator_id": "alice_smith",
                "creator_name": "Alice Smith"
            }
        ]
        
        for event_data in test_events:
            try:
                success = self.dm.create_event(event_data)
                if success:
                    self.test_events.append(event_data["title"])
                self.log_test(
                    f"Create event: {event_data['title']}", 
                    success,
                    f"Event creation {'successful' if success else 'failed'}",
                    event_data
                )
            except Exception as e:
                self.log_test(f"Create event: {event_data['title']}", False, str(e))
        
        # Test event with missing required fields
        try:
            incomplete_event = {
                "title": "Incomplete Event",
                "description": "Missing required fields"
                # Missing date, time, location, etc.
            }
            success = self.dm.create_event(incomplete_event)
            self.log_test(
                "Incomplete event creation", 
                not success, 
                "Should reject events with missing fields"
            )
        except Exception as e:
            self.log_test("Incomplete event creation", True, f"Correctly rejected: {str(e)}")

    def test_event_retrieval(self):
        """Test various event retrieval methods"""
        print("\n=== TESTING EVENT RETRIEVAL ===")
        
        # Test getting all events
        try:
            events = self.dm.get_all_events()
            success = isinstance(events, list)
            self.log_test(
                "Get all events", 
                success,
                f"Retrieved {len(events) if success else 0} events",
                {"count": len(events) if success else 0}
            )
        except Exception as e:
            self.log_test("Get all events", False, str(e))
        
        # Test getting events by category
        categories = ["Technology", "Business", "Networking"]
        for category in categories:
            try:
                events = self.dm.get_events_by_category(category)
                success = isinstance(events, list)
                self.log_test(
                    f"Get events by category: {category}", 
                    success,
                    f"Retrieved {len(events) if success else 0} {category} events",
                    {"category": category, "count": len(events) if success else 0}
                )
            except Exception as e:
                self.log_test(f"Get events by category: {category}", False, str(e))
        
        # Test getting events by creator
        for creator_id in ["alice_smith", "bob_johnson", "charlie_dev"]:
            try:
                events = self.dm.get_events_by_creator(creator_id)
                success = isinstance(events, list)
                self.log_test(
                    f"Get events by creator: {creator_id}", 
                    success,
                    f"Retrieved {len(events) if success else 0} events by {creator_id}",
                    {"creator": creator_id, "count": len(events) if success else 0}
                )
            except Exception as e:
                self.log_test(f"Get events by creator: {creator_id}", False, str(e))

    def test_event_registration(self):
        """Test user registration for events"""
        print("\n=== TESTING EVENT REGISTRATION ===")
        
        # Get some events to register for
        try:
            events = self.dm.get_all_events()
            if not events:
                self.log_test("Event registration setup", False, "No events available for registration testing")
                return
            
            # Test successful registrations
            registration_tests = [
                {"user_id": "alice_smith", "event_id": events[0].get("id"), "event_title": events[0].get("title")},
                {"user_id": "bob_johnson", "event_id": events[0].get("id"), "event_title": events[0].get("title")},
                {"user_id": "charlie_dev", "event_id": events[1].get("id") if len(events) > 1 else events[0].get("id"), 
                 "event_title": events[1].get("title") if len(events) > 1 else events[0].get("title")},
            ]
            
            for reg_test in registration_tests:
                try:
                    success = self.dm.register_for_event(reg_test["user_id"], reg_test["event_id"])
                    self.log_test(
                        f"Event registration: {reg_test['user_id']} -> {reg_test['event_title']}", 
                        success,
                        f"Registration {'successful' if success else 'failed'}",
                        reg_test
                    )
                except Exception as e:
                    self.log_test(f"Event registration: {reg_test['user_id']} -> {reg_test['event_title']}", False, str(e))
            
            # Test duplicate registration
            try:
                success = self.dm.register_for_event("alice_smith", events[0].get("id"))
                self.log_test(
                    "Duplicate event registration", 
                    not success, 
                    "Should prevent duplicate registrations"
                )
            except Exception as e:
                self.log_test("Duplicate event registration", True, f"Correctly rejected: {str(e)}")
                
        except Exception as e:
            self.log_test("Event registration setup", False, str(e))

    def test_user_event_queries(self):
        """Test querying user's events and registrations"""
        print("\n=== TESTING USER EVENT QUERIES ===")
        
        # Test getting user's created events
        for user_id in ["alice_smith", "bob_johnson", "charlie_dev"]:
            try:
                created_events = self.dm.get_user_created_events(user_id)
                success = isinstance(created_events, list)
                self.log_test(
                    f"Get created events: {user_id}", 
                    success,
                    f"User has created {len(created_events) if success else 0} events",
                    {"user_id": user_id, "created_count": len(created_events) if success else 0}
                )
            except Exception as e:
                self.log_test(f"Get created events: {user_id}", False, str(e))
        
        # Test getting user's registered events
        for user_id in ["alice_smith", "bob_johnson", "charlie_dev"]:
            try:
                registered_events = self.dm.get_user_registered_events(user_id)
                success = isinstance(registered_events, list)
                self.log_test(
                    f"Get registered events: {user_id}", 
                    success,
                    f"User is registered for {len(registered_events) if success else 0} events",
                    {"user_id": user_id, "registered_count": len(registered_events) if success else 0}
                )
            except Exception as e:
                self.log_test(f"Get registered events: {user_id}", False, str(e))

    def test_event_updates(self):
        """Test updating event information"""
        print("\n=== TESTING EVENT UPDATES ===")
        
        try:
            events = self.dm.get_all_events()
            if not events:
                self.log_test("Event update setup", False, "No events available for update testing")
                return
            
            # Test updating event details
            event_to_update = events[0]
            update_data = {
                "title": f"UPDATED: {event_to_update.get('title')}",
                "description": f"{event_to_update.get('description')} - This event has been updated with new information!",
                "max_participants": event_to_update.get('max_participants', 50) + 10
            }
            
            success = self.dm.update_event(event_to_update.get('id'), update_data)
            self.log_test(
                f"Update event: {event_to_update.get('title')}", 
                success,
                f"Event update {'successful' if success else 'failed'}",
                update_data
            )
            
        except Exception as e:
            self.log_test("Event update test", False, str(e))

    def test_event_cancellation(self):
        """Test event cancellation/deletion"""
        print("\n=== TESTING EVENT CANCELLATION ===")
        
        # Create a test event specifically for deletion
        test_event = {
            "title": "Event to be Cancelled",
            "description": "This event will be cancelled for testing purposes",
            "date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "time": "15:00",
            "location": "Test Location",
            "category": "Test",
            "max_participants": 10,
            "creator_id": "alice_smith",
            "creator_name": "Alice Smith"
        }
        
        try:
            # Create the event
            created = self.dm.create_event(test_event)
            if created:
                # Get the event ID (you might need to implement get_event_by_title or similar)
                events = self.dm.get_events_by_creator("alice_smith")
                event_to_cancel = None
                for event in events:
                    if event.get("title") == "Event to be Cancelled":
                        event_to_cancel = event
                        break
                
                if event_to_cancel:
                    success = self.dm.cancel_event(event_to_cancel.get("id"))
                    self.log_test(
                        "Cancel event", 
                        success,
                        f"Event cancellation {'successful' if success else 'failed'}"
                    )
                else:
                    self.log_test("Cancel event", False, "Could not find event to cancel")
            else:
                self.log_test("Cancel event setup", False, "Could not create test event for cancellation")
                
        except Exception as e:
            self.log_test("Cancel event test", False, str(e))

    def test_database_performance(self):
        """Test database performance with bulk operations"""
        print("\n=== TESTING DATABASE PERFORMANCE ===")
        
        start_time = time.time()
        
        # Test bulk event retrieval performance
        try:
            for i in range(10):  # Multiple rapid queries
                events = self.dm.get_all_events()
            
            end_time = time.time()
            duration = end_time - start_time
            success = duration < 5.0  # Should complete in under 5 seconds
            
            self.log_test(
                "Bulk query performance", 
                success,
                f"10 queries completed in {duration:.2f} seconds",
                {"duration_seconds": duration, "queries": 10}
            )
            
        except Exception as e:
            self.log_test("Bulk query performance", False, str(e))

    def run_all_tests(self):
        """Run the complete test suite"""
        print("🚀 STARTING COMPREHENSIVE DATABASE TEST SUITE 🚀")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run all test categories
        self.test_user_registration()
        self.test_user_authentication()
        self.test_event_creation()
        self.test_event_retrieval()
        self.test_event_registration()
        self.test_user_event_queries()
        self.test_event_updates()
        self.test_event_cancellation()
        self.test_database_performance()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Generate test report
        self.generate_test_report(total_duration)

    def generate_test_report(self, duration):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 60)
        print("📊 TEST SUITE RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests Run: {total_tests}")
        print(f"Tests Passed: {passed_tests} ✅")
        print(f"Tests Failed: {failed_tests} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        print(f"Total Duration: {duration:.2f} seconds")
        
        # Show failed tests details
        if failed_tests > 0:
            print(f"\n🔍 FAILED TESTS DETAILS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        # Save detailed report to file
        try:
            report_data = {
                "summary": {
                    "total_tests": total_tests,
                    "passed": passed_tests,
                    "failed": failed_tests,
                    "success_rate": success_rate,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat()
                },
                "detailed_results": self.test_results
            }
            
            with open(f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
                json.dump(report_data, f, indent=2)
            print(f"\n📄 Detailed report saved to: test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
        except Exception as e:
            print(f"\n⚠️  Could not save report file: {str(e)}")
        
        print("\n🏁 TEST SUITE COMPLETED!")
        print("=" * 60)


def main():
    """Main function to run the test suite"""
    test_suite = DatabaseTestSuite()
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()