import os
import re
from decorators import box_on_error

@box_on_error("Error updating wrl list")
def set_server(path: str, ip: str, wls: bool) -> None:
    print("Setting server for " + path + " to " + ip)
    updated = False
    with open(path, 'r') as f:
        # Create a temporary file to store the new .wrl
        with open('temp.wrl', 'w') as temp:
            # Locate and empty every field cpBureau and cpBureauWLS
            for line in f:
                if 'cpBureau' or 'cpBureauWLS' in line:
                    line = re.sub(r'(cpBureau(WLS)?\s*)".*"', r'\1""', line)
            
                # If we are using WLS, replace the WLS field with the ip
                if wls and 'cpBureauWLS' in line:
                    line = re.sub(r'(cpBureauWLS\s*)".*"', r'\1"{}"'.format(ip), line)
                    updated = True    
                # If we are not using WLS, replace the non-WLS field with the ip
                elif not wls and 'cpBureau' in line:
                    line = re.sub(r'(cpBureau\s*)".*"', r'\1"{}"'.format(ip), line)
                    updated = True
            
                temp.write(line)
            
            if not updated:
                # We need to add the field in the correct place in the file
                temp.write('Sony_WorldInfo {\n')
                if wls:
                    temp.write('\tcpBureauWLS "{}"\n'.format(ip))
                    temp.write('\tcpBureau ""\n')
                else:
                    temp.write('\tcpBureauWLS ""\n')
                    temp.write('\tcpBureau "{}"\n'.format(ip))
                temp.write('}\n')
                
    
    
    # Replace the original .wrl with the new .wrl
    os.rename(path, path + ".OLD")
    os.rename('temp.wrl', path)
    # If we successfully renamed here, we can delete the old file
    os.remove(path + ".OLD")