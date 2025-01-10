import heapq
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter, namedtuple

# Node structure for the Huffman tree
class Node(namedtuple("Node", ["char", "freq", "left", "right"])):
    def _lt_(self, other):
        return self.freq < other.freq

# Build Huffman Tree
def build_huffman_tree(frequencies):
    heap = [Node(char, freq, None, None) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(heap, merged)

    return heap[0]

# Generate Huffman Codes
def generate_huffman_codes(tree, prefix="", code_map={}):
    if tree is None:
        return

    if tree.char is not None:
        code_map[tree.char] = prefix
    else:
        generate_huffman_codes(tree.left, prefix + "0", code_map)
        generate_huffman_codes(tree.right, prefix + "1", code_map)

    return code_map

# Compress File
def compress_file(input_file, output_file):
    try:
        with open(input_file, "r") as file:
            content = file.read()

        # Step 1: Count character frequencies
        frequencies = Counter(content)

        # Step 2: Build Huffman tree
        huffman_tree = build_huffman_tree(frequencies)

        # Step 3: Generate Huffman codes
        huffman_codes = generate_huffman_codes(huffman_tree)

        # Step 4: Encode content
        encoded_content = "".join(huffman_codes[char] for char in content)

        # Save compressed data and metadata
        with open(output_file, "wb") as file:
            metadata = {
                "huffman_codes": huffman_codes,
                "original_size": len(content),
            }
            file.write(str(metadata).encode())
            file.write(b"\n")
            file.write(encoded_content.encode())

        messagebox.showinfo("Success", f"File compressed and saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to compress file: {e}")

# Decompress File
def decompress_file(compressed_file, output_file):
    try:
        with open(compressed_file, "rb") as file:
            lines = file.readlines()
            metadata = eval(lines[0].decode())
            encoded_content = lines[1].decode()

        # Reverse Huffman codes
        huffman_codes = metadata["huffman_codes"]
        reverse_codes = {v: k for k, v in huffman_codes.items()}

        # Decode content
        current_code = ""
        decoded_content = ""
        for bit in encoded_content:
            current_code += bit
            if current_code in reverse_codes:
                decoded_content += reverse_codes[current_code]
                current_code = ""

        with open(output_file, "w") as file:
            file.write(decoded_content)

        messagebox.showinfo("Success", f"File decompressed and saved as {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to decompress file: {e}")

# GUI Implementation
def select_file(operation):
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    if operation == "compress":
        output_file = filedialog.asksaveasfilename(defaultextension=".huff", filetypes=[("Huffman File", "*.huff")])
        if output_file:
            compress_file(file_path, output_file)
    elif operation == "decompress":
        output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text File", "*.txt")])
        if output_file:
            decompress_file(file_path, output_file)

# Create the GUI Window
def create_gui():
    root = tk.Tk()
    root.title("File Compression Tool")
    root.geometry("400x200")
    root.resizable(False, False)

    # Title Label
    title_label = tk.Label(root, text="Huffman File Compression Tool", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Compress Button
    compress_button = tk.Button(root, text="Compress File", font=("Arial", 14), command=lambda: select_file("compress"))
    compress_button.pack(pady=10)

    # Decompress Button
    decompress_button = tk.Button(root, text="Decompress File", font=("Arial", 14), command=lambda: select_file("decompress"))
    decompress_button.pack(pady=10)

    # Exit Button
    exit_button = tk.Button(root, text="Exit", font=("Arial", 14), command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_gui()
