import numpy as np
from sklearn.preprocessing import PolynomialFeatures


def poly_reg(source, target, degree):
    assert len(source) == len(target)
    n1 = len(source[0])
    assert all(n1 == len(e) for e in source)
    n2 = len(target[0])
    assert all(n2 == len(e) for e in target)

    source_vec = np.array(source).reshape(-1, n1)
    target_vec = np.array(target).reshape(-1, n2)

    poly = PolynomialFeatures(degree=degree, include_bias=True)
    source_poly = poly.fit_transform(source_vec)

    coeffs, _, _, _ = np.linalg.lstsq(source_poly, target_vec, rcond=None)

    num_features = source_poly.shape[1]
    coeffs = coeffs.reshape((num_features, 3))

    return coeffs


def apply_poly(source, coeffs, degree):
    n1 = len(source[0])
    assert all(n1 == len(e) for e in source)

    poly = PolynomialFeatures(degree=degree, include_bias=True)
    source_vec = np.array(source).reshape(-1, n1)
    source_poly = poly.fit_transform(source_vec)
    result_vec = source_poly.dot(coeffs)
    return result_vec


# example
# source = np.array([[0, 0], [0, 1], [1, 0]])
# target = np.array([[0, 0, 0], [0, 10, 0], [10, 0, 0]])
#
# c = poly_reg(source, dest, 2)
# print(c)
#
# r = apply_poly([[1,1], [2,2]], c, 2)
# print(r)