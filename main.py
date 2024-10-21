import socket

def connect_to_server():
    host = 'stackoverflow.nordquant.com'
    port = 2730

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Kapcsolódás sikeres!")
        return sock
    except Exception as e:
        print(f"Hiba a kapcsolódás közben: {e}")
        return None
