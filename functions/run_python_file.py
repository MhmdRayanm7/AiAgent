import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'


        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output_lines = []

        if result.returncode != 0:
            output_lines.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output_lines.append("No output produced")
        else:
            if result.stdout:
                output_lines.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_lines.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output_lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
