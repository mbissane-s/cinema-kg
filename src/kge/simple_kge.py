import pandas as pd
import numpy as np
import random

random.seed(42)
np.random.seed(42)

df = pd.read_csv("data/samples/kg_clean.csv")
triples = list(df.itertuples(index=False, name=None))

entities  = sorted(set(df["subject"]) | set(df["object"]))
relations = sorted(set(df["predicate"]))

ent2id = {e: i for i, e in enumerate(entities)}
rel2id = {r: i for i, r in enumerate(relations)}

triples_idx = [(ent2id[h], rel2id[r], ent2id[t]) for h, r, t in triples]

n_ent = len(entities)
n_rel = len(relations)
dim   = 50
lr    = 0.01
margin = 1.0
epochs = 100
batch  = 64


def normalize_rows(mat):
    norms = np.linalg.norm(mat, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    return mat / norms


E = normalize_rows(np.random.randn(n_ent, dim).astype(np.float32))
R = np.random.randn(n_rel, dim).astype(np.float32)


def corrupt(triple):
    h, r, t = triple
    if random.random() < 0.5:
        neg_h = random.randint(0, n_ent - 1)
        while neg_h == h:
            neg_h = random.randint(0, n_ent - 1)
        return (neg_h, r, t)
    else:
        neg_t = random.randint(0, n_ent - 1)
        while neg_t == t:
            neg_t = random.randint(0, n_ent - 1)
        return (h, r, neg_t)


def score_batch(hs, rs, ts):
    return np.linalg.norm(E[hs] + R[rs] - E[ts], axis=1)


for epoch in range(epochs):
    random.shuffle(triples_idx)
    total_loss = 0.0

    for i in range(0, len(triples_idx), batch):
        batch_pos = triples_idx[i:i+batch]
        batch_neg = [corrupt(t) for t in batch_pos]

        hs_p = np.array([t[0] for t in batch_pos])
        rs_p = np.array([t[1] for t in batch_pos])
        ts_p = np.array([t[2] for t in batch_pos])

        hs_n = np.array([t[0] for t in batch_neg])
        rs_n = np.array([t[1] for t in batch_neg])
        ts_n = np.array([t[2] for t in batch_neg])

        d_pos = score_batch(hs_p, rs_p, ts_p)
        d_neg = score_batch(hs_n, rs_n, ts_n)

        loss_vec = np.maximum(0, margin + d_pos - d_neg)
        total_loss += loss_vec.sum()

        active = loss_vec > 0
        if active.sum() == 0:
            continue

        grad_pos =  (E[hs_p] + R[rs_p] - E[ts_p])
        grad_neg = -(E[hs_n] + R[rs_n] - E[ts_n])

        for k in range(len(batch_pos)):
            if not active[k]:
                continue
            h_p, r_p, t_p = hs_p[k], rs_p[k], ts_p[k]
            h_n, r_n, t_n = hs_n[k], rs_n[k], ts_n[k]

            g = grad_pos[k] / (d_pos[k] + 1e-8)
            E[h_p] -= lr * g
            R[r_p] -= lr * g
            E[t_p] += lr * g

            g2 = grad_neg[k] / (d_neg[k] + 1e-8)
            E[h_n] -= lr * g2
            R[r_n] -= lr * g2
            E[t_n] += lr * g2

        E[:] = normalize_rows(E)

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}/{epochs}  loss: {total_loss:.2f}")


def evaluate(test_triples):
    ranks = []
    hits1, hits3, hits10 = 0, 0, 0

    all_ids = np.arange(n_ent)

    for h, r, t in test_triples:
        candidates = np.stack([
            np.full(n_ent, h),
            np.full(n_ent, r),
            all_ids
        ], axis=1)

        scores = np.linalg.norm(
            E[candidates[:, 0]] + R[candidates[:, 1]] - E[candidates[:, 2]],
            axis=1
        )
        order = np.argsort(scores)
        rank  = int(np.where(order == t)[0][0]) + 1
        ranks.append(rank)

        if rank <= 1:  hits1  += 1
        if rank <= 3:  hits3  += 1
        if rank <= 10: hits10 += 1

    n = len(ranks)
    mrr   = float(np.mean([1.0 / r for r in ranks]))
    h1    = hits1  / n
    h3    = hits3  / n
    h10   = hits10 / n
    return mrr, h1, h3, h10


split = int(0.8 * len(triples_idx))
train_t = triples_idx[:split]
test_t  = triples_idx[split:]

print("\n── TransE evaluation ──")
mrr, h1, h3, h10 = evaluate(test_t[:100])
print(f"MRR:     {mrr:.4f}")
print(f"Hits@1:  {h1:.4f}")
print(f"Hits@3:  {h3:.4f}")
print(f"Hits@10: {h10:.4f}")

print("\n── Nearest neighbors (Inception) ──")
if "Inception" in ent2id:
    target = E[ent2id["Inception"]]
    sims   = E @ target
    top5   = np.argsort(sims)[-6:][::-1]
    for idx in top5:
        if entities[idx] != "Inception":
            print(f"  {entities[idx]}")
