from functools import lru_cache
from collections import deque

# 1️⃣ Can I Win - Juego de cartas interactivo
def can_i_win_game():
    print("Juego: Can I Win (elige números para llegar a la suma objetivo)")
    max_choosable_int = int(input("Elige el máximo número disponible (ej: 10): "))
    desired_total = int(input("Elige la suma objetivo (ej: 11): "))

    if desired_total <= 0:
        print("Objetivo muy bajo, ganas automáticamente.")
        return
    if (max_choosable_int * (max_choosable_int + 1)) // 2 < desired_total:
        print("No es posible alcanzar el total, pierde el jugador 1.")
        return

    @lru_cache(None)
    def dfs(used_mask, current_total):
        for i in range(max_choosable_int):
            if not (used_mask & (1 << i)):
                if current_total + i + 1 >= desired_total:
                    return True
                if not dfs(used_mask | (1 << i), current_total + i + 1):
                    return True
        return False

    used_mask = 0
    current_total = 0
    player_turn = 1

    while True:
        print(f"\nSuma actual: {current_total}")
        print(f"Turno del jugador {player_turn}")
        print("Números disponibles:", [i+1 for i in range(max_choosable_int) if not (used_mask & (1 << i))])
        
        if player_turn == 1:
            # Jugador humano
            try:
                choice = int(input("Elige un número disponible: "))
            except:
                print("Entrada inválida, intenta otra vez.")
                continue
            if choice < 1 or choice > max_choosable_int or (used_mask & (1 << (choice-1))):
                print("Número no válido o ya usado. Intenta de nuevo.")
                continue
        else:
            # Jugador computadora (usa dfs para ganar si puede)
            choice = None
            for i in range(max_choosable_int):
                if not (used_mask & (1 << i)):
                    if current_total + i + 1 >= desired_total:
                        choice = i + 1
                        break
                    if not dfs(used_mask | (1 << i), current_total + i + 1):
                        choice = i + 1
                        break
            if choice is None:
                for i in range(max_choosable_int):
                    if not (used_mask & (1 << i)):
                        choice = i + 1
                        break
            print(f"Computadora elige: {choice}")

        current_total += choice
        used_mask |= (1 << (choice-1))

        if current_total >= desired_total:
            print(f"Jugador {player_turn} gana!")
            break

        player_turn = 2 if player_turn == 1 else 1


# 2️⃣ Juego de casillas: "Recolecta ítems"
def shortest_path_game():
    print("Juego: Recolecta ítems en el mapa (nodos conectados)")
    n = int(input("Número de nodos en el grafo: "))
    print("Introduce las conexiones (lista de vecinos por nodo):")
    graph = []
    for i in range(n):
        vecinos = input(f"Nodo {i} vecinos (separados por espacios): ").strip()
        if vecinos:
            vecinos_list = list(map(int, vecinos.split()))
        else:
            vecinos_list = []
        graph.append(vecinos_list)

    full_mask = (1 << n) - 1
    queue = deque()
    seen = set()
    queue.append((0, 1 << 0, 0))  # (pos, mask, dist)
    seen.add((0, 1 << 0))

    print("\nEstás en el nodo 0. Debes visitar todos los nodos.")
    while queue:
        pos, mask, dist = queue.popleft()
        print(f"Estás en nodo {pos}, visitados: {bin(mask)}, pasos: {dist}")
        if mask == full_mask:
            print(f"¡Has visitado todos los nodos en {dist} pasos!")
            return
        vecinos = graph[pos]
        print(f"Nodos conectados a {pos}: {vecinos}")
        choice = None
        while choice not in vecinos:
            try:
                choice = int(input(f"Elige nodo conectado para moverte: "))
                if choice not in vecinos:
                    print("Ese nodo no está conectado. Intenta otra vez.")
            except:
                print("Entrada inválida. Intenta de nuevo.")
        next_mask = mask | (1 << choice)
        if (choice, next_mask) not in seen:
            seen.add((choice, next_mask))
            queue.append((choice, next_mask, dist + 1))
    print("No se pudo visitar todos los nodos.")


# 3️⃣ Juego mental: "Elige el último número"
def last_number_game():
    n = int(input("Juego mental: Elige números del 1 al n. ¿Cuál es n?: "))

    @lru_cache(None)
    def dp(mask):
        for i in range(n):
            if not (mask & (1 << i)):
                if not dp(mask | (1 << i)):
                    return True
        return False

    mask = 0
    player_turn = 1
    print(f"\nNúmeros disponibles: {[i+1 for i in range(n)]}")

    while True:
        print(f"\nTurno del jugador {player_turn}")
        disponibles = [i+1 for i in range(n) if not (mask & (1 << i))]
        print(f"Números disponibles: {disponibles}")
        if not disponibles:
            print(f"Jugador {3 - player_turn} gana porque el jugador {player_turn} no tiene movimientos!")
            break

        if player_turn == 1:
            try:
                choice = int(input("Elige un número disponible: "))
            except:
                print("Entrada inválida, intenta otra vez.")
                continue
            if choice not in disponibles:
                print("Número no disponible, intenta de nuevo.")
                continue
        else:
            choice = None
            for i in disponibles:
                if not dp(mask | (1 << (i - 1))):
                    choice = i
                    break
            if choice is None:
                choice = disponibles[0]
            print(f"Computadora elige: {choice}")

        mask |= (1 << (choice - 1))
        player_turn = 2 if player_turn == 1 else 1


# Menú principal para elegir el juego
def main():
    while True:
        print("\nElige el juego para jugar:")
        print("1. Can I Win (Juego de cartas)")
        print("2. Recolecta ítems en el mapa")
        print("3. Elige el último número (Juego mental)")
        print("0. Salir")

        opcion = input("Opción: ")
        if opcion == "1":
            can_i_win_game()
        elif opcion == "2":
            shortest_path_game()
        elif opcion == "3":
            last_number_game()
        elif opcion == "0":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()
