# Notification Service
# Sends alerts to teachers when students struggle

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
from dapr.ext.fastapi import DaprApp

# Initialize FastAPI with Dapr
app = FastAPI(title="Notification Service", version="1.0.0")
dapr = DaprApp(app)

# Configuration
KAFKA_BINDING_NAME = os.getenv("DAPR_PUBSUB_NAME", "learnflow-pubsub")
TOPIC_STRUGGLE = "struggle-detected"

# Email/Notification settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

# ============================================================================
# Models
# ============================================================================

class StruggleAlert(BaseModel):
    """Alert for teacher intervention"""
    alert_id: str
    student_id: str
    student_name: str
    teacher_id: str
    teacher_email: str
    topic_id: Optional[int] = None
    trigger_type: str  # "repeated_error", "time_exceeded", "low_quiz_score", "keyword_phrase", "failed_executions"
    context: dict
    created_at: datetime
    severity: str = "medium"  # "low", "medium", "high"

class NotificationRequest(BaseModel):
    """Request to send notification"""
    recipient_email: str
    subject: str
    message: str
    alert_type: str = "email"

class NotificationStatus(BaseModel):
    """Status of sent notification"""
    notification_id: str
    alert_id: str
    status: str  # "pending", "sent", "failed"
    sent_at: Optional[datetime] = None
    error: Optional[str] = None

# In-memory storage for demo (use database in production)
notification_history: List[NotificationStatus] = []

# ============================================================================
# Notification Channels
# ============================================================================

class NotificationChannel:
    """Base class for notification channels"""

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send notification. Returns True if successful."""
        raise NotImplementedError

class EmailChannel(NotificationChannel):
    """Send email notifications"""

    def __init__(self):
        self.enabled = bool(SMTP_USER and SMTP_PASSWORD)

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send email via SMTP"""
        if not self.enabled:
            print(f"[Email] SMTP not configured. Would send to {recipient}: {subject}")
            return True  # Pretend success for demo

        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart()
            msg['From'] = SMTP_USER
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASSWORD)
                server.send_message(msg)

            print(f"[Email] Sent to {recipient}: {subject}")
            return True

        except Exception as e:
            print(f"[Email] Failed to send: {e}")
            return False

class WebhookChannel(NotificationChannel):
    """Send webhook notifications"""

    def __init__(self):
        self.webhook_urls = os.getenv("WEBHOOK_URLS", "").split(",")

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        """Send webhook POST request"""
        import httpx

        payload = {
            "recipient": recipient,
            "subject": subject,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }

        success = True
        for url in self.webhook_urls:
            if not url.strip():
                continue
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(url.strip(), json=payload, timeout=5)
                    response.raise_for_status()
                print(f"[Webhook] Sent to {url}")
            except Exception as e:
                print(f"[Webhook] Failed: {e}")
                success = False

        return success

class ConsoleChannel(NotificationChannel):
    """Log notifications to console (for demo/testing)"""

    async def send(self, recipient: str, subject: str, message: str) -> bool:
        """Print notification to console"""
        print(f"""
{'='*60}
NOTIFICATION
{'='*60}
To: {recipient}
Subject: {subject}
{message}
{'='*60}
        """)
        return True

# Initialize channels
channels = {
    "email": EmailChannel(),
    "webhook": WebhookChannel(),
    "console": ConsoleChannel()
}

# ============================================================================
# Notification Service
# ============================================================================

