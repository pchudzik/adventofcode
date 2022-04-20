from _24_balance import quantum_entanglement, find_qes


def test_quantum_entanglement():
    assert quantum_entanglement([11, 9]) == 99
    assert quantum_entanglement([10, 9, 1]) == 90


def test_find_smallest_qe_3_groups():
    packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    assert find_qes(packages, 3) == 99


def test_find_smallest_qe_4_groups():
    packages = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    assert find_qes(packages, 4) == 44
