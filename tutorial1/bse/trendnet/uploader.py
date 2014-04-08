'''
Created on Apr 4, 2014

@author: I028663
'''



if __name__ == '__main__':
    import paramiko
    
    host = "motorbox@smsi.bg"                    #hard-coded
    port = 21
    transport = paramiko.Transport((host, port))
    
    password = "smsibgqx"                #hard-coded
    username = "R_3KkmW7C?s="                #hard-coded
    transport.connect(username = username, password = password)
    
    sftp = paramiko.SFTPClient.from_transport(transport)
    files = sftp.listdir()
    
    sftp.close()
    transport.close()
    
    for file_name in files:
        print file_name
    pass