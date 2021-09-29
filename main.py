import sys
from requests_b3 import RequestsB3
from datetime import date

def main():
    dt=date(2021,9,28)
    with RequestsB3() as requests:
        data = requests.request_economic_indicator(dt)
    print(data)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrompido pelo usuário (CTRL+C)...")
        sys.exit(0)