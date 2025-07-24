from urllib.request import Request, urlopen
import argparse
import json
import pprint

def main(opts):
    """
    Script that tries to identify which company operates a given Spanish phone number

    Sources:
    - https://avance.digital.gob.es/es-ES/Servicios/Numeracion/Documents/Descripcion_PNN.pdf
    - https://avance.digital.gob.es/es-ES/Servicios/Numeracion/Documents/Guia_Numeracion.pdf

    """
    blocked_numbers = []
    numbering = {}

    if opts.number_list:
        with open(opts.number_list, "r") as file:
            blocked_numbers = [line.rstrip() for line in file]

    if opts.number:
        blocked_numbers.append(str(opts.number))

    response = urlopen(Request(url='https://numeracionyoperadores.cnmc.es/api/numeracion/get_busqueda_numeracion', headers={'User-Agent': 'Mozilla/5.0'}))
    if response.getcode() == 200:
        numbering = json.loads(response.read().decode('utf-8'))
    else:
        print("failed to get numbering db")

        # Alternatively, download the file externaly and enable the comment code below
        #
        # with open('busqueda_numeracion.json', 'r') as file:
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

    for number in blocked_numbers:

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

    main(parser.parse_args())
