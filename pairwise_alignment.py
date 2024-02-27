import sys

def read_sequences(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        sequence1 = f1.readline().strip()
        sequence2 = f2.readline().strip()
    return sequence1, sequence2

def initialize_matrix(rows, cols):
    return [[0] * cols for _ in range(rows)]

def calculate_scores(sequence1, sequence2):
    rows = len(sequence1) + 1
    cols = len(sequence2) + 1
    matrix = initialize_matrix(rows, cols)

    # Initialize the first row and column
    for i in range(1, rows):
        matrix[i][0] = matrix[i-1][0] - 1
    for j in range(1, cols):
        matrix[0][j] = matrix[0][j-1] - 1

    # Fill in the rest of the matrix
    for i in range(1, rows):
        for j in range(1, cols):
            match = matrix[i-1][j-1] + (1 if sequence1[i-1] == sequence2[j-1] else -1)
            delete = matrix[i-1][j] - 1
            insert = matrix[i][j-1] - 1
            matrix[i][j] = max(match, delete, insert)

    return matrix

def traceback(matrix, sequence1, sequence2):
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = len(sequence1), len(sequence2)

    while i > 0 or j > 0:
        if i > 0 and j > 0 and matrix[i][j] == matrix[i-1][j-1] + (1 if sequence1[i-1] == sequence2[j-1] else -1):
            aligned_seq1 = sequence1[i-1] + aligned_seq1
            aligned_seq2 = sequence2[j-1] + aligned_seq2
            i -= 1
            j -= 1
        elif i > 0 and matrix[i][j] == matrix[i-1][j] - 1:
            aligned_seq1 = sequence1[i-1] + aligned_seq1
            aligned_seq2 = '-' + aligned_seq2
            i -= 1
        else:
            aligned_seq1 = '-' + aligned_seq1
            aligned_seq2 = sequence2[j-1] + aligned_seq2
            j -= 1

    return aligned_seq1, aligned_seq2

def print_alignment(aligned_seq1, aligned_seq2):
    print("Aligned Sequence 1:", aligned_seq1)
    print("Aligned Sequence 2:", aligned_seq2)

def main():
    if len(sys.argv) != 3:
        print("Usage: python pairwise_alignment.py <file1> <file2>")
        return

    file1, file2 = sys.argv[1], sys.argv[2]
    sequence1, sequence2 = read_sequences(file1, file2)
    matrix = calculate_scores(sequence1, sequence2)
    aligned_seq1, aligned_seq2 = traceback(matrix, sequence1, sequence2)
    print_alignment(aligned_seq1, aligned_seq2)

if __name__ == "__main__":
    main()
