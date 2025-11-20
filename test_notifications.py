#!/usr/bin/env python3
"""
Test script for the notification system.
Run this script to test if desktop notifications are working.
"""

import sys
import os

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.notifications import (
    test_notification_system,
    send_alert_notification,
    send_system_notification
)


def main():
    print("Testing Health Alert Notification System...")
    print("=" * 50)
    
    # Test 1: Basic notification system test
    print("\n1. Testing basic notification system...")
    success = test_notification_system()
    if success:
        print("✅ Basic notification test passed!")
    else:
        print("❌ Basic notification test failed!")
    
    # Test 2: Health alert notification
    print("\n2. Testing health alert notification...")
    success = send_alert_notification(
        disease="Dengue",
        district="Test District",
        patient_count=3,
        window_days=14
    )
    if success:
        print("✅ Health alert notification test passed!")
    else:
        print("❌ Health alert notification test failed!")
    
    # Test 3: Custom system notification
    print("\n3. Testing custom system notification...")
    success = send_system_notification(
        "Test Complete",
        "All notification tests have been executed!"
    )
    if success:
        print("✅ Custom system notification test passed!")
    else:
        print("❌ Custom system notification test failed!")
    
    print("\n" + "=" * 50)
    print("Notification system testing complete!")
    print("Check your desktop for the notification popups.")
    print("\nNote: If notifications didn't appear, make sure:")
    print("1. You have installed the required dependencies: pip install plyer")
    print("2. Your system supports desktop notifications")
    print("3. Notification permissions are enabled for Python/your terminal")


if __name__ == "__main__":
    main()
