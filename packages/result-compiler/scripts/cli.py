import argparse
from pathlib import Path

from compiler.clean_results import clean_school_result
from compiler.generate_results import generate_school_result
from compiler.models.RawResponseModels import RawSchoolResultJsonModel


def compile(args: argparse.Namespace):
    src = Path(args.src)
    if not src.is_absolute():
        raise FileNotFoundError(
            f"the src path must be an absolute path. Recieved {args.src}"
        )
    if not src.exists():
        raise FileNotFoundError(f"no file found at {src.absolute()}")

    dest = Path(args.dest)
    if not dest.is_absolute():
        raise FileNotFoundError(
            f"the dest path must be an absolute path. Recieved {args.des}"
        )
    if not dest.parent.exists():
        raise FileNotFoundError(
            f"the dest directory doesnt exists at {dest.parent.absolute()}"
        )

    raw = RawSchoolResultJsonModel.model_validate_json(src.read_text())
    cleaned = clean_school_result(raw)
    compiled = generate_school_result(cleaned)
    dest.write_text(compiled.model_dump_json(indent=4 if args.pretty_json else None))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Result Compiler CLI")
    subparser = parser.add_subparsers(
        title="commands", required=True, help="Supported Commands"
    )
    compile_parser = subparser.add_parser("compile")
    compile_parser.add_argument(
        "src", help="Absolute path for the Result JSON response"
    )
    compile_parser.add_argument(
        "dest", help="Absolute path where the Compiled results would be saved to"
    )
    compile_parser.add_argument(
        "-p", "--pretty-json", action="store_true", default=False
    )
    compile_parser.set_defaults(func=compile)
    args = parser.parse_args()
    args.func(args)
