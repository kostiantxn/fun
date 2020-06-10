from fun.patterns import Case


def test_attributes_of_case():
    a, b = 'a', 'b'
    case = Case(a, b)

    assert case.pattern == a
    assert case.expression == b
