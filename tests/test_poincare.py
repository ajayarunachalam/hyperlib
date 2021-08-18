import tensorflow as tf
from hyperlib.manifold import poincare
from hyperlib.utils import math
from hyperlib.nn.layers import lin_hyp
from hyperlib.nn.optimizers import rsgd
import pytest

class TestClass:
    @classmethod
    def setup_class(self):
        self.test_tensor_shape_2_2_a = tf.constant(
            [[1.0, 2.0], [3.0, 4.0]], dtype=tf.float64
        )
        self.test_tensor_shape_2_2_b = tf.constant(
            [[0.5, 0.5], [0.5, 0.5]], dtype=tf.float64
        )
        self.test_tensor_shape_2_1a = tf.constant([[1.0], [2.0]], dtype=tf.float64)
        self.test_tensor_shape_2_1b = tf.constant([[0.5], [0.5]], dtype=tf.float64)
        self.poincare_manifold = poincare.Poincare()

    def test_math_functions(self, x=tf.constant([1.0, 2.0, 3.0])):
        return math.cosh(x)

    def test_mobius_matvec_(self):
        result = self.poincare_manifold.mobius_matvec(
            self.test_tensor_shape_2_2_a,
            self.test_tensor_shape_2_2_b
        )
        with pytest.raises(tf.errors.InvalidArgumentError):
            self.poincare_manifold.mobius_matvec(
                self.test_tensor_shape_2_2_a,
                self.test_tensor_shape_2_1a
            )

    def test_expmap0(self):
        result = self.poincare_manifold.expmap0(
            self.test_tensor_shape_2_2_a 
        )

    @pytest.mark.skip(reason="working on a test for this")
    def test_logmap0(self):
        result = self.poincare_manifold.logmap0(
            self.test_tensor_shape_2_2_b, self.curvature_tensor
        )

    def test_proj(self):
        result = self.poincare_manifold.proj(self.test_tensor_shape_2_2_a)

    def test_poincare_functions(self):
        manifold = poincare.Poincare()
        assert manifold.name == "PoincareBall"
        assert manifold.min_norm == 1e-15

    def test_create_layer(self, units=32):
        hyp_layer = lin_hyp.LinearHyperbolic(
            units, self.poincare_manifold, 1.0 
        )
        assert hyp_layer.units == units
        assert hyp_layer.manifold == self.poincare_manifold

    def test_layer_training(self, units=32):
        x_input = tf.zeros([units, 1])
        hyp_layer = lin_hyp.LinearHyperbolic(
            units, self.poincare_manifold, 1.0 
        )
        output = hyp_layer(x_input)

    def test_layer_training_with_bias(self, units=32):
        x_input = tf.zeros([units, 1])
        hyp_layer = lin_hyp.LinearHyperbolic(
            units, self.poincare_manifold, 1.0, use_bias=True
        )
        output = hyp_layer(x_input)

    def test_create_optimizer(self):
        opt = rsgd.RSGD()
