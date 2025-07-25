import re
from collections import Counter

# Cambia la ruta al archivo de log según corresponda
def analizar_logs(ruta_log, endpoint=None, ip=None):
    with open(ruta_log, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    filtro = []
    for linea in lineas:
        if endpoint and endpoint not in linea:
            continue
        if ip and ip not in linea:
            continue
        filtro.append(linea.strip())
    print(f"Total de coincidencias: {len(filtro)}")
    # Contar por IP
    ips = [re.search(r'(\d+\.\d+\.\d+\.\d+)', l) for l in filtro]
    ips = [m.group(1) for m in ips if m]
    print("Top IPs:", Counter(ips).most_common(5))
    # Contar por endpoint
    endpoints = [re.search(r'"GET (.*?) HTTP', l) for l in filtro]
    endpoints = [m.group(1) for m in endpoints if m]
    print("Top endpoints:", Counter(endpoints).most_common(5))
    # Mostrar ejemplos
    print("Ejemplo de líneas:")
    for l in filtro[:5]:
        print(l)

if __name__ == "__main__":
    # Ejemplo de uso:
    # analizar_logs('ruta/a/tu/logfile.log', endpoint='/api/perfilCliente/perfilCliente', ip='10.111.65.121')
    analizar_logs('server.log', endpoint='/api/perfilCliente/perfilCliente')
