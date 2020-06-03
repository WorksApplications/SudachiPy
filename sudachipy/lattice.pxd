from .latticenode cimport LatticeNode

cdef class Lattice:

    cdef int size
    cdef int capacity
    cdef LatticeNode eos_node

    cdef list end_lists
    cdef object grammar
    cdef object eos_params
    cdef const short[:,:] connect_costs

    cpdef void resize(self, int size)
    cpdef void insert(self, int begin, int end, LatticeNode node)
    cdef void connect_node(self, LatticeNode r_node)
    cdef void connect_eos_node(self)
