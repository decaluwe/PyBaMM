#
# Tests for the Base Parameter Values class
#
import pybamm

import unittest
import numpy as np


class TestBaseModel(unittest.TestCase):
    def test_read_parameters_csv(self):
        data = pybamm.BaseParameterValues().read_parameters_csv(
            "input/parameters/lead-acid/default.csv"
        )
        self.assertEqual(data["R"], 8.314)

    def test_init(self):
        # from dict
        param = pybamm.BaseParameterValues({"a": 1})
        self.assertEqual(param["a"], 1)
        # from file
        param = pybamm.BaseParameterValues("input/parameters/lead-acid/default.csv")
        self.assertEqual(param["R"], 8.314)

    def test_overwrite(self):
        # from dicts
        param = pybamm.BaseParameterValues(
            base_parameters={"a": 1, "b": 2}, optional_parameters={"b": 3}
        )
        self.assertEqual(param["a"], 1)
        self.assertEqual(param["b"], 3)
        param.update({"a": 4})
        self.assertEqual(param["a"], 4)
        # from files
        param = pybamm.BaseParameterValues(
            base_parameters="input/parameters/lead-acid/default.csv",
            optional_parameters="input/parameters/lead-acid/optional_test.csv",
        )
        self.assertEqual(param["R"], 8.314)
        self.assertEqual(param["Ln"], 0.5)

    def test_get_parameter_value(self):
        parameter_values = pybamm.BaseParameterValues({"a": 1})
        param = pybamm.Parameter("a")
        self.assertEqual(parameter_values.get_parameter_value(param), 1)

    def test_process_symbol(self):
        parameter_values = pybamm.BaseParameterValues({"a": 1, "b": 2})
        # process parameter
        a = pybamm.Parameter("a")
        processed_a = parameter_values.process_symbol(a)
        self.assertTrue(isinstance(processed_a, pybamm.Scalar))
        self.assertEqual(processed_a.value, 1)

        # process binary operation
        b = pybamm.Parameter("b")
        sum = a + b
        processed_sum = parameter_values.process_symbol(sum)
        self.assertTrue(isinstance(processed_sum, pybamm.Addition))
        self.assertTrue(isinstance(processed_sum.children[0], pybamm.Scalar))
        self.assertTrue(isinstance(processed_sum.children[1], pybamm.Scalar))
        self.assertEqual(processed_sum.children[0].value, 1)
        self.assertEqual(processed_sum.children[1].value, 2)

        scal = pybamm.Scalar(34)
        mul = a * scal
        processed_mul = parameter_values.process_symbol(mul)
        self.assertTrue(isinstance(processed_mul, pybamm.Multiplication))
        self.assertTrue(isinstance(processed_mul.children[0], pybamm.Scalar))
        self.assertTrue(isinstance(processed_mul.children[1], pybamm.Scalar))
        self.assertEqual(processed_mul.children[0].value, 1)
        self.assertEqual(processed_mul.children[1].value, 34)

        # process unary operation
        grad = pybamm.Gradient(a)
        processed_grad = parameter_values.process_symbol(grad)
        self.assertTrue(isinstance(processed_grad, pybamm.Gradient))
        self.assertTrue(isinstance(processed_grad.children[0], pybamm.Scalar))
        self.assertEqual(processed_grad.children[0].value, 1)

        # process variable
        c = pybamm.Variable("c")
        processed_c = parameter_values.process_symbol(c)
        self.assertTrue(isinstance(processed_c, pybamm.Variable))
        self.assertEqual(processed_c.name, "c")

        # process scalar
        d = pybamm.Scalar(14)
        processed_d = parameter_values.process_symbol(d)
        self.assertTrue(isinstance(processed_d, pybamm.Scalar))
        self.assertEqual(processed_d.value, 14)

        # process array types
        e = pybamm.Vector(np.ones(4))
        processed_e = parameter_values.process_symbol(e)
        self.assertTrue(isinstance(processed_e, pybamm.Vector))
        np.testing.assert_array_equal(processed_e.evaluate(), np.ones(4))

        f = pybamm.Matrix(np.ones((5, 6)))
        processed_f = parameter_values.process_symbol(f)
        self.assertTrue(isinstance(processed_f, pybamm.Matrix))
        np.testing.assert_array_equal(processed_f.evaluate(), np.ones((5, 6)))

    @unittest.skip("model not yet implemented")
    def test_process_model(self):
        model = pybamm.BaseModel()
        a = pybamm.Parameter("a")
        b = pybamm.Parameter("b")
        c = pybamm.Variable("c")
        model.rhs = {c: a * pybamm.grad(c)}
        model.initial_conditions = {c: b}
        model.boundary_conditions = {}
        parameter_values = pybamm.BaseParameterValues({"a": 1, "b": 2})
        parameter_values.process(model)
        self.assertTrue(isinstance(model.rhs[c].children[0], pybamm.Scalar))
        self.assertEqual(model.rhs[c].children[0].value, 1)


if __name__ == "__main__":
    print("Add -v for more debug output")
    import sys

    if "-v" in sys.argv:
        debug = True
    unittest.main()