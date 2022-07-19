import os
import re

def set_server(path: str, ip: str, wls: bool) -> None:
    print("Setting server for " + path + " to " + ip)
    with open(path, 'r') as f:
        # Create a temporary file to store the new .wrl
        with open('temp.wrl', 'w') as temp:
            # Locate and empty every field cpBureau and cpBureauWLS
            try:
                for line in f:
                    if 'cpBureau' or 'cpBureauWLS' in line:
                        line = re.sub(r'(cpBureau(WLS)?\s*)".*"', r'\1""', line)
                
                    # If we are using WLS, replace the WLS field with the ip
                    if wls and 'cpBureauWLS' in line:
                            line = re.sub(r'(cpBureauWLS\s*)".*"', r'\1"{}"'.format(ip), line)
                    # If we are not using WLS, replace the non-WLS field with the ip
                    elif not wls and 'cpBureau' in line:
                        line = re.sub(r'(cpBureau\s*)".*"', r'\1"{}"'.format(ip), line)
                
                    temp.write(line)
            except:
                print("Error setting server for " + path)
                return
    
    # Replace the original .wrl with the new .wrl
    os.remove(path)

    os.rename('temp.wrl', path)