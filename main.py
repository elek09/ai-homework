import socket
import json
import time
from collections import deque


def connect_to_server():
    host = 'stackoverflow.nordquant.com'
    port = 2730

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Connection successful!")
        return sock
    except Exception as e:
        print(f"Error during connection: {e}")
        return None


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError:
        return False
    return True


def receive_data(sock):
    buffer = ""
    try:
        while True:
            data = sock.recv(4096).decode('utf-8')
            if not data:
                break

            buffer += data
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if is_json(line.strip()):
                    try:
                        answer = json.loads(line)
                        return answer
                    except json.JSONDecodeError as e:
                        print(f"JSON error: {e} - Line: {line}")
                else:
                    print(f"Non-JSON line: {line.strip()}")
    except Exception as e:
        print(f"Error while reading data: {e}")
        return None


def process_data(answers_stream, max_iterations=None):
    sliding_window = deque(maxlen=5)
    iterations = 0  #only for unit test

    while True:
        if max_iterations and iterations >= max_iterations:
            break

        current_time = time.time()
        answers = receive_data(answers_stream)

        if answers:
            sliding_window.append((current_time, answers))

        window_answers = [a for t, a in sliding_window if current_time - t <= 5]

        cooking_count = sum(a['site'] == 'cooking' for a in window_answers)
        datascience_count = sum(a['site'] == 'datascience' for a in window_answers)
        stackoverflow_count = sum(a['site'] == 'stackoverflow' for a in window_answers)

        print({
            "startTime": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(current_time - 5)),
            "endTime": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(current_time)),
            "answer_counts": {
                "cooking": cooking_count,
                "datascience": datascience_count,
                "stackoverflow": stackoverflow_count
            }
        })

        time.sleep(1)
        iterations += 1

if __name__ == "__main__":
    sock = connect_to_server()
    if sock:
        process_data(sock)