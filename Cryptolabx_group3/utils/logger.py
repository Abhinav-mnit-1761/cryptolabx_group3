from datetime import datetime


def write_log(option):
    with open("outputs/log.txt", "a") as log_file:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{current_time} - {option}\n")