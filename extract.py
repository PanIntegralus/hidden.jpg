import sys
import os

def is_text(data):
    try:
        data.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

if len(sys.argv) != 2:
    print(f"{sys.argv[0]} input_file")
    sys.exit(1)

input_file = sys.argv[1]
base_name, ext = os.path.splitext(input_file)
output_file = f"{base_name}_hidden"

try:
    with open(input_file, 'rb') as f:
        contenido = f.read()

    jpg_end = contenido.find(bytes([0xFF, 0xD9]))
    if jpg_end == -1:
        print("Invalid file.")
        sys.exit(1)

    hidden_data = contenido[jpg_end + 2:]

    if hidden_data:
        if hidden_data.startswith(b'PK'):
            output_file += '.zip'
        elif hidden_data.startswith(b'%PDF'):
            output_file += '.pdf'
        elif hidden_data.startswith(b'\x89PNG'):
            output_file += '.png'
        elif is_text(hidden_data):
            output_file += '.txt'
        else:
            output_file += '.bin'

    with open(output_file, 'wb') as f:
        f.write(hidden_data)

    print(f"Extracted file saved as: {output_file}")

except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
