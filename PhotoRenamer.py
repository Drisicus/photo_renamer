import os
import argparse
import re
import shutil
import sys

'''
Simple script to rename photos based on the date in the filename.
Only for photos of 2000 until 2099 (change 20 for 21 if you are alive by then :) ).

The structure of the file must be:
 
20YYMMDD.xxx

It can have any character before the 20 and between the date and the extension.

Usage:

python PhotoRenamer.py -i <input_path> -o <output_path> -l <language>

-l is optional and can be "es" or "en" (default is "es")

Example:

python -i "C:\IMAGES\Fotos" -o "C:\IMAGES\FotosSorted" 

Both must exist in advance to avoid moving everything to a wrong destination.

'''

month_replacement = {
    "es": {
        "01": "enero",
        "02": "febrero",
        "03": "marzo",
        "04": "abril",
        "05": "mayo",
        "06": "junio",
        "07": "julio",
        "08": "agosto",
        "09": "septiembre",
        "10": "octubre",
        "11": "noviembre",
        "12": "diciembre"
    },
    "en": {
        "01": "january",
        "02": "february",
        "03": "march",
        "04": "april",
        "05": "may",
        "06": "june",
        "07": "july",
        "08": "august",
        "09": "september",
        "10": "october",
        "11": "november",
        "12": "december"
    }
}


def parse_args():

    parser = argparse.ArgumentParser(description="Run photo renamer")

    parser.add_argument("-i", "--input_path", type=str, help="Input path")

    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        help="Output path",
    )

    parser.add_argument(
        "-l",
        "--language",
        type=str,
        help="Language for the month folders",
        choices=["es", "en"],
        default="es"
    )

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        exit(1)

    return parser.parse_args()


def main(arguments: argparse.Namespace):

    print(f"Input path: {arguments.input_path}")
    print(f"Output path: {arguments.output_path}")

    input_path = arguments.input_path
    output_path = arguments.output_path
    language = arguments.language

    if not os.path.exists(input_path):
        print("Input path does not exist")
        return
    elif not os.path.exists(output_path):
        print("Output path does not exist")
        return

    walk_folder_and_move_photos(input_path, output_path, language)
    print("..Finished..")


def walk_folder_and_move_photos(input_path: str, output_path: str, language: str) -> None:
    print("Checking folder: " + input_path)
    for root, dirs, filenames in os.walk(input_path):
        sort_and_move_photos(filenames, output_path, root, language)
        print("\tFinished folder: " + input_path)
        for dir in dirs:
            walk_folder_and_move_photos(root + "\\" + dir, output_path, language)


def sort_and_move_photos(filenames: list[str], output_path: str, root: str, language: str) -> None:
    for filename in filenames:
        file_path = os.path.join(root, filename)

        date = re.findall(r"20[0-9]{6}", filename)
        if date:
            year = date[0][:4]
            month = date[0][4:6]
            day = date[0][6:]
            os.makedirs(output_path + "\\" + year, exist_ok=True)

            destination_path = (output_path + "\\" + year + "\\"
                                + month + "_" + month_replacement.get(language).get(month))
            os.makedirs(destination_path, exist_ok=True)
            if os.path.exists(destination_path + "\\" + filename):
                extension_pattern = r"\.[a-zA-Z]{3}"
                extension = re.findall(extension_pattern, file_path)[0]
                updated_file_path = re.sub(extension_pattern, f"_copy{extension}", file_path)
                os.rename(file_path, updated_file_path)
                shutil.move(updated_file_path, destination_path)
            else:
                shutil.move(file_path, destination_path)


if __name__ == "__main__":

    args = parse_args()
    main(args)
