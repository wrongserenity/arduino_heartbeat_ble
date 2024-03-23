import serial
import threading
import csv
import time

# Порт, к которому подключен Arduino
arduino_port = 'COM3'  # Измените на свой порт

# Открытие последовательного порта
arduino = serial.Serial(arduino_port, 9600, timeout=1)
arduino.flush()

# Флаг для сигнала начала записи данных
start_flag = False

# Переменная для хранения пульса
a = 0


# Функция для записи данных в CSV файл
def write_to_csv():
    while True:
        with open('pulse_data.csv', mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), a])
        time.sleep(30)


# Запуск второго потока для записи данных в CSV файл
csv_thread = threading.Thread(target=write_to_csv)
csv_thread.start()

# Основной цикл программы
while True:
    # Считывание данных из Arduino
    if arduino.in_waiting > 0:
        line = arduino.readline().decode('utf-8').rstrip()
        print(line)

        # Проверка сигнала "start" от Arduino
        if line == "start":
            start_flag = True

        # Если сигнал "start" получен, ожидаем сигнал пульса и записываем его в переменную a
        while start_flag:
            if arduino.in_waiting > 0:
                pulse = arduino.readline().decode('utf-8').rstrip()
                try:
                    a = int(pulse)
                    print("Pulse:", a)
                except ValueError:
                    print("Invalid pulse value")