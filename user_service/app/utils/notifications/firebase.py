import logging
import firebase_admin
from firebase_admin import credentials, messaging
import os

logger = logging.getLogger(__name__)

try:
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase-credentials.json")
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin initialized successfully.")
    else:
        logger.warning(f"Firebase credentials not found at {cred_path}. Notifications will be mocked.")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin: {e}")

def send_notification(token: str, title: str, body: str, data: dict = None):
    """
    Sends a push notification to a single device token.
    """
    if not firebase_admin._apps:
        logger.info(f"Mock Notification -> Title: {title} | Body: {body} | Token: {token}")
        return False

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            token=token,
        )
        response = messaging.send(message)
        logger.info(f"Successfully sent message: {response}")
        return True
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False

def send_multicast_notification(tokens: list[str], title: str, body: str, data: dict = None):
    """
    Sends a push notification to multiple device tokens.
    """
    if not tokens:
        return False
        
    if not firebase_admin._apps:
        logger.info(f"Mock Multicast Notification -> Title: {title} | Body: {body} | Tokens: {len(tokens)}")
        return False

    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=tokens,
        )
        response = messaging.send_multicast(message)
        logger.info(f"Successfully sent multicast message. Success count: {response.success_count}")
        return True
    except Exception as e:
        logger.error(f"Error sending multicast message: {e}")
        return False
