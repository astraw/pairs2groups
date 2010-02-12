"""find homogeneous groups of items based on pairwise information

A motivating example
--------------------

Suppose you have performed several experiments from four treatments
(treatments 1,2,3, and 4). From each treatment, you have collected
many independent samples. The question is into what groups of
'statistically not different' the results may be divided.

This package, pairs2groups, finds the groups into which the treatments
may be divided such that each member of a group is not significantly
different than other members in the group.

A picture may make this more clear. Samples from each treatment are
plotted below in a boxplot. The letters below each box describe the
groups each treatment is a member of. For example, all treatments in
group 'a' are not statistically significantly different than each
other.

.. plot::

   import matplotlib.pyplot as plt
   import matplotlib.transforms as mtransforms
   import numpy as np
   from pairs2groups import label_homogeneous_groups

   np.random.seed(2)
   inc = 0.1
   e1 = np.random.uniform(0,1, size=(500,))
   e2 = np.random.uniform(0,1, size=(500,))
   e3 = np.random.uniform(0,1 + inc, size=(500,))
   e4 = np.random.uniform(0,1 + 2*inc, size=(500,))

   treatments = [e1,e2,e3,e4]
   group_info = label_homogeneous_groups(treatments)

   fig = plt.figure()
   ax = fig.add_subplot(111)
   pos = np.array(range(len(treatments)))+1
   bp = ax.boxplot( treatments, notch=0, sym='k+', patch_artist=True,
                    positions=pos )
   text_transform= mtransforms.blended_transform_factory(ax.transData,
                                                         ax.transAxes)
   for i,label in enumerate(group_info['group_strings']):
       ax.text( pos[i], 0.02, label,
                transform=text_transform,ha='center')
   ax.set_xlabel('treatment')
   ax.set_ylabel('response')
   ax.set_ylim(-0.2, 1.4)
   plt.setp(bp['whiskers'], color='k',  linestyle='-' )
   plt.setp(bp['fliers'], markersize=3.0)
   fig.subplots_adjust(right=0.99,top=0.99)
   plt.show()


Problem definition
------------------

The problem is how to find the (minimal but complete) set of
homogeneous groups of a collection of items. A homogeneous group is
defined to have no member that is 'different' (defined below) than any
other member.

Consider the problem of *n* items and pairwise knowledge of whether
each item is either 'different' or 'not different' from every other
item. This property of 'different' is commutative (A is different than
B means B is different than A), but not transtive (A is different than
B is different than C does not specify the relation between A and C).

How to construct groups such that every member population of a group
is not different than the other populations in the group?

Development information
-----------------------

The source code and issue tracker for this library are at
http://github.com/astraw/pairs2groups

"""
import pairs2groups.util as util

def find_homogeneous_groups( different_pairs, N_items ):
    """Find all homogeneous groups of not-different pairs.

    The algorithm used is as follows, where *S* is the set of all *n*
    items.

     1. Set *k* equal *n*, and *T* equal *S*.

     2. Set *m* equal *n* choose *k*. Take all (*m* in number) *k* element
        subsets of *T*. Denote the *i*th subset of *T* as *U_i*.

     3. For *i* in (0, ..., m-1):

       3a. If no pair within *U_i* is different, then *U_i* is a
           group. Remember it.

       3b. Else, set *k* equal *k-1*, and *T* equal *U_i*. Goto 2.

    Parameters
    ----------

    different_pairs : list of 2-tuples
        A list of pairs specifying different between two items
    N_popupations : int
        The number of items in the population

    Example
    -------

      >>> diff = [ (0,2) ]
      >>> N = 3
      >>> find_homogeneous_groups( diff, N )
      [(1, 2), (0, 1)]

    """
    # setup initial values
    S = frozenset( range(N_items) )
    k = N_items
    assert k == len(S)

    T = S.copy()
    different_pairs = set([ util.UnorderedPair((p[0],p[1]))
                              for p in different_pairs])

    # define the recursive function
    def _f( T, k, already_descended ):
        this_good_sets = []
        U = util.get_k_element_subsets( k, T )
        m = len(U)
        for i, U_i in enumerate(U):
            if U_i in already_descended:
                continue
            else:
                already_descended.add(U_i)
            pairs = frozenset(util.get_all_pairs(U_i))
            if len( pairs.intersection( different_pairs )):
                if k >= 3:
                    child_good_sets = _f( U_i, k-1, already_descended)
                    this_good_sets.extend( child_good_sets )
            else:
                this_good_sets.append( U_i )
        return this_good_sets

    # call the recursive function
    good_sets = _f(T,k,set())
    # remove non-unique by a round-trip through set
    good_sets = list(set(good_sets))
    final_sets = util.remove_overlapping_subsets( good_sets )
    return [ tuple(f) for f in final_sets]

