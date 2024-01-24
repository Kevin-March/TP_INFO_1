from pyformlang.pda import PDA, State, StackSymbol, Symbol, Epsilon
import graphviz

pda= PDA()
pda.add_transition("q0", "a", "Z", "q1", ("X", "Z"))
pda.add_transition("q1", "b", "X", "q2", ("X",))
pda.add_transition("q2", Epsilon(), "Z", "qf", ("Z",))

pda.set_start_state(State("q0"))
pda.set_start_stack_symbol(StackSymbol("Z"))
pda.add_final_state(State("qf"))

pda_final_state = pda.to_empty_stack()
pda.write_as_dot("test.dot")
pda_final_state.write_as_dot("test_final.dot")
# Lee el archivo DOT generado por write_as_dot
with open("test_final.dot", "r") as dot_file:
    dot_code = dot_file.read()

# Crea un objeto Digraph de Graphviz desde el código DOT
graph = graphviz.Source(dot_code, format='png')

# Guarda la imagen en un archivo
graph.render('pda_graph', format='png', cleanup=True)

print("El gráfico del PDA se ha generado y guardado en 'pda_graph.png'.")