from creationmatrix import matrix


datap = int(input("enter nomber of p :"))
datat = int(input("enter nomber of t :"))
post_matrix = matrix()
pre_matrix = matrix()

print("creation of post_matrix")
post_matrix.CreateMat(datap, datat)
print("display of post_matrix")
post_matrix.ShowMat()
print("creation of pre_matrix")
pre_matrix.CreateMat(datap, datat)
print("display of pre_matrix")
pre_matrix.ShowMat()
print("MatrixC is matrix of simulation :")
res = matrix.RdpSim(post_matrix.matrix,pre_matrix.matrix )
print("display of res")
for row in res:
        print(' '.join(map(str, row)))

connections = matrix.generate_graph(post_matrix.matrix, pre_matrix.matrix)
matrix.show_graph(connections)
matrix.visualize_graph(connections)


initial_marking = [1, 0, 0, 0] #marquage initail


marking_history = matrix.RspSim(pre_matrix.matrix, post_matrix.matrix, initial_marking)

matrix.visualize_marking_evolution(marking_history)


matrix.visualize_marking_graph(pre_matrix.matrix, post_matrix.matrix, marking_history)