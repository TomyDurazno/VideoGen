import json
import http.client

def read_and_split(file_name):
    phrases = []  # List to store phrases

    try:
        with open(file_name, 'r') as archivo:
            text = archivo.read()  # Lee el contenido del archivo

            # Divide el text en phrases utilizando el punto como delimitador
            phrases = text.split('.')

            # Elimina los espacios en blanco al inicio y al final de cada oración
            phrases = [oracion.strip() for oracion in phrases if oracion.strip()]

    except FileNotFoundError:
        print(f"El archivo '{file_name}' no se encontró.")
    
    return phrases




# Function to send a request to the API and save the speech
def generate_speech(api_key, text, voice_id, output_filename):
    # API endpoint
    conn = http.client.HTTPSConnection("api.elevenlabs.io")

    # Request headers
    headers = {
        "accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    # Request payload
    payload = {
        "text" : text,
        "model_id": "eleven_multilingual_v1",
        "voice_settings": {
            "stability": 0.8,
            "similarity_boost": 0.5
        }
    }

    # Send POST request to the API
    conn.request("POST", f"/v1/text-to-speech/{voice_id}?optimize_streaming_latency=0", headers=headers, body=json.dumps(payload))

    # Get the response
    response = conn.getresponse()

    # Check if the request was successful
    if response.status == 200:
        # Save the audio file
        with open(f"{output_filename}.mp3", "wb") as file:
            file.write(response.read())
        print("Speech generated successfully!")
    else:
        print("Error:", response.status)

    # Close the connection
    conn.close()


api_key = "c469cc35bc1b60d3e53a88aa65da1f2f"
voice_id = "5Q0t7uMcjvnagumLfvZi"


# Ejemplo de uso
file_name = "C:\\Users\\ignac\\Desktop\\text-to-speech-python-master\\guiones\\text.txt"  # Reemplaza 'text.txt' con el nombre de tu archivo
found_phrases = read_and_split(file_name)

i=0
for oracion in found_phrases:
    i = i+1
    output_filename = "C:\\Users\\ignac\\Desktop\\text-to-speech-python-master\\exports\\" + str(i)
    generate_speech(api_key, oracion, voice_id, output_filename)
