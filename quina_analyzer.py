import os
from collections import Counter
import pandas as pd

from utils import (
    is_prime, even_odd_count, count_primes, count_leq_40,
    count_mult_3, count_fib, count_ends0, count_dup_digits,
    diff_max_min, modo_dict
)
from downloader import download_and_process_quina


class QuinaAnalyzer:
    """Analisa estatísticas históricas dos sorteios da Quina."""

    def __init__(self, df_file: str = "database/quina_sorteios_passados.xlsx"):
        if not os.path.exists(df_file):
            print("\033[1;93m⚠️ Banco de dados da Quina não encontrado. Baixando...\033[0m")
            download_and_process_quina()
            print("\033[1;92m✔ Banco de dados da Quina atualizado!\033[0m")

        self.df_hist = pd.read_excel(df_file)
        self.draw_cols = [f"dezena{i}" for i in range(1, 6)]
        self.primes = {n for n in range(1, 81) if is_prime(n)}
        self.fibonacci = {1, 2, 3, 5, 8, 13, 21, 34, 55}
        self._analyze_historical_data()
        self.freq_dezenas = self.freq_por_dezena()

    def _analyze_historical_data(self):
        sums_hist = self.df_hist[self.draw_cols].sum(axis=1)

        self.pair_odd = Counter(even_odd_count(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_pair = modo_dict(self.pair_odd)

        self.prime_count = Counter(count_primes(row, self.primes) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_prime = modo_dict(self.prime_count)

        self.le40 = Counter(count_leq_40(row) for _, row in self.df_hist[self.draw_cols].iterrows())
        self.modo_le40 = modo_dict(self.le40)

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

        self.q1, self.q3 = sums_hist.quantile([0.25, 0.75])

        self.frac_even = self.modo_pair[0] / 5
        self.frac_prime = self.modo_prime / 5
        self.frac_le40 = self.modo_le40 / 5
        self.frac_mult3 = self.modo_mult3 / 5
        self.frac_fib = self.modo_fib / 5
        self.avg_sum_min = self.q1 / 5
        self.avg_sum_max = self.q3 / 5

    def freq_por_dezena(self):
        cont = Counter()
        for col in self.draw_cols:
            cont.update(self.df_hist[col])
        return [cont.get(n, 0) for n in range(1, 81)]
