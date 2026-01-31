from opensanctions.config import DELIVERY_TOKEN
from opensanctions.download import download_dataset_file


def main() -> None:
    path = download_dataset_file(
        dataset="sanctions",
        date="20211231",
        output_path="datasets/2021",
        delivery_token=DELIVERY_TOKEN,
    )
    print(f"Downloaded to: {path.resolve()}")


if __name__ == "__main__":
    main()
