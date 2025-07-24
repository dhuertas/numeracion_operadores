# Numeracion Operadores
Python utility script to find public phone operator information from a phone number (Spain only).

The script searches the database from Comisión Nacional de los Mercados y la Competencia (CNMC):

[https://numeracionyoperadores.cnmc.es/numeracion](https://numeracionyoperadores.cnmc.es/numeracion)

# Examples

Show script help:

```bash
python numeracion_operadores.py -h

usage: numeracion_operadores.py [-h] [-n NUMBER | -l NUMBER_LIST]

options:
  -h, --help            show this help message and exit
  -n NUMBER, --number NUMBER
                        The phone number to search
  -l NUMBER_LIST, --number-list NUMBER_LIST
                        Text file containing a list of numbers to search (one number per line)
```

Search for a number:

```bash
python numeracion_operadores.py -n 123456789

Number 123456789:
[{'operador': '...',
  'nif': '...',
  'fecha': 'YYYY-mm-dd 00:00:00.000',
  'estado': 'Asignado',
  'digitos': None,
  'comentario': None,
  'tipo': None,
  'indicativo_destino': '123',
  'bloque': '45',
  'provincia': '...',
  'tipo_num': 'geográfica',
  'subbloque': None,
  'distrito': None,
  'cod_distrito': None,
  'servicio': None,
  'tipo_red': None,
  'nrn': None}]
```
