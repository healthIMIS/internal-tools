# !/usr/bin/python3

import sys
import getopt
import yaml
from yaml.constructor import ConstructorError
import subprocess


def continue_prompt(filename):
    print(f"This will overwrite the following file: {filename} and encrypt all variables inside.\n"
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


def main(argv):
    vault_filename = ""
    password_filename = ""
    try:
        opts, args = getopt.getopt(argv, "hv:p:")
    except getopt.GetoptError:
        print('usage: encrypt_vault_variables.py -v <vaultfile> -p <passwordfile>')
        sys.exit(2)
    if len(sys.argv) < 2:
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

    encrypted_vault = ""

    print("Reading vault file...")

    with open(vault_filename, "r") as stream:
        try:
            config = yaml.safe_load(stream)
            for variable in config:
                print(f"Encrypting variable: {variable} ...")
                encrypted_vault += subprocess.check_output(
                    ['ansible-vault', 'encrypt_string', '--vault-password-file', password_filename, config[variable],
                     '--name', variable]).decode("utf-8")
        except yaml.YAMLError as exc:
            if isinstance(exc, yaml.constructor.ConstructorError) and "!vault" in exc.problem:
                print("Failed to parse yaml file. It seems like your variables already are encrypted.")
            else:
                print(exc)
            sys.exit(2)

    print("Rewriting vault file...")

    with open(vault_filename, "w") as file:
        file.writelines(encrypted_vault)

    print("Done. Your variables are now encrypted to be used with ansible vault.")


if __name__ == "__main__":
    main(sys.argv[1:])
