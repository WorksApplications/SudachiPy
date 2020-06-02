from .latticenode cimport LatticeNode

cdef class Lattice:

    cdef int size
    cdef int capacity
    cdef LatticeNode eos_node

    cdef list end_lists
    cdef object grammar
    cdef object eos_params
    #cdef const short[:,:] connect_costs

    cdef void resize_c(self, int size)
    cdef void insert_c(self, int begin, int end, LatticeNode node)
    cdef void connect_node(self, LatticeNode r_node)
