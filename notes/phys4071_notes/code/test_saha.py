import unittest

from saha import (
    inverse_mean_free_path_of_photon,
    mean_free_path_of_photon,
    mean_free_path_physical_and_comoving_mpc,
    saha_get_ionization_fraction,
    saha_get_temperature_for_ionization_fraction,
)


class TestSahaFunctions(unittest.TestCase):
    def test_forward_output_range(self):
        for T in [3000.0, 6000.0, 10000.0, 20000.0, 50000.0]:
            y = saha_get_ionization_fraction(T)
            self.assertTrue(0.0 < y < 1.0)

    def test_round_trip_temperature(self):
        # Invertibility is best conditioned away from Y_p ~ 1 saturation.
        for T in [3200.0, 3600.0, 4000.0, 4500.0, 5200.0]:
            y = saha_get_ionization_fraction(T)
            t_back = saha_get_temperature_for_ionization_fraction(y)
            rel_err = abs(t_back - T) / T
            self.assertLess(rel_err, 1e-9)

    def test_round_trip_ionization_fraction(self):
        for y in [1e-6, 1e-4, 1e-2, 0.1, 0.5, 0.9]:
            t = saha_get_temperature_for_ionization_fraction(y)
            y_back = saha_get_ionization_fraction(t)
            rel_err = abs(y_back - y) / y
            self.assertLess(rel_err, 1e-9)

    def test_recombination_scale(self):
        t_half = saha_get_temperature_for_ionization_fraction(0.5)
        self.assertTrue(3000.0 <= t_half <= 4000.0)

    def test_mean_free_path_scale_near_recombination(self):
        # Expected comoving horizon-scale order around recombination.
        mfp_mpc = mean_free_path_of_photon(0.5, comoving=True, unit="Mpc")
        self.assertTrue(1.0 <= mfp_mpc <= 10.0)

    def test_mean_free_path_units_and_invalids(self):
        mfp_kpc = mean_free_path_of_photon(0.5, comoving=True, unit="kpc")
        self.assertGreater(mfp_kpc, 0.0)

        with self.assertRaises(ValueError):
            mean_free_path_of_photon(0.5, unit="bad_unit")
        with self.assertRaises(ValueError):
            mean_free_path_of_photon(1.0)

    def test_dual_mfp_helper(self):
        lam_phys, lam_com, n_e = mean_free_path_physical_and_comoving_mpc(0.5)
        self.assertGreater(lam_phys, 0.0)
        self.assertGreater(lam_com, lam_phys)
        self.assertGreater(n_e, 0.0)

    def test_inverse_mean_free_path(self):
        y_true = 0.5
        lam_com = mean_free_path_of_photon(y_true, comoving=True, unit="Mpc")
        y_back = inverse_mean_free_path_of_photon(lam_com, comoving=True, unit="Mpc")
        self.assertLess(abs(y_back - y_true), 1e-10)

        lam_phys = mean_free_path_of_photon(y_true, comoving=False, unit="Mpc")
        y_back_phys = inverse_mean_free_path_of_photon(lam_phys, comoving=False, unit="Mpc")
        self.assertLess(abs(y_back_phys - y_true), 1e-10)

        with self.assertRaises(ValueError):
            inverse_mean_free_path_of_photon(-1.0)
        with self.assertRaises(ValueError):
            inverse_mean_free_path_of_photon(1.0, unit="bad_unit")

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            saha_get_ionization_fraction(0.0)
        with self.assertRaises(ValueError):
            saha_get_ionization_fraction(-10.0)

        for bad_y in [0.0, 1.0, -0.1, 1.1]:
            with self.assertRaises(ValueError):
                saha_get_temperature_for_ionization_fraction(bad_y)


if __name__ == "__main__":
    unittest.main()
