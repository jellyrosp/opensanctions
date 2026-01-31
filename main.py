import sys

from scripts.download_data import main as download_main


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py download")
        sys.exit(1)

    command = sys.argv[1]

    if command == "download":
        download_main()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
