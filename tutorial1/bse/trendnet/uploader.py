'''
Created on Apr 4, 2014

@author: I028663
'''



if __name__ == '__main__':
    import paramiko
    
    host = "THEHOST.com"                    #hard-coded
    port = 22
    transport = paramiko.Transport((host, port))
    
    password = "THEPASSWORD"                #hard-coded
    username = "THEUSERNAME"                #hard-coded
    transport.connect(username = username, password = password)
    
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    import sys
    path = './THETARGETDIRECTORY/' + sys.argv[1]    #hard-coded
    localpath = sys.argv[1]
    sftp.put(localpath, path)
    
    sftp.close()
    transport.close()
    print 'Upload done.'
    pass