import hashlib
import json
import rsa

def generate_keys(seed):
    name = seed.get('name', '')
    uid = seed.get('uid', '')
    age = seed.get('age', '')
    
    # Concatenate name, uid, and age to generate seed for keys
    seed_str = f"{name}{uid}{age}"
    
    # Generate private key and public key using RSA algorithm
    private_key, public_key = rsa.newkeys(512, poolsize=8, exponent=65537)
    
    # Convert private key and public key to strings for storage
    private_key_str = private_key.save_pkcs1().decode('utf-8')
    public_key_str = public_key.save_pkcs1().decode('utf-8')
    
    # Add the private key and public key to the seed dictionary
    seed['private_key'] = private_key_str
    seed['public_key'] = public_key_str
    
    return seed

if __name__ == '__main__':
    # Example usage:
    input_dict = {
        "name": "User",
        "uid": "21634029147",
        "phone": "9012790217",
        "age": "43",
        "password": "iudgiusjisa"
    }
    print(generate_keys(input_dict))