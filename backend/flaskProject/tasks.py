from celery_config import app
from send_email import send_email
from utils import get_db_connection

@app.task
def check_pending_reqs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT
            Users.mail,
            Users.full_name,
            COUNT(ServiceRequests.serviceman_id) AS request_count
        FROM ServiceRequests
        JOIN Users ON ServiceRequests.serviceman_id = Users.user_id
        WHERE ServiceRequests.status = "requested"
        GROUP BY Users.mail, Users.full_name;
        """)

    pendings = cursor.fetchall()
    conn.close()

    for serviceman in pendings:
        email = serviceman['mail']
        full_name = serviceman['full_name']
        request_count = serviceman['request_count']

        html_content = f"""
        <html>
        <body style="text-align: center; font-family: Arial, sans-serif;">
            <h2>🔔 Notification of Pending Service Requests</h2>
            <p>Dear {full_name},</p>
            <p>We hope this email finds you well. We wanted to bring to your attention that you currently have pending service requests that require your attention.</p>
            <table style="border-collapse: collapse; width: 60%; margin: 20px auto; text-align: left;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 12px; border: 1px solid #ddd;">Pending Requests</th>
                    <th style="padding: 12px; border: 1px solid #ddd;">Count</th>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #ddd;">Service Requests Awaiting Your Response</td>
                    <td style="padding: 12px; border: 1px solid #ddd;"><strong>{request_count}</strong></td>
                </tr>
            </table>
            <p>These requests are from customers who are eagerly waiting for your services. We kindly request you to review and respond to these requests at your earliest convenience.</p>
            <p>To view and manage your pending requests, please click the button below to log in to our website:</p>
            <a href="http://localhost:8080/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0;">Login to Manage Requests</a>
            <p>Responding promptly to these requests will help maintain high customer satisfaction and potentially lead to more business opportunities for you.</p>
            <p>If you have any questions or need assistance in managing these requests, please don't hesitate to contact our support team.</p>
            <p>Thank you for your prompt attention to this matter and for being a valued member of our service network.</p>
            <p>Best regards,<br>Your Service Management Team</p>
        </body>
        </html>
        """

        subject = f"You have {request_count} pending service request{'s' if request_count > 1 else ''}"
        send_email(email, subject, html_content)

    print(f"Sent email notifications to {len(pendings)} servicemen about their pending requests.")