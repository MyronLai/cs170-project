import leaderboard
import json
import sys

if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        our_scores = json.loads(f.read())

    top_scores, submitted_scores, _, by_input = leaderboard.parse_leaderboard()

    ranks = leaderboard.calculate_ranks(our_scores, by_input)
    submitted_ranks = leaderboard.calculate_ranks(submitted_scores, by_input)

    real_ranks = [max(x, 1) for x in ranks.values()]
    real_rank = sum(real_ranks) / len(real_ranks)

    submitted_rank = sum(submitted_ranks.values()) / len(submitted_ranks.values())

    print(f"Overall Average Rank: {real_rank}")
    print(f"Submitted Average Rank: {submitted_rank} (diff {real_rank - submitted_rank})")

    all_scores = our_scores.values()
    small_scores = [s[1] for s in our_scores.items() if "small" in s[0]]
    medium_scores = [s[1] for s in our_scores.items() if "medium" in s[0]]
    large_scores = [s[1] for s in our_scores.items() if "large" in s[0]]

    avg = sum(all_scores)/len(all_scores)
    submitted_avg = sum(submitted_scores.values())/len(submitted_scores.values())

    print()
    print("Overall average score:", avg)
    print(f"Submitted average score: {submitted_avg} (diff {avg - submitted_avg})")
    print("Small average score:", sum(small_scores)/len(small_scores))
    print("Medium average score:", sum(medium_scores)/len(medium_scores))
    print("Large average score:", sum(large_scores)/len(large_scores))

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