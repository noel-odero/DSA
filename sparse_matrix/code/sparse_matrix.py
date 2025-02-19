
class SparseMatrix:
    def __init__(self, num_rows=None, num_cols=None, matrix_file_path=None):
        self.rows = 0
        self.cols = 0
        self.data = {}  # Dictionary to store (row, col): value

        if matrix_file_path:
            self.load_from_file(matrix_file_path)
        elif num_rows is not None and num_cols is not None:
            self.rows = num_rows
            self.cols = num_cols
        else:
            raise ValueError(
                "Must provide either file path or row/col dimensions")

    def load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f]  # Remove whitespace

                self.rows = int(lines[0].split('=')[1])
                self.cols = int(lines[1].split('=')[1])

                for line in lines[2:]:
                    if not line:
                        continue
                    line = line.replace(" ", "")
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError("Input file has wrong format")
                    parts = line[1:-1].split(',')
                    if len(parts) != 3:
                        raise ValueError("Input file has wrong format")
                    row, col, value = map(int, parts)
                    self.set_element(row, col, value)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except ValueError as e:
            raise ValueError(f"Input file has wrong format: {e}")

    def set_element(self, row, col, value):
        self.data[(row, col)] = value

    def get_element(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.data.get((row, col), 0)  # Default to 0 if not found
        else:
            raise IndexError("Row or column index out of bounds")

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices must have the same dimensions for addition")
        result = SparseMatrix(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                # print(self.get_element(row, col), other.get_element(row, col))
                result.set_element(row, col, self.get_element(
                    row, col) + other.get_element(row, col))
        return result

    def subtract(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                "Matrices must have the same dimensions for subtraction")

        result = SparseMatrix(self.rows, self.cols)
        for row in range(self.rows):
            for col in range(self.cols):
                result.set_element(row, col, self.get_element(
                    row, col) - other.get_element(row, col))
        return result

    def multiply(self, other):
        if self.cols != other.rows:
            raise ValueError(
                "Number of columns in first matrix must be equal to number of rows in second matrix for multiplication")

        result = SparseMatrix(self.rows, other.cols)
        for i in range(self.rows):
            for j in range(other.cols):
                sum_val = 0
                for k in range(self.cols):
                    sum_val += self.get_element(i, k) * \
                        other.get_element(k, j)
                if sum_val != 0:
                    result.set_element(i, j, sum_val)
        return result

    def __str__(self):
        matrix_str = ""
        for i in range(self.rows):
            row_str = ""
            for j in range(self.cols):
                row_str += str(self.get_element(i, j)) + " "
            matrix_str += row_str + "\n"
        return matrix_str

    def print_readable(self, max_rows=10, max_cols=10):
        """Prints a readable representation of the sparse matrix.

        Args:
            max_rows (int, optional): Maximum number of rows to print. Defaults to 10.
            max_cols (int, optional): Maximum number of columns to print. Defaults to 10.
        """

        if self.rows > max_rows or self.cols > max_cols:
            print(
                f"Matrix is large ({self.rows}x{self.cols}). Showing only top-left {max_rows}x{max_cols} elements.")

        for i in range(min(self.rows, max_rows)):
            row_str = ""
            for j in range(min(self.cols, max_cols)):
                row_str += str(self.get_element(i, j)).rjust(5) + \
                    " "
            print(row_str)

        if self.rows > max_rows or self.cols > max_cols:
            print("...")


# try:
#     # create matrix1 from file
#     matrix1 = SparseMatrix(matrix_file_path="../sample_input/matrixfile1.txt")
#     # matrix2 = SparseMatrix(matrix_file_path="../sample_input/matrixfile1.txt")

#     # print(matrix1)  # create matrix2 from file
#     matrix1.print_readable()

#     # sum_matrix = matrix1.add(matrix2)  # Add matrix1 and matrix2
#     # print("Sum Matrix:\n", sum_matrix.print_readable(15, 15))

#     # product_matrix = matrix1.multiply(matrix2)  # Multiply matrix1 and matrix2
#     # print("Product Matrix:\n", product_matrix)

# except (FileNotFoundError, ValueError) as e:
#     print(e)
# except Exception as e:
#     print(f"An unexpected error occurred: {e}")
