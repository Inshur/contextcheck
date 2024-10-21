import argparse

from contextcheck.executors.tests_router import TestsRouter


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        self.exit(2, f"\n{self.prog}: error: {message}\n")

    def validate_args(self, args):
        if args.output_type == "file":
            if not args.filename and not args.folder:
                self.error("--filename or --folder is required")
            if (args.filename or args.folder) and not args.output_folder:
                self.error(
                    '--output-folder is required when --output is "console" and filename or folder is set'
                )


def main():
    parser = CustomArgumentParser(
        description=(
            "ContextCheck Tests Runner. Run tests from a file or folder and output the results in the console or save to JSON files."
        )
    )

    parser.add_argument(
        "--output-type",
        required=True,
        choices=["console", "file"],
        help='Specify the output type: "console" or "file"',
    )

    parser.add_argument(
        "--filename",
        nargs="+",
        help="Filename (or list of space separated filenames) to use for tests",
    )

    parser.add_argument("--folder", help="Folder name to load all YAML files from for tests")

    parser.add_argument(
        "--output-folder",
        help='[Required if --output-type is "file"] Specify the output folder to save the test results in JSON format',
    )

    parser.add_argument(
        "--exit-on-failure", action="store_true", help="Exit with status code 1 if any test fails"
    )

    parser.add_argument(
        "--aggregate-results", action="store_true", help="Aggregate assertion results"
    )

    parser.add_argument(
        "--show-time-statistics", action="store_true", help="Show aggregated time statistics"
    )

    args = parser.parse_args()
    parser.validate_args(args)

    TestsRouter(**vars(args)).run_tests()


if __name__ == "__main__":
    main()
