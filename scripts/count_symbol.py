def count_symbol_in_file(file_path, symbol):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        count = content.count(symbol)
        print(f"Symbol '{symbol}' appears {count} times in '{file_path}'.")
        return count
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python3 count_symbol.py <file_path> <symbol>")
    else:
        count_symbol_in_file(sys.argv[1], sys.argv[2])
