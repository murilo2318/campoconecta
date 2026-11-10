"""Calcula os indicadores pedidos no relatório de Cluster. Uso: python calcular_ganho.py T2 T4"""
import sys

if len(sys.argv) != 3:
    sys.exit("Uso: python calcular_ganho.py T2 T4   (tempos em segundos)")
t2, t4 = float(sys.argv[1]), float(sys.argv[2])
if t2 <= 0 or t4 <= 0:
    sys.exit("Os tempos precisam ser positivos.")
print(f"T2 = {t2:.3f} s | T4 = {t4:.3f} s")
print(f"Redução percentual do tempo: {(t2 - t4) / t2 * 100:.1f}%")
print(f"Razão T2/T4 (speedup): {t2 / t4:.2f}  (ideal com o dobro de workers: 2,00)")
print(f"Eficiência do paralelismo: {t2 / t4 / 2 * 100:.0f}%")
