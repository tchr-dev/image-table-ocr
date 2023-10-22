To call a function from the `table_ocr.extract_tables` module in your script, you'll first need to import the module and then invoke the desired function.

However, given that the author suggests running the module as a script directly from the terminal, it might be designed with a command-line interface in mind. If this is the case, the function or main behavior you want might be in the module's `if __name__ == "__main__":` block.

Let's break down the process:

1. **Import the Module Directly**: If the package is correctly installed, you can simply import the module and use its functions.

   ```python
   from table_ocr import extract_tables

   # Now use the functions from extract_tables, if they're available as public functions
   ```

2. **Use the `subprocess` Module**: If the desired behavior is only available when running the module as a script (i.e., in the `if __name__ == "__main__":` block), you can invoke it using the `subprocess` module:

   ```python
   import subprocess

   # Assuming you want to process the file /tmp/pdf-images.txt
   with open("/tmp/pdf-images.txt", "r") as f:
       files = [line.strip() for line in f]

   extracted_tables = []

   for file in files:
       result = subprocess.run(["python", "-m", "table_ocr.extract_tables", file], capture_output=True, text=True)
       if "table" in result.stdout:
           extracted_tables.append(result.stdout)

   with open("/tmp/extracted-tables.txt", "w") as f:
       for table in extracted_tables:
           f.write(table)
   ```

The above is a more "Pythonic" way of achieving the same behavior as the command-line pipeline you provided.

Note: Ensure that the `table_ocr` package is installed in the same Python environment as the one you're running your script in. Otherwise, the `import` statement or the `subprocess` call will fail.