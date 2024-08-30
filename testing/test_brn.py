import os
#sudo mkdir -p /root/.hidden_dir
#echo -e "pos_id: 1\nbrn: add5008577937ea6a3227b496eda41f92fb8630db42639efb89197cefb4e77a5617b766ddc1ab5da" | sudo tee /root/.hidden_dir/secret_file.txt > /dev/null

# Define the path to the secret file
secret_file_path = os.path.expanduser("~/.hidden_dir/secret_file.txt")

# Read the file contents
with open(secret_file_path, 'r') as file:
    secret_data = file.read()

# Split the secret data into pos_id and brn
secret_lines = secret_data.strip().splitlines()
pos_id = secret_lines[0].split(': ')[1]
brn = secret_lines[1].split(': ')[1]

print(brn)
print(pos_id)