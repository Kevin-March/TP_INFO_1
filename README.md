<h1> Trabajo Practico INFO 1</h1>

<p>objetivo: Hacer un programa que construya un PDA con estados finales a una PDA por reconocimiento por pila vacía.</p>

<h2>Requisitos</h2>
<p> instalar graphviz y pygraphviz </p>

<h2>Funcionamiento</h2>
<p2> El usuario es preguntado cuantos nodos o estados tiene su PDA, seguido de esto se le pregunta cual de estos estados es el estado inicial, luego de esto se le pide que escriba el Alfabeto del PDA y el Alfabeto de la pila (OBS: Aqui hay que poner el simbolo inical de la pila).
Luego pedimos que escriba todas las transiciones de su PDA para asi poder ser graficado <b> El formato para la carga de las transcisiones es: (estado_actual, caracter_lee, pila_contenido)=(estado_destino, cola_contenido)</b> esta hecho de esta forma debido a que la terminal usualmente no le gustan los caracteres griegos para la carga asi que quitamos sigma.
Obs: Se cargan uno a uno las transciciones, mas que nada pq asi me parecia mejor.
Por ultimo se le pregunta cuales son los estados finales, con esto se genera tanto un archivo.DOT como un archivo .PNG llamado pda_final_state para poder corroborar que el PDA final state este correcto.</p2>
<p2>Luego se llama a la Funcion generar_empty_stack(), que basicamente codifica todos los datos del PDA final_state para que se pueda crear un PDA empty stack</p2>
