# !/usr/bin/python3

import sys
import getopt
import yaml
from yaml.constructor import ConstructorError
import subprocess


# see https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data
# Monkey Patch for dumping multline strings to blocks
def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)


def continue_prompt(filename: str) -> bool:
    print(
        f"This will overwrite the following file: {filename} and encrypt all vault variables (\"vault_...\") inside.\n"
        f"Do you want to continue? (Y/n)")

    yes = {'yes', 'y', ''}
    no = {'no', 'n'}

    while True:
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'.\n")


def load_yaml(filename: str) -> dict:
    with open(filename, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            if isinstance(exc, yaml.constructor.ConstructorError) and "!vault" in exc.problem:
                print("Failed to parse yaml file. It seems like your variables already are encrypted.")
            else:
                print(exc)
            sys.exit(2)


def recursive_vault_dict(dictionary: dict, password_filename: str) -> dict:
    vault_dictionary = dict()
    for key in dictionary:
        if isinstance(dictionary[key], dict):
            vault_dictionary[key] = recursive_vault_dict(dictionary[key], password_filename)
        else:
            if str(key).startswith("vault_"):
                print(f"Found vault variable: {key}")
                if str(dictionary[key]).startswith("!vault |"):
                    print(f"-> Variable: {key} is already encrypted. Skipping encryption...")
                    vault_dictionary[key] = dictionary[key]
                else:
                    print(f"-> Encrypting variable: {key} ...")
                    encrypted_parameter_string = subprocess.check_output(
                        ['ansible-vault', 'encrypt_string', '--vault-password-file', password_filename,
                         dictionary[key]]).decode("utf-8")
                    vault_dictionary[key] = encrypted_parameter_string
            else:
                vault_dictionary[key] = dictionary[key]
    return vault_dictionary


def main(argv):
    vault_filename = ""
    password_filename = ""
    try:
        opts, args = getopt.getopt(argv, "hv:p:")
    except getopt.GetoptError:
        print('usage: encrypt_vault_variables.py -v <vaultfile> -p <passwordfile>')
        sys.exit(2)
    if len(argv) < 4:
        print('usage: encrypt_vault_variables.py -v <vaultfile> -p <passwordfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: encrypt_vault_variables.py -i <vaultfile> -p <passwordfile>')
            sys.exit()
        elif opt in "-v":
            vault_filename = arg
        elif opt in "-p":
            password_filename = arg

    continue_prompt(vault_filename)

    print("Reading vault file...")

    config = load_yaml(vault_filename)

    vault_config = recursive_vault_dict(config, password_filename)

    print("Rewriting vault file...")

    with open(vault_filename, 'w', encoding='utf8') as outfile:
        yaml.representer.SafeRepresenter.add_representer(str, str_presenter)
        yaml.safe_dump(vault_config, outfile, default_flow_style=False, sort_keys=False)

    # Manually transforming multiline strings into vault lines

    with open(vault_filename, "r") as stream:
        lines = stream.readlines()

    for line in lines:
        if line.endswith(": |\n"):
            nextline = lines[lines.index(line) + 1]
            if str.lstrip(nextline).startswith("!vault |"):
                lines[lines.index(line)] = line[:-2] + str.lstrip(nextline)
                lines.remove(nextline)

    with open(vault_filename, "w") as stream:
        stream.writelines(lines)

    print("Done. Your variables are now encrypted to be used with ansible vault.")


if __name__ == "__main__":
    main(sys.argv[1:])
