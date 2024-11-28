import math
import random

cost_per_fail = 1000
cost_fail_success = 7800
cost_fail_success_success = 49500

P_fail = 5 / 6
P_success = 1 / 6
prize = 100000
# question 1:

def calculate_tosses():
    P_success = 1 / 6
    P_failure = 1 - P_success

    P_3_successes = P_success ** 3
    P_failure_total = 1 - P_3_successes

    target = 0.95
    n = math.ceil(math.log(1 - target) / math.log(P_failure_total))

    return n

tosses_needed = calculate_tosses()
print("Number of tosses needed for 95% win confidence: ", tosses_needed)


# question 2:
def expected_cost():
    global cost_per_fail, cost_fail_success, cost_fail_success_success, P_fail, P_success, prize

    E_cost_1 = P_fail * cost_per_fail
    E_cost_2 = P_success * P_fail * cost_fail_success
    E_cost_3 = P_success ** 2 * P_fail * cost_fail_success_success

    # Total expect cost:
    E_cost = E_cost_1 + E_cost_2 + E_cost_3

    return E_cost

def expected_gain():
    P_success_3 = (1 / 6) ** 3
    prize_win = 100000

    E_gain = P_success_3 * prize
    return E_gain

def net_gain_loss():
    E_cost = expected_cost()
    E_gain = expected_gain()

    net_gain = E_gain - E_cost
    return net_gain, E_cost, E_gain

net_gain, cost_expected, gain_expected = net_gain_loss()
print("Expected cost: ", cost_expected)
print("Expected gain: ", gain_expected)
print("Net gain/ loss: ", net_gain)


# question 3:
def minimum_prize_amount():
    return expected_cost()

# question 4:
def simulate_game(max_tosses=300):
    global cost_per_fail, cost_fail_success, cost_fail_success_success, P_fail, P_success
    results = []
    for player in range(4):
        toss_count = 0
        total_cost = 0
        successes = 0
        
        while toss_count < max_tosses:
            toss = random.randint(1, 6) # Roll the dice
            toss_count +=1

            if toss == 1:
                successes +=1 
                # check if player has won
                if successes == 3:
                    net_gain = prize - total_cost
                    break
            else:
                total_cost +=cost_per_fail
                if successes > 0: # If there have been success
                    if successes == 1:
                        total_cost +=cost_fail_success
                    elif successes == 2:
                        total_cost += cost_fail_success_success

                successes = 0 # reset success after a failure
        else:
            # If the loop ends without breaking, player did not win
            net_gain = -total_cost # total lost if no prize

        results.append({
            "Player": player + 1,
            "Net Gain": net_gain,
            "Tosses": toss_count,
            "Total Cost": total_cost
            })
    return results

game_results = simulate_game()
for result in game_results:
    print(f"Player {result['Player']}: Net Gain = {result['Net Gain']} USD, "
            f"Tosses = {result['Tosses']}, Total Cost = {result['Total Cost']} USD")


if __name__ == "__main__":
    print("1. Number of tosses needed for 95% win confidence (1 die) ", calculate_tosses())
    print("2. Expected Cost: ", expected_cost())
    print("3. Expected Gain: ", expected_gain())
    print("4. Minimum prize amount to consider playing: ", minimum_prize_amount())
    print(simulate_game())



    



