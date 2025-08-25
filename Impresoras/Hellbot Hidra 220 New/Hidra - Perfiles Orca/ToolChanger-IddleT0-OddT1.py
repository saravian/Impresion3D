import zipfile
import xml.etree.ElementTree as ET
import os
import shutil

def assign_extruders_by_color(input_3mf, output_3mf):
    temp_dir = "temp_3mf"
    os.makedirs(temp_dir, exist_ok=True)

    # Paso 1: Descomprimir el archivo .3mf
    with zipfile.ZipFile(input_3mf, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    scene_path = os.path.join(temp_dir, "3D", "scene.xml")
    tree = ET.parse(scene_path)
    root = tree.getroot()

    # Paso 2: Reasignar extrusores según ID de material
    for item in root.findall(".//{http://schemas.microsoft.com/3dmanufacturing/2013/01}object"):
        for mesh in item.findall(".//{http://schemas.microsoft.com/3dmanufacturing/2013/01}mesh"):
            for triangle in mesh.findall(".//{http://schemas.microsoft.com/3dmanufacturing/2013/01}triangle"):
                pid = triangle.attrib.get("pid")
                if pid is not None:
                    pid_int = int(pid)
                    # Asignar extrusor según par/impar
                    triangle.attrib["p1"] = "0" if pid_int % 2 == 1 else "1"

    # Paso 3: Guardar el XML modificado
    tree.write(scene_path)

    # Paso 4: Reempaquetar el archivo .3mf
    with zipfile.ZipFile(output_3mf, 'w', zipfile.ZIP_DEFLATED) as zip_out:
        for foldername, subfolders, filenames in os.walk(temp_dir):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                arcname = os.path.relpath(filepath, temp_dir)
                zip_out.write(filepath, arcname)

    # Limpieza
    shutil.rmtree(temp_dir)
    print(f"Archivo modificado guardado como: {output_3mf}")

# Ejemplo de uso
assign_extruders_by_color("modelo_original.3mf", "modelo_dualcolor.3mf")
