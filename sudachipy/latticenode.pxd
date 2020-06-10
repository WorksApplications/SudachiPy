cdef class LatticeNode:

    cdef int begin
    cdef int end
    cdef int total_cost
    cdef int word_id
    cdef bint _is_oov
    cdef LatticeNode best_previous_node
    cdef bint is_connected_to_bos
    cdef object extra_word_info
    cdef object undefined_word_info
    cdef bint is_defined
    cdef object lexicon
    cdef int left_id
    cdef int right_id
    cdef int cost

