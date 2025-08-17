import platform
import psutil
import subprocess
import os

def get_system_info():
    info = {}

    # ОС
    info["OS"] = f"{platform.system()} {platform.release()} ({platform.version()})"

    # Архітектура
    info["Architecture"] = platform.architecture()[0]

    # Ім’я комп’ютера
    info["Machine name"] = platform.node()

    # Процесор
    info["Processor"] = platform.processor()

    # Кількість ядер і потоків
    info["CPU Cores"] = psutil.cpu_count(logical=False)
    info["CPU Threads"] = psutil.cpu_count(logical=True)

    # Оперативна пам’ять
    ram = psutil.virtual_memory()
    info["RAM"] = f"{round(ram.total / (1024**3), 2)} GB"

    # Диск
    disk = psutil.disk_usage('/')
    info["Disk"] = f"{round(disk.total / (1024**3), 2)} GB"

    # Відеокарта (через WMIC)
    try:
        gpu_info = subprocess.check_output(
            "wmic path win32_VideoController get name", shell=True
        ).decode(errors="ignore").strip().split("\n")[1:]
        info["GPU"] = ", ".join([gpu.strip() for gpu in gpu_info if gpu.strip()])
    except Exception as e:
        info["GPU"] = f"Error: {e}"

    return info


if __name__ == "__main__":
    system_info = get_system_info()
    print("=== System Information ===")
    for key, value in system_info.items():
        print(f"{key}: {value}")
