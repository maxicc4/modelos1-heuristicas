from time import time

# Si hay empate me quedo con el banco que tenga numero de indice menor
def get_banco_mas_cercano(distancias, bancos_sin_visitar, banco_actual):
    distancia_min = 10000
    index_min = None
    for index_banco in bancos_sin_visitar:
        distancia_con_banco = distancias[banco_actual][index_banco]
        if distancia_con_banco < distancia_min:
            distancia_min = distancia_con_banco
            index_min = index_banco
    return index_min

# Se le pasa un tour y devuelve la distancia total
def distancia_total(distancias, bancos_visitados):
    anterior = bancos_visitados[0]
    distancia = 0
    for actual in bancos_visitados[1:]:
        distancia += distancias[anterior][actual]
        anterior = actual
    # Vuelta a la sede
    distancia += distancias[bancos_visitados[len(bancos_visitados) - 1]][0]
    return distancia

def swap_2opt(tour, i, k):
    aux = tour[i+1:k+1]
    nuevo_tour = tour[0:i+1]+aux[::-1]
    if k != len(tour)-1:
        nuevo_tour += tour[k+1:]
    return nuevo_tour

def cumple_restricciones_transacciones(transacciones, tour, max_dinero):
    dinero_acumulado = 0
    for banco in tour:
        dinero_acumulado += transacciones[banco]
        if dinero_acumulado < 0 or dinero_acumulado > max_dinero:
            return False
    return True

start_time = time()

distancias = [
    [None, 154, 151, 120, 104, 119, 35, 47, 13, 124, 39],
    [154, None, 99, 34, 50, 96, 78, 102, 39, 50, 98],
    [151, 99, None, 30, 46, 94, 20, 30, 66, 56, 100],
    [120, 34, 30, None, 16, 93, 30, 20, 57, 85, 39],
    [104, 50, 46, 16, None, 77, 23, 93, 111, 54, 29],
    [119, 96, 94, 93, 77, None, 58, 84, 17, 85, 38],
    [35, 78, 20, 30, 23, 58, None, 87, 98, 23, 76],
    [47, 102, 30, 20, 93, 84, 87, None, 54, 87, 91],
    [13, 39, 66, 57, 111, 17, 98, 54, None, 45, 10],
    [124, 50, 56, 85, 54, 85, 23, 87, 45, None, 22],
    [39, 98, 100, 39, 29, 38, 76, 91, 10, 22, None]
]

transacciones = [0, 5, -20, 30, 20, -10, -20, 10, -25, 10, 5]
MAX_DINERO = 50
saldo_actual = 0

bancos_sin_visitar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
bancos_visitados = []
tramos = []
# Empiezo por la sede (0)
banco_actual = 0
bancos_visitados.append(banco_actual)

banco_mas_cercano = get_banco_mas_cercano(distancias, bancos_sin_visitar, banco_actual)

bancos_sin_visitar_no_excluidos = bancos_sin_visitar.copy()
while len(bancos_sin_visitar_no_excluidos):
    if (saldo_actual + transacciones[banco_mas_cercano] > 0) and (
            saldo_actual + transacciones[banco_mas_cercano] <= MAX_DINERO):
        saldo_actual += transacciones[banco_mas_cercano]
        banco_actual = banco_mas_cercano
        bancos_visitados.append(banco_mas_cercano)
        bancos_sin_visitar.remove(banco_mas_cercano)
        bancos_sin_visitar_no_excluidos = bancos_sin_visitar.copy()
    else:
        # Si se pasa del saldo, lo excluyo solo para el banco actual
        bancos_sin_visitar_no_excluidos.remove(banco_mas_cercano)

    banco_mas_cercano = get_banco_mas_cercano(distancias, bancos_sin_visitar_no_excluidos, banco_actual)

elapsed_time = time() - start_time
distancia = distancia_total(distancias, bancos_visitados)
print('\n-------HEURISTICA DE CONSTRUCCIÓN-------')
print('Distancia: ' + str(distancia))
print('Tour: ' + str(bancos_visitados))
print("Tiempo: %0.10f segundos" % elapsed_time)


print('\n-------HEURISTICA DE MEJORAMIENTO-------')
start_time = time()
hubo_cambio_tour = True
while hubo_cambio_tour:
    hubo_cambio_tour = False
    for i in range(len(bancos_visitados)-1):
        for k in range(i+1, len(bancos_visitados)):
            nuevo_tour = swap_2opt(bancos_visitados, i, k)
            nueva_distancia = distancia_total(distancias, nuevo_tour)
            if nueva_distancia < distancia and cumple_restricciones_transacciones(transacciones, nuevo_tour, MAX_DINERO):
                bancos_visitados = nuevo_tour
                distancia = nueva_distancia
                hubo_cambio_tour = True
                print('Nuevo tour encontrado')
                print('Distancia: ' + str(distancia))
                print('Tour: ' + str(bancos_visitados)+'\n')
                break
        if hubo_cambio_tour:
            break

elapsed_time = time() - start_time
print("Tiempo: %0.10f segundos" % elapsed_time)
