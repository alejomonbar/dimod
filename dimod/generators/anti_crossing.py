# Copyright 2020 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

from dimod.binary.binary_quadratic_model import BinaryQuadraticModel
from dimod.vartypes import Vartype

__all__ = ['anti_crossing_clique', 'anti_crossing_loops']


def anti_crossing_clique(num_variables: int) -> BinaryQuadraticModel:
    """Generate an anti-crossing problem with a single clique.

    Let ``N = num_variables // 2``. This function returns a binary quadratic
    model where half the variables, `[0, N)`, form a ferromagnetic clique, with
    each variable, `v`, also ferromagnetically interacting with one variable,
    `v+N`, of the remaining half of the variables, `[N, 2*N)`.

    All of the variables in the clique except variable `1` have a linear bias
    of `+1`, and all of the variables attached to the clique have a linear bias
    of `-1`.

    The ground state of this problem is therefore `+1` for all variables.

    Args:
        num_variables:
            Number of variables used to generate the problem. Must be an even
            number greater than or equal to 6.

    Returns:
        A binary quadratic model.

    Examples:
        >>> bqm = dimod.generators.anti_crossing_clique(6)
        >>> set(list(bqm.linear.values())[3:]) == set(bqm.quadratic.values()) == {-1.0}
        True
        >>> list(bqm.linear.values())[:3]
        [1.0, 0.0, 1.0]
    """

    if num_variables % 2 or num_variables < 6:
        raise ValueError('num_variables must be an even number >= 6')

    bqm = BinaryQuadraticModel(Vartype.SPIN)

    hf = int(num_variables / 2)
    for n in range(hf):
        for m in range(n + 1, hf):
            bqm.add_quadratic(n, m, -1)

        bqm.add_quadratic(n, n + hf, -1)

        bqm.add_linear(n, 1)
        bqm.add_linear(n + hf, -1)

    bqm.set_linear(1, 0)

    return bqm


def anti_crossing_loops(num_variables: int) -> BinaryQuadraticModel:
    """Generate an anti-crossing problem with two loops.

    This is the problem studied in [DJA]_.

    Note that for small values of ``num_variables``, the loops can be as small
    as a single edge.

    The ground state of this problem is `+1` for all variables.

    Args:
        num_variables:
            Number of variables used to generate the problem. Must be an even
            number greater than or equal to 8.

    Returns:
        A binary quadratic model.

    .. [DJA] Dickson, N., Johnson, M., Amin, M. et al. Thermally assisted
        quantum annealing of a 16-qubit problem. Nat Commun 4, 1903 (2013).
        https://doi.org/10.1038/ncomms2920

    Examples:
        The graphic lines of this example require the `Matplotlib <https://matplotlib.org>`_
        library.

        >>> import matplotlib as plt                   # doctest: +SKIP
        >>> import networkx as nx
        >>> bqm16 = dimod.generators.anti_crossing_loops(16)
        >>> g16 = dimod.to_networkx_graph(bqm16)
        >>> colors = [g16.nodes[n]['bias'] for n in g16.nodes]
        >>> nx.draw(g16, node_color=colors,
        ...         with_labels=True, cmap=plt.cm.autumn)   # doctest: +SKIP
        >>> plt.show()                                      # doctest: +SKIP
    """

    if num_variables % 2 or num_variables < 8:
        raise ValueError('num_variables must be an even number >= 8')

    bqm = BinaryQuadraticModel(Vartype.SPIN)

    hf = int(num_variables / 4)
    for n in range(hf):
        if n % 2 == 1:
            bqm.set_quadratic(n, n + hf, -1)

        bqm.set_quadratic(n, (n + 1) % hf, -1)
        bqm.set_quadratic(n + hf, (n + 1) % hf + hf, -1)

        bqm.set_quadratic(n, n + 2 * hf, -1)
        bqm.set_quadratic(n + hf, n + 3 * hf, -1)

        bqm.add_linear(n, 1)
        bqm.add_linear(n + hf, 1)
        bqm.add_linear(n + 2 * hf, -1)
        bqm.add_linear(n + 3 * hf, -1)

    bqm.set_linear(0, 0)
    bqm.set_linear(hf, 0)

    return bqm
