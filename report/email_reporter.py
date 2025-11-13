# coding=utf-8

######################################################################################################
#  Class that will generate and send an email with the ACI Fabric information collected.              #
######################################################################################################

##################
# Import Section #
##################

import smtplib
import ssl
import certifi
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Type
from datetime import datetime


###########################
# Private Singleton Class #
###########################

class _PrivateCookie(type):

    _instances: Dict[Type[Any], Any] = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

##########################################################################################################
# EmailReportGenerator Class that will format the collected data and send an email report                #
##########################################################################################################

class EmailReportGenerator(metaclass=_PrivateCookie):

    def __init__(self, sender_email, smtp_server, sender_password, receiver_email, smtp_port):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.receiver_email = receiver_email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def _generate_html_report(self, nodeList, edgeList):
        """Generates the HTML content for the email report based on nodeList and edgeList."""

        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; color: #333; }
            .container { max-width: 800px; margin: 20px auto; background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
            h1, h2 { color: #0056b3; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            pre { background-color: #eee; padding: 10px; border-radius: 5px; overflow-x: auto; }
            .section-header { margin-top: 30px; border-bottom: 2px solid #0056b3; padding-bottom: 5px; }
        </style>
        </head>
        <body>
        <div class="container">
            <h1>Cisco ACI Fabric Health Report</h1>
            <p>This report provides an overview of the network nodes and connections in your Cisco ACI fabric.</p>

            <h2 class="section-header">Node Information</h2>
            <pre>"""

        # Add nodeList info to the HTML
        for node, attributes in nodeList:
            html_content += f"Node: {node}\n"
            for key, attr in attributes.items():
                html_content += f"  - {key}: {attr}\n"
            html_content += "\n"

        html_content += """</pre>

            <h2 class="section-header">Edge Information</h2>
            <pre>"""

        # Add edgeList info to the HTML
        for source, target, attributes in edgeList:
            html_content += f"Edge from {source} to {target}\n"
            if attributes:
                for key, value in attributes.items():
                    html_content += f"  - {key}: {value}\n"
            html_content += "\n"

        html_content += f"""</pre>

            <p>Report generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
        </body>
        </html>
        """
        return html_content

    def send_report(self, nodeList, edgeList, subject="ACI Fabric Health Report"):
        """Sends the email report with the collected data."""

        # Create the email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email

        # Generate the HTML content
        html_body = self._generate_html_report(nodeList, edgeList)
        html_part = MIMEText(html_body, "html")

        # Attach HTML part to the message
        msg.attach(html_part)

        try:
            # Create a SSL context that uses the certifi CA bundle
            context = ssl.create_default_context(cafile=certifi.where())
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("Email sent successfully! 🚀")
        except Exception as e:
            print(f"Error sending email: {e} 😞")
            print("Please check your email credentials, SMTP server settings, and ensure 'less secure app access' is enabled for your email account if necessary.")
