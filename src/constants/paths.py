from pathlib import Path


# Path to the src directory used as a base path for other paths
SRC_PATH = Path(__file__).resolve().parent.parent

paths: dict[str, Path] = {
  "USERS_DB": SRC_PATH / 'database' / 'users.json'
}


if __name__ == "__main__":
  for key, value in paths.items():
    print(f"{key}: {value}")