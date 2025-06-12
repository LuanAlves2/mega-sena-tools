import os
import pandas as pd
from collections import Counter
from datetime import datetime
from analyzer import MegaSenaAnalyzer
from utils import (
    even_odd_count, count_primes, count_leq_30,
    count_mult_3, count_fib, count_ends0, count_dup_digits,
    diff_max_min
)

class MegaSenaValidator:
    def __init__(self):
        self.analyzer = MegaSenaAnalyzer()

    def aposta_valida(self, nums):
        k = len(nums)
        if even_odd_count(nums) != (round(self.analyzer.frac_even*k), k-round(self.analyzer.frac_even*k)):
            return False
        if count_primes(nums, self.analyzer.primes) != round(self.analyzer.frac_prime*k): 
            return False
        s = sum(nums)
        if not (self.analyzer.avg_sum_min*k <= s <= self.analyzer.avg_sum_max*k): 
            return False
        if count_leq_30(nums) != round(self.analyzer.frac_le30*k): 
            return False
        if count_mult_3(nums) != round(self.analyzer.frac_mult3*k): 
            return False
        if count_fib(nums, self.analyzer.fibonacci) != round(self.analyzer.frac_fib*k): 
            return False
        if count_ends0(nums) != self.analyzer.modo_end0: 
            return False
        if count_dup_digits(nums) != self.analyzer.modo_dup: 
            return False
        if diff_max_min(nums) != self.analyzer.modo_diff: 
            return False
        return True

    def gerar_apostas(self, n_apostas, dezenas):
        import random
        apostas = []
        while len(apostas) < n_apostas:
            cand = random.sample(range(1,61), dezenas)
            if self.aposta_valida(cand):
                apostas.append(sorted(cand))
        return apostas

    def validar_arquivo(self, path):
        df = pd.read_excel(path)
        cols = [c for c in df.columns if 'dezena' in c.lower()]
        for idx, row in df.iterrows():
            nums = [int(row[c]) for c in cols]
            status = "VÁLIDA" if self.aposta_valida(nums) else "INVÁLIDA"
            print(f"Linha {idx+1}: {nums} → {status}")

    def checar_resultado(self, path, resultado):
        df = pd.read_excel(path)
        cols = [c for c in df.columns if 'dezena' in c.lower()]
        apostas = df[cols].values.tolist()
        res_set = set(resultado)
        cont = Counter(len(res_set & set(a)) for a in apostas)
        print("\n=== Resumo de Acertos ===")
        for ac in sorted(cont): 
            print(f"{ac:>2} acertos: {cont[ac]} apostas")
        print("\nDetalhe (≥4 acertos):")
        for i,a in enumerate(apostas,1):
            ac = len(res_set & set(a))
            if ac>=4: 
                print(f"  Aposta{i:3d}: {a} → {ac} acertos")

    def salvar_apostas(self, apostas, n_apostas, dezenas):
        os.makedirs("sorteios", exist_ok=True)
        cols = [f"dezena{i+1}" for i in range(dezenas)]
        df_out = pd.DataFrame(apostas, columns=cols)
        hoje = datetime.now().strftime("%Y%m%d")
        fn = f"sorteios/Apostas_Geradas_{n_apostas}Apostas_{dezenas}Dezenas_{hoje}.xlsx"
        df_out.to_excel(fn, index=False)
        return fn 