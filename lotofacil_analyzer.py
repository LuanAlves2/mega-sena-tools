import os
from collections import Counter
from datetime import datetime
import pandas as pd

from utils import (
    is_prime, even_odd_count, count_primes, count_leq_12,
    count_mult_3, count_fib, count_ends0, count_dup_digits,
    diff_max_min, quadrant_count, modo_dict
)
from downloader import download_and_process_lotofacil


class LotofacilAnalyzer:
    """Analisa estatísticas históricas dos sorteios da Lotofácil."""

    def __init__(self, df_file: str = "database/lotofacil_sorteios_passados.xlsx"):
        if not os.path.exists(df_file):
            print("\033[1;93m⚠️ Banco de dados da Lotofácil não encontrado. Baixando...\033[0m")
            download_and_process_lotofacil()
            print("\033[1;92m✔ Banco de dados da Lotofácil atualizado!\033[0m")

        self.df_hist = pd.read_excel(df_file)
        self.draw_cols = [f"dezena{i}" for i in range(1, 16)]
        self.primes = {n for n in range(1, 26) if is_prime(n)}
        self.fibonacci = {1, 2, 3, 5, 8, 13, 21}
        self._analyze_historical_data()
        self.freq_dezenas = self.freq_por_dezena()

    def _analyze_historical_data(self):
        sums_hist = self.df_hist[self.draw_cols].sum(axis=1)

        self.pair_odd = Counter(even_odd_count(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_pair = modo_dict(self.pair_odd)

        self.prime_count = Counter(count_primes(row, self.primes) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_prime = modo_dict(self.prime_count)

        self.le12 = Counter(count_leq_12(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_le12 = modo_dict(self.le12)

        self.mult3 = Counter(count_mult_3(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_mult3 = modo_dict(self.mult3)

        self.fibc = Counter(count_fib(row, self.fibonacci) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_fib = modo_dict(self.fibc)

        self.end0 = Counter(count_ends0(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_end0 = modo_dict(self.end0)

        self.dup = Counter(count_dup_digits(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_dup = modo_dict(self.dup)

        self.diffs = Counter(diff_max_min(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_diff = modo_dict(self.diffs)

        self.cluster = Counter(sum(1 for x in row if 20 <= x <= 25) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_cluster = modo_dict(self.cluster)

        self.quadrant = Counter(quadrant_count(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_quadrant = modo_dict(self.quadrant)

        self.q1, self.q3 = sums_hist.quantile([0.25, 0.75])
        self.avg_sum_min = self.q1 / 15
        self.avg_sum_max = self.q3 / 15

        self.frac_even = self.modo_pair[0] / 15
        self.frac_prime = self.modo_prime / 15
        self.frac_le12 = self.modo_le12 / 15
        self.frac_mult3 = self.modo_mult3 / 15
        self.frac_fib = self.modo_fib / 15

    def freq_por_dezena(self):
        cont = Counter()
        for col in self.draw_cols:
            cont.update(self.df_hist[col])
        return [cont.get(n, 0) for n in range(1, 26)]
