from kafka import KafkaConsumer
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Função para enviar notificação por e-mail
def send_email(file_name, operation, contact):
    sender_email = "ijtp@discente.ifpe.edu.br"
    receiver_email = contact
    password = "Plughi123!"  

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Operação concluída"

    body = f"O arquivo {file_name} passou pela operação de {operation}."
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")



# Consumir as mensagens do tópico Kafka
def consume_notifications():
    consumer = KafkaConsumer(
        '/notificacao',
        bootstrap_servers=['kafka1:19091', 'kafka2:19092', 'kafka3:19093'],
        group_id='notificador-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        file_name = message.value['file_name']
        operation = message.value['operation']
        contact = message.value['email']  
        
    send_email(file_name, operation, contact)

# Iniciar o consumo
try:
    consume_notifications()
except Exception as e :
    print("Erro ao consumir mensagem")
