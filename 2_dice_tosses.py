import random
import math

# Constants for the second game (tossing "11", "16", or "66")
cost_to_destroy_die = 1000000
reward = 3000000  # Reward for winning
winning_combinations = {11, 16, 66}
cost_per_fail = 1000
cost_fail_success = 7800
cost_fail_success_success = 49500

def calculate_tosses_for_95_confidence():
    """Calculate the number of tosses needed for 95% win confidence."""
    p_success = 1 / 12  # Probability of rolling "11", "16", or "66"
    p_three_successes = p_success ** 3
    p_failure = 1 - p_three_successes
    n_needed = math.ceil(math.log(0.05) / math.log(p_failure))
    return n_needed

def expected_cost(n_needed):
    """Calculate expected cost based on number of tosses."""
    e_cost = (1 - (1 / 12)) * cost_per_fail * n_needed  # Cost for each failed toss
    e_cost += (1 / 12) * (1 - (1 / 12)) * cost_fail_success * n_needed  # Cost after one success
    e_cost += (1 / 12) * (1 / 12) * (1 - (1 / 12)) * cost_fail_success_success * n_needed  # Cost after two successes
    return e_cost

def expected_gain():
    """Calculate expected gain for the second game."""
    return reward / (1 / 12) ** 3  # Expected gain based on probability of winning

def analyze_decision(n_needed):
    """Analyze whether to pay to destroy a die before the final toss."""
    # Expected costs and gains without destroying the die
    e_cost_without_destroy = expected_cost(n_needed)
    e_gain_without_destroy = expected_gain()
    net_gain_without_destroy = e_gain_without_destroy - e_cost_without_destroy

    # Expected costs and gains with destroying the die
    e_cost_with_destroy = cost_to_destroy_die  # Cost of destroying the die
    e_gain_with_destroy = reward  # Expected gain after destroying the die
    net_gain_with_destroy = e_gain_with_destroy - e_cost_with_destroy

    return (
        net_gain_without_destroy,
        net_gain_with_destroy,
        e_cost_without_destroy,
        e_cost_with_destroy,
        e_gain_without_destroy,
        e_gain_with_destroy
    )

def simulate_game_2_dice():
    """Simulate the game for tossing '11', '16', or '66'."""
    total_tosses = 0
    total_cost = 0
    attempts = 0
    
    while attempts < 10000:  # Limit to prevent infinite loop
        successes = 0
        for attempt in range(3):  # Attempt to achieve 3 consecutive successes
            roll = random.randint(1, 6) + random.randint(1, 6)  # Roll two dice
            total_tosses += 1
            
            if roll in winning_combinations:
                successes += 1
                if successes == 3:
                    return total_tosses, total_cost  # Player wins
            else:
                # Calculate cost based on the number of successes before the failure
                if successes == 0:
                    total_cost += cost_per_fail
                elif successes == 1:
                    total_cost += cost_fail_success
                elif successes == 2:
                    total_cost += cost_fail_success_success
                successes = 0  # Reset successes on failure
        
        attempts += 1
    
    print("No winner after maximum attempts.")
    return total_tosses, total_cost

def main():
    # Calculate for tossing "11", "16", or "66"
    n_needed = calculate_tosses_for_95_confidence()
    net_gain_no_destroy, net_gain_destroy, cost_no_destroy, cost_destroy, gain_no_destroy, gain_destroy = analyze_decision(n_needed)

    print("Analysis of Tossing '11', '16', or '66'")
    print("Number of tosses needed for 95% confidence:", n_needed)
    print("Expected Cost without Destroying Die:", cost_no_destroy)
    print("Expected Gain without Destroying Die:", gain_no_destroy)
    print("Net Gain without Destroying Die:", net_gain_no_destroy)
    print("Expected Cost with Destroying Die:", cost_destroy)
    print("Expected Gain with Destroying Die:", gain_destroy)
    print("Net Gain with Destroying Die:", net_gain_destroy)

    if net_gain_destroy > net_gain_no_destroy:
        print("It is beneficial to pay $1,000,000 to destroy the die before the final toss.")
    else:
        print("It is not beneficial to pay $1,000,000 to destroy the die before the final toss.")

    # Part 2: Simulate the game
    total_tosses, total_cost = simulate_game_2_dice()
    print("\nSimulation Results:")
    print("Total Tosses:", total_tosses)
    print("Total Cost: $", total_cost)

if __name__ == "__main__":
    main()
