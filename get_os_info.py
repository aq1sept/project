import platform
import psutil
import subprocess

def safe_get(func, default="N/A"):
    """Безпечний виклик функції з обробкою помилок"""
    try:
        return func()
    except Exception as e:
        return f"{default} (Error: {e})"

def get_system_info():
    info = {}

    # ОС
    info["OS"] = safe_get(lambda: f"{platform.system()} {platform.release()} ({platform.version()})")

    # Архітектура
    info["Architecture"] = safe_get(lambda: platform.architecture()[0])

    # Ім’я комп’ютера
    info["Machine name"] = safe_get(lambda: platform.node())

    # Процесор
    info["Processor"] = safe_get(lambda: platform.processor() or "Unknown CPU")

    # Кількість ядер і потоків
    info["CPU Cores"] = safe_get(lambda: psutil.cpu_count(logical=False))
    info["CPU Threads"] = safe_get(lambda: psutil.cpu_count(logical=True))

    # Оперативна пам’ять
    info["RAM"] = safe_get(lambda: f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB")

    # Диск (C:)
    info["Disk (C:)"] = safe_get(lambda: f"{round(psutil.disk_usage('C:\\').total / (1024**3), 2)} GB")

    # GPU
    def get_gpu():
        gpu_info = subprocess.check_output(
            "wmic path win32_VideoController get name", shell=True
        ).decode(errors="ignore").strip().split("\n")[1:]
        gpus = [gpu.strip() for gpu in gpu_info if gpu.strip()]
        return ", ".join(gpus) if gpus else "Unknown GPU"

    info["GPU"] = safe_get(get_gpu)

    return info


if __name__ == "__main__":
    print("=== System Information ===")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")
