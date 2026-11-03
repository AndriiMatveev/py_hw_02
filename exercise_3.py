import sys
from typing import List, Dict, Optional


def parse_log_line(line: str) -> Optional[dict]:
    line = line.strip()
    if not line:
        return None
    parts = line.split(' ', 3)
    if len(parts) < 4:
        return None
    return {
        "date": parts[0],
        "time": parts[1],
        "level": parts[2].upper(),
        "message": parts[3]
    }


def load_logs(file_path: str) -> List[dict]:
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                parsed = parse_log_line(line)
                if parsed:
                    logs.append(parsed)
                elif line.strip():
                    print(f"Попередження: Пропущено некоректний рядок {line_num}")
    except FileNotFoundError:
        print(f"Помилка: Файл за шляхом '{file_path}' не знайдено.")
        sys.exit(1)
    except IOError:
        print(f"Помилка: Не вдалося прочитати файл '{file_path}'.")
        sys.exit(1)

    return logs


def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    target_level = level.upper()
    return [log for log in logs if log["level"] == target_level]

def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    counts = {}
    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1
    return counts


def display_log_counts(counts: Dict[str, int]):
    print(f"{'Рівень логування':<16} | {'Кількість'}")
    print("-" * 17 + "|" + "-" * 10)
    standard_levels = ["INFO", "DEBUG", "ERROR", "WARNING"]
    all_levels = standard_levels + [lvl for lvl in counts if
                                    lvl not in standard_levels]
    for level in all_levels:
        if level in counts:
            print(f"{level:<16} | {counts[level]}")


def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <path_to_logfile.log> [log_level]")
        sys.exit(1)
    file_path = sys.argv[1]
    logs = load_logs(file_path)

    if not logs:
        print("Файл порожній або не містить коректних записів логів.")
        return
    counts = count_logs_by_level(logs)
    display_log_counts(counts)
    if len(sys.argv) >= 3:
        requested_level = sys.argv[2].upper()
        filtered = filter_logs_by_level(logs, requested_level)
        print(f"\nДеталі логів для рівня '{requested_level}':")
        if not filtered:
            print(f"Записів із рівнем {requested_level} не знайдено.")
        else:
            for log in filtered:
                print(f"{log['date']} {log['time']} - {log['message']}")


if __name__ == "__main__":
    main()