def test_find_homogeneous_groups():
    N = 2
    diff = [ (0,1) ]
    expected = []
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 2
    diff = []
    expected = [ (0,1) ]
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 3
    diff = []
    expected = [ (0,1,2) ]
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 3
    diff = [ (0,1) ]
    expected = [ (0,2), (1,2) ]
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 3
    diff = [ (1,2) ]
    expected = [ (0,1), (0,2) ]
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 3
    diff = [ (0,2) ]
    expected = [ (0,1), (1,2) ]
    actual = find_homogeneous_groups( diff, N )
    assert util.is_list_of_sets_equal(actual,expected)

    N = 5
    diff = [ (0,2),
             (0,3),
             (2,3),
             ]
    find_homogeneous_groups( diff, N )

def test_find_homogeneous_groups_pathology1():
    # I was having trouble with this set of data

    diff_pairs = [(0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (1, 5), (1, 6),
                  (1, 7), (1, 8), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
                  (3, 5), (3, 6), (3, 7), (3, 8), (4, 6), (4, 7), (4, 8),
                  (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8)]
    N = 9
    groups = find_homogeneous_groups( diff_pairs, N )
    for group in groups:
        for a,b in diff_pairs:
            if a in group:
                assert b not in group

def test_find_homogeneous_groups_pathology2():
    # I was having trouble with this set of data

    diff_pairs = [(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 8),
                  (0, 11), (1, 2), (1, 3), (1, 5), (1, 8), (1, 11),
                  (5, 9), (5, 10), (5, 12), (9, 11)]
    N = 13
    groups = find_homogeneous_groups( diff_pairs, N )
    for group in groups:
        for a,b in diff_pairs:
            if a in group:
                assert b not in group

def label_homogeneous_groups(populations,
                             significance_level=0.05,
                             two_tailed = True,
                             force_letter = True,
                             ):
    """perform statistical comparisons and call :func:`find_homogeneous_groups`

    The statistical test used is the Mann Whitney U.

    Parameters
    ----------
    populations : A sequence of of sequences
        The list of populations to analyze.
    significance_level : float, optional
        The significance level required to determine two groups different.
    two_tailed : bool, optional
        Whether the comparison is two-tailed.
    force_letter : bool, optional
        If true (the default), each population gets assigned a letter

    Returns
    -------

    group_info : dictionary

        These keys are returned: 'groups' specifies the population
        indices for each group, 'group_strings' assigns letters to
        each group and returns a list of strings for each item,
        'p_values' is a matrix of p values, 'medians' is the median of
        each population.

    Examples
    --------

    This example generates four populations. Three from the same
    distribution, and the last from a different distribution. Then,
    :func:`label_homogeneous_groups` is used to find which of these
    populations belong to statistically non significantly different
    groups.

    >>> import numpy as np
    >>> pop1 = np.random.normal(size=(100,))
    >>> pop2 = np.random.normal(size=(100,))
    >>> pop3 = np.random.normal(size=(100,))
    >>> pop4 = np.random.normal(size=(100,)) + 2
    >>> populations = [pop1, pop2, pop3, pop4]
    >>> group_info = label_homogeneous_groups(populations)
    >>> group_info                  # doctest: +SKIP
    {'p_values': array([[        NaN,  0.578,  0.705 ,  0.        ],
                        [ 0.578,         NaN,  0.855,  0.        ],
                        [ 0.705 ,  0.855,         NaN,  0.        ],
                        [ 0.        ,  0.        ,  0.        ,         NaN]]),
    'medians': [0.071, -0.010, -0.0156, 2.054],
    'group_strings': ['a', 'a', 'a', ''], 'groups': [(0, 1, 2)]}

    """
    import scipy.stats
    import numpy as np

    # create pairwise differences
    n_comparisons = (len(populations)**2 - len(populations))/2

    diff_pairs = []
    p_values = np.nan*np.ones( (len(populations), len(populations)))
    medians = [ np.median( x ) for x in populations ]
    for i in range(len(populations)):
        for j in range(len(populations)):
            if not i < j:
                continue
            pair = (i,j)
            A = populations[i]
            B = populations[j]

            U,p1=scipy.stats.mannwhitneyu(A,B)
            if two_tailed:
                p = p1*2
            else:
                p = p1

            p_values[i,j] = p
            sig = significance_level/n_comparisons # Bonferroni correction
            if p < sig:
                different = True
            else:
                different = False

            if different:
                diff_pairs.append( pair )
    groups = find_homogeneous_groups( diff_pairs, len(populations) )

    group_strs = []

    group_order = -1*np.ones((len(groups),),dtype=np.int)
    next_group = 0
    for i in range(len(populations)):
        mystr = []
        for j in range(len(groups)):
            if i in groups[j]:
                order = group_order[j]
                if order==-1:
                    order = next_group
                    next_group += 1
                    group_order[j] = order
                mystr += [ chr( order+ord('a') ) ]
        if len(mystr):
            mystr.sort()
            mystr = ''.join(mystr)
        else:
            if force_letter:
                order = next_group
                next_group += 1
                mystr = chr( order+ord('a') )
            else:
                mystr = ''
        group_strs.append( mystr )

    # make the p_value matrix symmetric
    for i in range(len(populations)):
        for j in range(len(populations)):
            if not i > j:
                continue
            p_values[i,j] = p_values[j,i]

    group_info = dict( groups=groups,
                       group_strings=group_strs,
                       p_values=p_values,
                       medians=medians,
                       )
    return group_info
