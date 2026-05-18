from pathlib import Path

# TODO: find some better way to resolve data package
data_dir = Path(__file__).parent.parent.parent.parent / "data" / "data"


def read_from(filename: str) -> str:
    filepath = data_dir.joinpath(filename)
    if not filepath.exists():
        raise FileNotFoundError(f"File {filepath.absolute()} doesnt exists")

    return filepath.read_text()


def write_to(filename: str, content: str) -> None:
    filepath = data_dir.joinpath(filename)
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True)
    filepath.write_text(content)
