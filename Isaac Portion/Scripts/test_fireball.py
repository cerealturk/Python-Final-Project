# Isaac Burmingham

import unittest
from fireball import Fireball
import pandas as pd
import numpy as np

class UnitTestFireball(unittest.TestCase):

    def test_fb(self):
        df = Fireball().fireballdf
        self.assertTrue(isinstance(df,pd.DataFrame))


    def test_vel_max(self):
        df = Fireball().fireballdf
        df['velocity'] = df['Velocity (km/s)']
        df_adj = df[np.abs(df.velocity-df.velocity.mean()) <= (1.5*df.velocity.std())]
        self.assertTrue((df_adj.velocity.max() > 1.5*df_adj.velocity.std())) # verify the equation works

    def test_size(self):
        df = Fireball().fireballdf
        self.assertTrue(len(df) == 822)

    def test_header(self):
        df = Fireball().fireballdf
        head = Fireball().get_header()
        self.assertTrue(len(head) <= 5)











if __name__ == "__main__":
    unittest.main()
