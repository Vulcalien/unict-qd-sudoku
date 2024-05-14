# Modulo 'sudoku.py'

## Classe Sudoku
Questo modulo espone la classe 'Sudoku', che è in grado di generare una
griglia di gioco avente indizi che portano ad una soluzione unica.

La classe Sudoku espone le seguenti funzioni:
  - [\_\_init__(block_size: int)](#__init__)
  - [get_symbols() -> list[int]](#get_symbols)
  - [is_cell_inside(x: int, y: int) -> bool](#is_cell_inside)
  - [get_cell(x: int, y: int) -> int | None](#get_cell)
  - [is_fixed(x: int, y: int) -> bool](#is_fixed)
  - [generate_grid(iterations: int) -> int](#generate_grid)

### \_\_init__
`__init__(block_size: int)`

Il costruttore prende per parametro `block_size`, cioè il lato di uno
dei blocchi interni. Un altro modo di vedere questo parametro è la
radice quadrata del lato della griglia.

Ad esempio, se la griglia è 9x9, `block_size` dovrà valere 3.

### get_symbols
`get_symbols() -> list[int]`

`get_symbols()` restituisce una lista ordinata di tutti i simboli
inseribili nella griglia.

Ad esempio, se la griglia è 9x9, verrà restituito `range(1, 9+1)` (cioè
tutti gli interi da 1 a 9).

### is_cell_inside
`is_cell_inside(x: int, y: int) -> bool`

`is_cell_inside()` restituisce `True` se le coordinate date
corrispondono ad una cella della griglia, altrimenti `False`.

Se la griglia è NxN, verrà restituito `True` solo se sia `x` che `y`
appartengono al range [0, N-1].

### get_cell
`get_cell(x: int, y: int) -> int | None`

`get_cell` restituisce il simbolo collocato nella cella specificata,
oppure `None` se le coordinate sono invalide.

Il simbolo restituito è sempre parte della soluzione. Per capire se si
tratta di un indizio al giocatore, chiamare anche la funzione
(is_fixed)[#is_fixed].

### is_fixed
`is_fixed(x: int, y: int) -> bool`

`is_fixed` restituisce `True` se la cella specificata è marcata come
'fixed', altrimenti `False`. Una cella è marcata 'fixed' se questa è un
indizio e non dovrebbe quindi essere sovrascrivibile.

### generate_grid
`generate_grid`(iterations: int) -> int`

`generate_grid` genera una griglia completa ed una sua soluzione.
Inoltre, prova per `iterations` volte a diminuire il numero di indizi
presenti, mantenendo però l'unicità della soluzione. Restituisce infine
il numero di indizi che effettivamente sono stati risolti.

Vista la sua natura randomica, il tempo impiegato da questa funzione può
variare significativamente anche se `iterations` non cambia.

## Esempio
La classe Sudoku va usata per generare una griglia con tanto di
soluzione, e per conoscere quali sono gli indizi da dare al giocatore.

Nel seguente esempio, si genera una griglia 9x9 e se ne controlla la
soluzione.

```python
grid = Sudoku(3)

hints = (9 * 9) - grid.generate_grid(65)
print('ci sono ' + str(hints) + ' indizi')

# stampa la griglia (solo per debug)
print(grid)

# controlla se la cella (3, 5) è un indizio
x, y = 3, 5
if grid.is_fixed(x, y):
    print('la cella (' + str(x) + ', ' + str(y) + ') è un indizio')
else:
    print('la cella (' + str(x) + ', ' + str(y) + ') non è un indizio')

# leggi il valore della soluzione alla cella (6, 3), senza far caso al
# fatto che sia o meno un indizio
x, y = 6, 3
val = grid.get_cell(x, y)
print('la cella (' + str(x) + ', ' + str(y) + ') contiene ' + str(val))
```
