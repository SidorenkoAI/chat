import csv
import sys

from db.storage import get_connection, load_all_messages


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "history.csv"
    rows = load_all_messages(get_connection())

    # utf-8-sig и ";" — чтобы русский Excel открыл файл без «кракозябр» и по столбцам.
    with open(out_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow(["id", "автор", "текст", "время"])
        writer.writerows(rows)

    print(f"Выгружено сообщений: {len(rows)} -> {out_path}")


if __name__ == "__main__":
    main()
