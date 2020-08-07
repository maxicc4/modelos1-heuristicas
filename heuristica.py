# Si hay empate me quedo con el banco que tenga numero de indice menor
from time import time


def get_banco_mas_cercano(distancias, bancos_sin_visitar, banco_actual):
    distancia_min = 10000
    index_min = None
    for index_banco in bancos_sin_visitar:
        distancia_con_banco = distancias[banco_actual][index_banco]
        if distancia_con_banco < distancia_min:
            distancia_min = distancia_con_banco
            index_min = index_banco
    return index_min


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
        tramos.append({
            'origen': banco_actual,
            'destino': banco_mas_cercano,
            'distancia': distancias[banco_actual][banco_mas_cercano]
        })
        saldo_actual += transacciones[banco_mas_cercano]
        banco_actual = banco_mas_cercano
        bancos_visitados.append(banco_mas_cercano)
        bancos_sin_visitar.remove(banco_mas_cercano)
        bancos_sin_visitar_no_excluidos = bancos_sin_visitar.copy()
    else:
        # Si se pasa del saldo, lo excluyo solo para el banco actual
        bancos_sin_visitar_no_excluidos.remove(banco_mas_cercano)

    banco_mas_cercano = get_banco_mas_cercano(distancias, bancos_sin_visitar_no_excluidos, banco_actual)

# Agrego la vuelta a la sede
tramos.append({
    'origen': tramos[len(tramos) - 1]['destino'],
    'destino': 0,
    'distancia': distancias[tramos[len(tramos) - 1]['destino']][0]
})
distancia_total = 0
for tramo in tramos:
    distancia_total += tramo['distancia']

elapsed_time = time() - start_time

print('Distancia: ' + str(distancia_total))
print('Tour: ' + str(bancos_visitados))
print("Tiempo: %0.10f segundos" % elapsed_time)
