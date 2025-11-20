"""
Server-side notification utility for health alert system.
Provides desktop notifications when health alerts are generated.
"""

import logging
import threading
from typing import Optional


def send_desktop_notification(title: str, message: str, timeout: int = 10) -> bool:
    """
    Send a desktop notification using plyer library.
    
    Args:
        title: Notification title
        message: Notification message body
        timeout: Notification timeout in seconds (default: 10)
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    try:
        # Try multiple ways to import plyer
        notification_module = None
        try:
            from plyer import notification as notification_module
        except ImportError:
            try:
                import sys
                import os
                # Try adding common virtual environment paths
                possible_paths = [
                    r"d:\project\sanitary\code\v5\.venv\Lib\site-packages",
                    r"d:\Project\Sanitary\Code\V5\.venv\Lib\site-packages",
                    r".venv\Lib\site-packages",
                    r"venv\Lib\site-packages"
                ]
                
                for path in possible_paths:
                    if os.path.exists(path) and path not in sys.path:
                        sys.path.insert(0, path)
                        try:
                            from plyer import notification as notification_module
                            break
                        except ImportError:
                            continue
                            
                if notification_module is None:
                    raise ImportError("Could not import plyer from any location")
                    
            except Exception:
                raise ImportError("plyer library not available")
        
        if notification_module is None:
            raise ImportError("plyer notification module not available")
        
        # Send notification in a separate thread to avoid blocking the main thread
        def _send_notification():
            try:
                notification_module.notify(
                    title=title,
                    message=message,
                    timeout=timeout,
                    app_name="Health Alert System",
                    app_icon=None  # You can add an icon path here if available
                )
                logging.info(f"Desktop notification sent: {title} - {message}")
            except Exception as e:
                logging.error(f"Failed to send desktop notification: {e}")
        
        # Run notification in background thread
        notification_thread = threading.Thread(target=_send_notification, daemon=True)
        notification_thread.start()
        
        return True
        
    except ImportError as e:
        logging.warning(f"plyer library not available: {e}. Try: pip install plyer")
        return False
    except Exception as e:
        logging.error(f"Error sending desktop notification: {e}")
        return False


def send_alert_notification(disease: str, district: str, patient_count: int, window_days: int) -> bool:
    """
    Send a health alert notification with formatted message.
    
    Args:
        disease: Disease name
        district: District name
        patient_count: Number of unique patients
        window_days: Time window in days
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    title = "🚨 Health Alert Generated"
    message = f"{disease} outbreak alert for {district}: {patient_count} unique patient(s) in last {window_days} days"
    
    return send_desktop_notification(title, message, timeout=15)


def send_system_notification(title: str, message: str) -> bool:
    """
    Send a general system notification.
    
    Args:
        title: Notification title
        message: Notification message
        
    Returns:
        bool: True if notification was sent successfully, False otherwise
    """
    return send_desktop_notification(f"Health System - {title}", message)


def test_notification_system() -> bool:
    """
    Test the notification system by sending a test notification.
    
    Returns:
        bool: True if test notification was sent successfully, False otherwise
    """
    return send_system_notification(
        "System Test", 
        "Notification system is working correctly!"
    )


# Email notification support (optional extension)
def send_email_notification(
    to_email: str, 
    subject: str, 
    message: str, 
    smtp_server: Optional[str] = None,
    smtp_port: Optional[int] = None,
    username: Optional[str] = None,
    password: Optional[str] = None
) -> bool:
    """
    Send email notification (requires SMTP configuration).
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        message: Email message body
        smtp_server: SMTP server address
        smtp_port: SMTP server port
        username: SMTP username
        password: SMTP password
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Use default values if not provided (you can configure these in .env)
        smtp_server = smtp_server or "smtp.gmail.com"
        smtp_port = smtp_port or 587
        
        if not username or not password:
            logging.warning("Email credentials not provided. Skipping email notification.")
            return False
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(username, password)
        text = msg.as_string()
        server.sendmail(username, to_email, text)
        server.quit()
        
        logging.info(f"Email notification sent to {to_email}: {subject}")
        return True
        
    except Exception as e:
        logging.error(f"Failed to send email notification: {e}")
        return False
