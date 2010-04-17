import dickens

class TestAnalyzer:
    def test_clock_plot(self):
        a = dickens.Analyzer()
        letters = [ ('A',1840), ('B',1841), ('A',1843) ]
        counts, starts, ends = a._clock_data(letters)
        assert counts['A'] == 2
        assert starts['A'] == 1840
        assert ends['A'] == 1844, ends
        assert ends['B'] == 1842, ends

        out = a._clock_data_in_polar(counts,starts,ends, start_radius=0.0)
        assert out['A'] == [ (0,1/3.0), 360, 2/3.0 ], out
        assert out['B'] == [ (90,0.0), 90.0, 1/3.0 ], out

        a.clock_plot(letters, fn='clock_test.png')

