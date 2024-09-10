import time
from simpleai.search import SearchProblem, astar
from simpleai.search.viewers import WebViewer

GOAL = (1, 2, 3,
       4, 5, 6,
       7, 8, 0)  # 0 es el espacio en blanco


class PuzzleProblem(SearchProblem):
   def actions(self, state):
       return ["Derecha", "Izquierda", "Arriba", "Abajo"]  # Los 4 movimientos posibles

   def result(self, state, action):
       zero_idx = state.index(0)  # Indice del espacio en blanco
       row = zero_idx // 3  # Fila del espacio en blanco
       col = zero_idx % 3  # Columna del espacio en blanco

       # Asignamos la nueva fila/columna segun la acción
       if action == "Derecha":
           new_row, new_col = row, col + 1
       elif action == "Izquierda":
           new_row, new_col = row, col - 1
       elif action == "Arriba":
           new_row, new_col = row - 1, col
       elif action == "Abajo":
           new_row, new_col = row + 1, col
       else:
           new_row, new_col = row, col

       if 0 <= new_row < 3 and 0 <= new_col < 3:  # Si la nueva fila/columna esta dentro del tablero
           new_idx = new_row * 3 + new_col  # El nuevo índice del valor a mover
           new_state = list(state)  # Copiamos el estado actual
           new_state[zero_idx], new_state[new_idx] = new_state[new_idx], new_state[
               zero_idx]  # Intercambiamos el espacio en blanco y el número
           return tuple(new_state)  # Devolvemos la tupla modificada
       else:  # Si la nueva fila/columna está fuera del tablero
           return state  # Devolvemos el estado actual

   def is_goal(self, state):
       return state == GOAL

   def heuristic(self, state):
       distance = 0
       for i in range(9):
           if state[i] != 0:
               current_row, current_col = divmod(i, 3)
               goal_row, goal_col = divmod(GOAL.index(state[i]), 3)
               distance += abs(current_row - goal_row) + abs(current_col - goal_col)
       return distance


problem_manhattan = PuzzleProblem(initial_state=(1, 2, 3, 4, 5, 6, 7, 0, 8))
start_time = time.time()
result_manhattan = astar(problem_manhattan, viewer=WebViewer(), graph_search=False)
end_time = time.time()
execution_time_manhattan = end_time - start_time
print("Result using Manhattan distance heuristic:")
print("State:", result_manhattan.state)
print("Path:", result_manhattan.path())
print("Path length:", len(result_manhattan.path()))
print("Execution time:", execution_time_manhattan)