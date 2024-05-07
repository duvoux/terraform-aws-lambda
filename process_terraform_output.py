# coding: utf-8

import subprocess
import json
import sys

def run_command(module_name='lambda'):
    # Running the 'terraform show -json' command
    terraform_show = subprocess.Popen(["terraform", "show", "-json"], stdout=subprocess.PIPE)
    output, error = terraform_show.communicate()

    if error:
        print(json.dumps({"error": str(error)}))
        sys.exit(1)

    # Parsing the JSON output from 'terraform show'
    terraform_data = json.loads(output)

    # Construct the address string using the module_name parameter
    target_address = f"module.{module_name}.null_resource.archive[0]"
    # Extracting the specific resource ID based on the dynamically constructed address
    for index in terraform_data["values"]["root_module"]["child_modules"]:
        for resource in index["resources"]:
            if resource.get('address') == target_address:
                print(json.dumps({"timestamp": resource.get('values', {}).get('triggers').get('timestamp')}))
                return

    # If the resource is not found, output an empty JSON
    print(json.dumps({"timestamp": ""}))

if __name__ == "__main__":
    # Check if a module name is provided as a command-line argument, otherwise default to 'lambda'
    module_name = sys.argv[1] if len(sys.argv) > 1 else 'lambda'
    run_command(module_name)


