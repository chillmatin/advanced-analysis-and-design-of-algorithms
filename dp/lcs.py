import sys
import os

# Define the sequences based on the slides example (using 0-indexing for convenience in Python)
# We will prepend a space to simulate 1-based indexing for the calculation logic
# X = 'ABCBDAB' (m=7), Y = 'BDCABA' (n=6)
X = " " + "ABCBDAB"
Y = " " + "BDCABA"
M = len(X) - 1 # Length of sequence X
N = len(Y) - 1 # Length of sequence Y

def format_table(C, X_seq, Y_seq, highlight_i, highlight_j):
    """Formats and prints the DP table with headers and a highlighted cell."""
    
    # 1. Print Y sequence as column header
    header = " " * 4
    for char in Y_seq:
        header += f"{char:^5}"
    print("-" * 5 * (N + 2))
    print(header)
    print("-" * 5 * (N + 2))

    # 2. Print rows
    for i in range(M + 1):
        row_output = f"{X_seq[i]:>3} |"
        
        for j in range(N + 1):
            cell_value = C[i][j]
            
            # Highlight the current cell being calculated
            if i == highlight_i and j == highlight_j:
                row_output += f"\033[97;44m{cell_value:^4}\033[0m|" # Bright white on blue background
            # Highlight cells used for calculation (i-1, j-1), (i-1, j), (i, j-1)
            elif (i, j) == (highlight_i - 1, highlight_j - 1):
                row_output += f"\033[93m{cell_value:^4}\033[0m|" # Yellow
            elif (i, j) == (highlight_i - 1, highlight_j):
                row_output += f"\033[92m{cell_value:^4}\033[0m|" # Green
            elif (i, j) == (highlight_i, highlight_j - 1):
                row_output += f"\033[91m{cell_value:^4}\033[0m|" # Red
            else:
                row_output += f"{cell_value:^4}|"
        print(row_output)
    print("-" * 5 * (N + 2))

def pause_and_prompt():
    """Waits for user input to proceed."""
    print("\n--- Press ENTER to proceed to the next step ---")
    input()
    # Clear screen for better visual experience (might not work in all environments)
    os.system('cls' if os.name == 'nt' else 'clear')

def lcs_bottom_up(X, Y, M, N):
    """
    Implements the bottom-up DP approach for LCS with step-by-step visualization.
    """
    # Initialize the DP table C[M+1][N+1] with zeros
    C = [[0] * (N + 1) for _ in range(M + 1)]

    # Use ' ' for the 0-index in X and Y sequences for clean header printing
    X_seq = [' '] + list(X[1:])
    Y_seq = [' '] + list(Y[1:])

    print("--- LCS Dynamic Programming Simulation ---")
    print(f"Sequence X (vertical): {X[1:]} (M={M})")
    print(f"Sequence Y (horizontal): {Y[1:]} (N={N})")
    
    # Initialization Step
    print("\n[Initialization]")
    print("The 0th row and 0th column are set to 0 (Base Case: LCS with an empty string is 0).")
    format_table(C, X_seq, Y_seq, -1, -1)
    pause_and_prompt()

    # Fill the table (i and j start from 1 because 0s are base cases)
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            
            x_char = X[i] # Current character in X prefix
            y_char = Y[j] # Current character in Y prefix

            print(f"\n[Calculating C[{i},{j}]] - LCS of X[1..{i}] ('{X[1:i+1]}') and Y[1..{j}] ('{Y[1:j+1]}')")
            print(f"Comparing X[{i}] ('{x_char}') vs Y[{j}] ('{y_char}')")

            if x_char == y_char:
                # Case 1: Match
                # c[i,j] = c[i-1, j-1] + 1
                C[i][j] = C[i-1][j-1] + 1
                
                print("\n\033[96m<<< CASE 1: MATCH >>>\033[0m") # Cyan text
                print(f"The characters match! We take the diagonal value (\033[93m{C[i-1][j-1]}\033[0m) and add 1.")
                print(f"Formula: C[{i},{j}] = C[{i-1},{j-1}] + 1 = {C[i-1][j-1]} + 1 = {C[i][j]}")
                
            else:
                # Case 2: Mismatch
                # c[i,j] = max(c[i-1, j], c[i, j-1])
                
                # Highlight the two candidates for max:
                val_up = C[i-1][j]
                val_left = C[i][j-1]
                
                C[i][j] = max(val_up, val_left)
                
                print("\n\033[95m<<< CASE 2: MISMATCH >>>\033[0m") # Magenta text
                print(f"The characters mismatch. We take the maximum of the value above (\033[92m{val_up}\033[0m) and the value to the left (\033[91m{val_left}\033[0m).")
                print(f"Formula: C[{i},{j}] = max(C[{i-1},{j}], C[{i},{j-1}]) = max({val_up}, {val_left}) = {C[i][j]}")
            
            # Display the table with the new value and highlighted dependencies
            format_table(C, X_seq, Y_seq, i, j)
            
            # Pause for the next step
            pause_and_prompt()

    print("--- SIMULATION COMPLETE ---")
    print(f"The length of the Longest Common Subsequence is C[{M},{N}] = {C[M][N]}")

if __name__ == "__main__":
    try:
        lcs_bottom_up(X, Y, M, N)
    except EOFError:
        print("\nSimulation aborted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")