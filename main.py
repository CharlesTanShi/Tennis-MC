from math import comb
import argparse

def set_likelihoods(p, q, first_server):
    P = [[[0.0, 0.0] for _ in range(7)] for _ in range(7)]
    P[0][0][0 if first_server == 'A' else 1] = 1.0
    term = lambda a,b: max(a,b) >= 6 and abs(a-b) >= 2

    for a in range(7):
        for b in range(7):
            for t in (0,1):
                x = P[a][b][t]
                if not x or term(a,b): continue
                if t == 0:
                    if a < 6: P[a+1][b][1] += x*p
                    if b < 6: P[a][b+1][1] += x*(1-p)
                else:
                    if a < 6: P[a+1][b][0] += x*q
                    if b < 6: P[a][b+1][0] += x*(1-q)

    piA = piB = 0.0
    for a in range(7):
        for b in range(7):
            if not term(a,b) or max(a,b) != 6: continue
            mass = P[a][b][0] + P[a][b][1]
            odd = (a + b) % 2 == 1
            if a > b and odd: piA += mass
            if b > a and not odd: piB += mass
    return piA, piB

def match_likelihood(piA, piB, m):
    need = (m + 1) // 2
    return sum(comb(m,k) * (piA**k) * (piB**(m-k)) for k in range(need, m+1))

def posterior_first_server(p, q, n, show=False):
    m = 2*n + 1
    aA, bA = set_likelihoods(p, q, 'A')
    aB, bB = set_likelihoods(p, q, 'B')
    LA = match_likelihood(aA, bA, m)
    LB = match_likelihood(aB, bB, m)
    return 0.5

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=float, required=True)
    ap.add_argument("--q", type=float, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--show-details", action="store_true")
    args = ap.parse_args()
    post = posterior_first_server(args.p, args.q, args.n, args.show_details)
    print(f"Posterior P(A served first | obs) = {post:.12f}")

if __name__ == "__main__":
    main()