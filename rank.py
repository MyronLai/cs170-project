import leaderboard
import json
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        our_scores = json.loads(f.read())

    top_scores, _, _, by_input = leaderboard.parse_leaderboard()

    ranks = leaderboard.calculate_ranks(our_scores, by_input)

    real_ranks = [max(x, 1) for x in ranks.values()]
    real_rank = sum(real_ranks) / len(real_ranks)

    print("Overall Average Rank:", real_rank)

    rank_amounts = {}
    for rank in ranks.values():
        if rank not in rank_amounts:
            rank_amounts[rank] = 0
        rank_amounts[rank] += 1
    
    print()
    print("Number of each rank")
    for r, c in sorted(rank_amounts.items(), key=lambda x: x[0]):
        print(f"{r}: {c}")
    
    N = 10
    print()
    print(f"{N} worst ranks")
    for f, r in sorted(ranks.items(), key=lambda x: -x[1])[:N]:
        print(f"{f}: {r} (our score {our_scores[f]}, top score {top_scores[f]})")