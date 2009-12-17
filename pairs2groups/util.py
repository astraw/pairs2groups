def take_not( T, j ):
    """remove jth element of T

    >>> T = [0, 1, 2, 3]
    >>> take_not( T, 1)
    [0, 2, 3]
    """
    return [ T[i] for i in range(len(T)) if i!=j ]

def is_list_of_sets_equal(A, B):
    """test whether list of sets A is equal to list of sets B

    >>> A = [frozenset([1])]

    >>> B = [frozenset([1])]
    >>> is_list_of_sets_equal(A, B)
    True

    >>> B = [frozenset([2])]
    >>> is_list_of_sets_equal(A, B)
    False

    >>> B = [frozenset([1]),frozenset([2])]
    >>> is_list_of_sets_equal(A, B)
    False

    >>> B = []
    >>> is_list_of_sets_equal(A, B)
    False

    """
    if len(A) != len(B):
        return False
    As = frozenset(A)
    Bs = frozenset(B)
    try:
        Cs = As - Bs
    except:
        # return False, but what error to catch?
        raise
    if len(Cs) != 0:
        return False
    return True

def get_k_element_subsets( k, T ):
    """get all subsets of T of length k

    Returns len(T) choose k subsets.
    """
    if k == len(T):
        result = [T]
    elif k == len(T)-1:
        Tl = list(T)
        result = [ frozenset(take_not(Tl,j)) for j in range(len(T)) ]
    else:
        raise NotImplementedError('')
    return result

def test_get_k_element_subsets():
    T = frozenset([0,1,2,3])

    k = 4
    expected = [ frozenset([0,1,2,3]) ]
    actual = get_k_element_subsets( k, T )
    assert is_list_of_sets_equal(actual,expected)

    k = 3
    expected = [ frozenset([1,2,3]), frozenset([0,2,3]), frozenset([0,1,3]), frozenset([0,1,2]) ]
    actual = get_k_element_subsets( k, T )
    assert is_list_of_sets_equal(actual,expected)

def get_all_pairs(S):
    """get a list of all pairs of values of S

    >>> get_all_pairs( [0,1,2,3] )
    [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    """
    result = []
    Sl = list(S)
    for i,Si in enumerate(Sl):
        for Sj in Sl[i+1:]:
            result.append( (Si,Sj) )
    return result

def remove_overlapping_subsets( S ):
    """given a list of sets S, find the minimal list T of unique sets
    such that every set in S is a subset of a set in T."""

    # XXX need to actually test!

    T = []
    for i,elem in enumerate(S):
        present_later = False
        for test_elem in take_not(S,i):
            if len(elem - test_elem) == 0:
                present_later = True
                break
        if not present_later:
            T.append(elem)
    return T