class NotificationService:
    """Service for sending teacher notifications"""

    @staticmethod
    def format_alert_message(alert: StruggleAlert) -> str:
        """Format struggle alert into readable message"""
        trigger_descriptions = {
            "repeated_error": "Student has encountered the same error multiple times",
            "time_exceeded": "Student has spent too long on a single exercise",
            "low_quiz_score": "Student scored poorly on a recent quiz",
            "keyword_phrase": "Student expressed frustration or asked for help",
            "failed_executions": "Student has multiple failed code executions"
        }

        description = trigger_descriptions.get(
            alert.trigger_type,
            "Student may need additional support"
        )

        return f"""
LearnFlow Student Alert

Student: {alert.student_name} (ID: {alert.student_id})
Topic: {alert.context.get('topic_name', 'General')} (ID: {alert.topic_id})
Issue: {description}
Severity: {alert.severity.upper()}
Time: {alert.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Details:
{alert.context.get('details', 'No additional details available')}

Please check in with the student to provide guidance.

---
This is an automated alert from LearnFlow Platform.
        """

    @staticmethod
    def determine_severity(alert: StruggleAlert) -> str:
        """Determine alert severity based on trigger type and context"""
        if alert.trigger_type in ["failed_executions", "keyword_phrase"]:
            return "high"
        elif alert.trigger_type in ["low_quiz_score", "time_exceeded"]:
            return "medium"
        else:
            return "low"

    async def send_alert(self, alert: StruggleAlert) -> NotificationStatus:
        """
        Send notification to teacher about struggling student.

        Args:
            alert: The struggle alert to send

        Returns:
            NotificationStatus with result
        """
        alert_id = alert.alert_id or f"alert-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        notification_id = f"notif-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

        # Ensure severity is set
        if not alert.severity or alert.severity == "medium":
            alert.severity = self.determine_severity(alert)

        # Format message
        message = self.format_alert_message(alert)
        subject = f"[{alert.severity.upper()}] LearnFlow Alert: {alert.student_name}"

        # Send via all configured channels
        success_count = 0
        for channel_name, channel in channels.items():
            try:
                if await channel.send(alert.teacher_email, subject, message):
                    success_count += 1
            except Exception as e:
                print(f"[Notification] {channel_name} failed: {e}")

        # Create status
        status = NotificationStatus(
            notification_id=notification_id,
            alert_id=alert_id,
            status="sent" if success_count > 0 else "failed",
            sent_at=datetime.now() if success_count > 0 else None,
            error=None if success_count > 0 else "All notification channels failed"
        )

        notification_history.append(status)
        return status

# Global service instance
notification_service = NotificationService()

# ============================================================================
# Routes
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "Notification Service",
        "status": "healthy",
        "version": "1.0.0",
        "channels": list(channels.keys())
    }

@app.get("/health")
async def health():
    """Health check for Kubernetes probes"""
    return {"status": "healthy"}

@app.post("/notify", response_model=NotificationStatus)
async def send_notification(request: NotificationRequest, background_tasks: BackgroundTasks):
    """Send a direct notification"""
    notification_id = f"notif-{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    # Send in background
    async def send_and_log():
        channel = channels.get("console", channels["email"])
        await channel.send(request.recipient_email, request.subject, request.message)

    background_tasks.add_task(send_and_log)

    return NotificationStatus(
        notification_id=notification_id,
        alert_id="manual",
        status="pending",
        sent_at=None,
        error=None
    )

@app.post("/alert", response_model=NotificationStatus)
async def send_alert(alert: StruggleAlert, background_tasks: BackgroundTasks):
    """Send struggle alert to teacher"""
    async def send():
        await notification_service.send_alert(alert)

    background_tasks.add_task(send)

    return NotificationStatus(
        notification_id=f"notif-{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
        alert_id=alert.alert_id,
        status="pending",
        sent_at=None,
        error=None
    )

@app.get("/notifications")
async def list_notifications(limit: int = 50):
    """List notification history"""
    return {
        "notifications": notification_history[-limit:],
        "total": len(notification_history)
    }

# ============================================================================
# Kafka Event Handler (Dapr)
# ============================================================================

# @dapr.subscribe(pubsub_name=KAFKA_BINDING_NAME, topic=TOPIC_STRUGGLE)
async def handle_struggle_alert(event_data: dict) -> None:
    """
    Subscribe to struggle.detected topic and send notifications.

    Automatically alerts teachers when students show signs of struggling.
    """
    try:
        data = event_data.get("data", {})

        alert = StruggleAlert(
            alert_id=data.get("alert_id", f"auto-{datetime.now().strftime('%Y%m%d%H%M%S')}"),
            student_id=data.get("student_id", ""),
            student_name=data.get("student_name", "Student"),
            teacher_id=data.get("teacher_id", ""),
            teacher_email=data.get("teacher_email", ""),
            topic_id=data.get("topic_id"),
            trigger_type=data.get("trigger_type", "unknown"),
            context=data.get("context", {}),
            created_at=datetime.now(),
            severity="medium"
        )

        await notification_service.send_alert(alert)
        print(f"[Notification] Sent alert for student {alert.student_id} to {alert.teacher_email}")

    except Exception as e:
        print(f"[Notification] Error handling struggle alert: {e}")

# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8109)))
