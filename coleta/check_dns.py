import socket

SUPABASE_DB_HOST = "db.nflmvptqgicabovfmnos.supabase.co"

print(f"Tentando resolver o host: {SUPABASE_DB_HOST}")

try:
    # Tenta resolver para IPv4
    ipv4_address = socket.gethostbyname(SUPABASE_DB_HOST)
    print(f"Resolução IPv4 bem-sucedida: {ipv4_address}")
except socket.gaierror as e:
    print(f"Falha na resolução IPv4: {e}")

try:
    # Tenta resolver para IPv6
    # socket.getaddrinfo retorna uma lista de tuplas para diferentes tipos de socket
    # O primeiro elemento da tupla é a família de endereços (AF_INET ou AF_INET6)
    # O quarto elemento é o endereço (IP, porta)
    ipv6_addresses_info = socket.getaddrinfo(SUPABASE_DB_HOST, None, socket.AF_INET6)
    ipv6_addresses = [addr_info[4][0] for addr_info in ipv6_addresses_info]
    print(f"Resolução IPv6 bem-sucedida: {ipv6_addresses}")
except socket.gaierror as e:
    print(f"Falha na resolução IPv6: {e}")

print("Verificação de DNS concluída.")