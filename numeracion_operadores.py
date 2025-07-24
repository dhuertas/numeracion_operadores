from urllib.request import Request, urlopen
import argparse
import json
import os
import pprint

numbering_filepath = "./busqueda_numeracion.json"

numbering_url = "https://numeracionyoperadores.cnmc.es/api/numeracion/get_busqueda_numeracion"

def download_numbering(save: bool = False) -> dict:

    response = urlopen(Request(url=numbering_url, headers={'User-Agent': 'Mozilla/5.0'}))
    if response.getcode() != 200:
        print("failed downloading operator numbering database")
        return {}

    numbering = json.loads(response.read().decode('utf-8'))

    if save:
        with open(numbering_filepath, "w", encoding="utf-8") as file:
            json.dump(numbering, file)

    return numbering


def main(opts):
    """
    Script that tries to identify which company operates a given Spanish phone number

    Sources:
    - https://avance.digital.gob.es/es-ES/Servicios/Numeracion/Documents/Descripcion_PNN.pdf
    - https://avance.digital.gob.es/es-ES/Servicios/Numeracion/Documents/Guia_Numeracion.pdf

    """
    search_numbers = []
    numbering = {}

    if opts.number_list:
        with open(opts.number_list, "r") as file:
            search_numbers = [line.rstrip() for line in file]

    if opts.number:
        search_numbers.append(str(opts.number))

    if not search_numbers:
        print("No numbers to search")
        return

    if opts.no_cache:
        # Using no-cache
        numbering = download_numbering()
    else:
        if os.path.isfile(numbering_filepath):
            # Use existing file
            with open(numbering_filepath, "r") as file:
                numbering = json.load(file)
        else:
            # Download file and save
            numbering = download_numbering(save=True)

    if not numbering:
        print("Numbering database not found")
        return

    response = urlopen(Request(url=numbering_url, headers={'User-Agent': 'Mozilla/5.0'}))
    if response.getcode() == 200:
        numbering = json.loads(response.read().decode('utf-8'))
    else:
        print("failed to get numbering db")

        # Alternatively, download the file externaly and enable the comment code below
        #
        # with open(numbering_filepath, 'r') as file:
        #     numbering = json.load(file)
        return

    ndc_db = {}
    for n in numbering:

        destination_code = n.get("indicativo_destino")
        segment = n.get("bloque")

        if destination_code not in ndc_db:
            ndc_db[destination_code] = set()

        if segment:
            ndc_db[destination_code].add(segment)

    for number in search_numbers:

        found_dc = None
        found_segment = None

        for dc in ndc_db.keys():

            if number.startswith(dc):

                found_dc = dc
                subscriber_number = number[len(dc):]

                for segment in ndc_db.get(dc):

                    if subscriber_number.startswith(segment):
                        found_segment = segment

        if found_dc and found_segment:

            result = [elem for elem in numbering if elem["indicativo_destino"] == found_dc and elem["bloque"] == found_segment]

            # Sort results by date (newer first)
            result = sorted(result, key=lambda elem: elem['fecha'], reverse=True)
            print(f"Number {number}:")
            pprint.pp(result)
        else:
            print(f"Info for number {number} not found")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    input_args = parser.add_mutually_exclusive_group()
    input_args.add_argument("-n", "--number", type=str, help="The phone number to search")
    input_args.add_argument("-l", "--number-list", type=str, help="Text file containing a list of numbers to search (one number per line)")

    parser.add_argument("-nc", "--no-cache", action="store_true", help="Do not use cached file")

    main(parser.parse_args())
