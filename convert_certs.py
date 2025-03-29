def pem_to_cpp_string(pem_path, var_name):
    with open(pem_path, "r") as f:
        lines = f.readlines()

    cpp_string = f'const char* {var_name} = \\\n'
    for line in lines:
        line = line.strip('\n')
        cpp_string += f'"{line}\\n" \\\n'
    cpp_string += ';\n'
    return cpp_string


# Archivos de entrada y nombres de variables
certs = [
    ("certificados/AmazonRootCA1.pem", "AWS_ROOT_CA"),
    ("certificados/device-certificate.pem.crt", "DEVICE_CERT"),
    ("certificados/device-private.pem.key", "PRIVATE_KEY")
]

# Crear el archivo certs.h
with open("certs.h", "w") as out:
    out.write("#ifndef CERTS_H\n#define CERTS_H\n\n")
    for pem_file, var_name in certs:
        try:
            cpp_code = pem_to_cpp_string(pem_file, var_name)
            out.write(cpp_code + "\n")
            print(f"✅ Procesado: {pem_file}")
        except FileNotFoundError:
            print(f" Archivo no encontrado: {pem_file}")
    out.write("#endif\n")