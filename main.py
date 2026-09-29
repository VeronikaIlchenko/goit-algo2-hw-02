from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    jobs = [
        PrintJob(
            id=job["id"],
            volume=job["volume"],
            priority=job["priority"],
            print_time=job["print_time"]
        )
        for job in print_jobs
    ]
    
    max_volume = constraints["max_volume"]
    max_items = constraints["max_items"]

    jobs.sort(key=lambda x: x.priority)

    print_order = []
    total_time = 0
    i = 0
    n = len(jobs)
    
    while i < n:
        current_batch = []
        current_batch_volume = 0
        max_time_in_batch = 0
        
        while i < n:
            job = jobs[i]
            if len(current_batch) < max_items and (current_batch_volume + job.volume <= max_volume or not current_batch):
                current_batch.append(job)
                current_batch_volume += job.volume
                max_time_in_batch = max(max_time_in_batch, job.print_time)
                i += 1
            else:
                break
                
        for job in current_batch:
            print_order.append(job.id)
            
        total_time += max_time_in_batch

    return {
        "print_order": print_order,
        "total_time": total_time
    }


def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    memo_profit = {}
    memo_cuts = {}

    def helper(l):
        if l == 0:
            return 0, []
        if l in memo_profit:
            return memo_profit[l], memo_cuts[l]

        max_p = 0
        best_cuts = []

        for i in range(1, l + 1):
            if i - 1 < len(prices):
                sub_profit, sub_cuts = helper(l - i)
                total_profit = prices[i - 1] + sub_profit
                
                if total_profit > max_p:
                    max_p = total_profit
                    best_cuts = [i] + sub_cuts

        memo_profit[l] = max_p
        memo_cuts[l] = best_cuts
        return max_p, best_cuts

    max_profit, cuts = helper(length)
    sorted_cuts = sorted(cuts)
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": max_profit,
        "cuts": sorted_cuts,
        "number_of_cuts": number_of_cuts
    }


def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    dp = [0] * (length + 1)
    first_cut = [0] * (length + 1)

    for i in range(1, length + 1):
        max_p = 0
        best_c = 0
        for j in range(1, i + 1):
            if j - 1 < len(prices):
                current = prices[j - 1] + dp[i - j]
                if current > max_p:
                    max_p = current
                    best_c = j
        dp[i] = max_p
        first_cut[i] = best_c

    current_length = length
    cuts = []
    while current_length > 0:
        cut = first_cut[current_length]
        cuts.append(cut)
        current_length -= cut

    sorted_cuts = sorted(cuts)
    number_of_cuts = len(cuts) - 1 if len(cuts) > 0 else 0

    return {
        "max_profit": dp[length],
        "cuts": sorted_cuts,
        "number_of_cuts": number_of_cuts
    }


def test_printing_optimization():
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]

    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1:")
    print(optimize_printing(test1_jobs, constraints))
    print("Тест 2:")
    print(optimize_printing(test2_jobs, constraints))
    print("Тест 3:")
    print(optimize_printing(test3_jobs, constraints))


def run_tests():
    test_cases = [
        {"length": 5, "prices": [2, 5, 7, 8, 10], "name": "Базовий випадок"},
        {"length": 3, "prices": [1, 3, 8], "name": "Оптимально не різати"},
        {"length": 4, "prices": [3, 5, 6, 7], "name": "Рівномірні розрізи"}
    ]

    for test in test_cases:
        print(f"\n--- {test['name']} ---")
        print("Memo:", rod_cutting_memo(test['length'], test['prices']))
        print("Table:", rod_cutting_table(test['length'], test['prices']))


if __name__ == "__main__":
    test_printing_optimization()
    run_tests()