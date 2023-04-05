'''
Name: Kirisan Suthanthireswaran
ID: 1186029
Assignment: 2
Due Date: 2023/02/28 
'''

import sys;
import MolDisplay
import molsql
import molecule
import json
import urllib
from http.server import HTTPServer 
from http.server import BaseHTTPRequestHandler

db = molsql.Database(reset=False)
db.create_tables()

currentFile = None
currentName = None
currentId = None
currentSVG = None
elementCheck = None
moleculeCheck = None
runCheck = 0

#BaseHTTPRequestHandler Class: Subclass of the BaseHTTPRequestHandler
class BaseHTTPRequestHandler(BaseHTTPRequestHandler):

    def open_File(self, fileName):
        file = open(fileName, "r")
        fileContents = file.read()
        return fileContents
    #do_GET method: Sends the home_page to the server, otherwise returns an error message
    def do_GET(self):

        #Home Page 
        if self.path == "/":
            
            fileContents = self.open_File("home.html")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", len(fileContents))
            self.end_headers()

            self.wfile.write(bytes(fileContents, "utf-8"))

        if self.path == "/elementPage":
           fileContents = self.open_File("element.html")
           self.send_response(200)
           self.send_header("Content-type", "text/html")
           self.send_header("Content-length", len(fileContents))
           self.end_headers()

           self.wfile.write(bytes(fileContents, "utf-8"))
           

        elif self.path == "/backgroundSVG":
           image = open("realTest.png", "rb")
           f = image.read()
           b = bytearray(f)
           self.send_response(200)
           self.send_header("Content-type", "image/jpeg")
           #self.send_header("Content-length", len(image))
           self.end_headers()

           self.wfile.write(b)
           
          
           

        elif self.path == "/sdfPage":
           fileContents = self.open_File("sdf.html")
           self.send_response(200)
           self.send_header("Content-type", "text/html")
           self.send_header("Content-length", len(fileContents))
           self.end_headers()
           self.wfile.write(bytes(fileContents, "utf-8"))

        elif self.path == "/moleculePage":
          fileContents = self.open_File("molecule.html")
          self.send_response(200)
          self.send_header("Content-type", "text/html")
          self.send_header("Content-length", len(fileContents))
          self.end_headers()
          self.wfile.write(bytes(fileContents, "utf-8"))
           

        elif self.path == "/currentElements":
           table = db.select_Elements()
           x = json.dumps(table)

           self.send_response(200)
           self.send_header("Content-type", "application/json")
           self.send_header("Content-length", len(x))
           self.end_headers()
           
           self.wfile.write(x.encode())
          
        elif self.path == "/currentMolecules":
            names = db.select_Molecule_Names()
            mainString = []

            for i in range(len(names)):
              mol = db.load_mol(names[i][0])

              string = (names[i][0],mol.atom_no, mol.bond_no)
              mainString.append(string)
            
            x = json.dumps(mainString)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Content-length", len(x))
            self.end_headers()
           
            self.wfile.write(x.encode())


        elif self.path == "/jquery.js":
           
            fileContents = self.open_File("jquery.js")
            self.send_response(200)
            self.send_header("Content-type", "application/javascript")
            self.send_header("Content-length", len(fileContents))
            self.end_headers()

            self.wfile.write(bytes(fileContents, "utf-8"))

        elif self.path == "/styles.css":
           
            fileContents = self.open_File("styles.css")
            self.send_response(200)
            self.send_header("Content-type", "text/css")
            self.send_header("Content-length", len(fileContents))
            self.end_headers()

            self.wfile.write(bytes(fileContents, "utf-8"))
 
        elif self.path == "/loadCurrentSVG":
          x = json.dumps(currentSVG)
          self.send_response(200)
          self.send_header("Content-type", "application/json")
          self.send_header("Content-length", len(x))
          self.end_headers()
            
          self.wfile.write(x.encode())

        elif self.path == "/viewMolecule":
          mol = db.load_mol( currentName )
          mol.sort()
          MolDisplay.radius = db.radius()
          MolDisplay.element_name = db.element_name()
          svgString = mol.svg()

          specialString = svgString.split()

          next = 0
          nexty = 0
          maxX = 0.0
          maxY = 0.0
          minX = 10000000.0
          minY = 10000000.0
          
          for i in specialString:
      
             if(nexty == 1):
              yString = i.strip("cy=\"")

              if(float(yString) < minY):
                 minY = float(yString)

              if(float(yString) > maxY):
                 maxY = float(yString)

              nexty = 0

             if(next == 1):
              xString = i.strip("cx=\"")
              
              if(float(xString) < minX):
                 minX = float(xString)


              if(float(xString) > maxX):
                 maxX = float(xString)
                 

              next = 0
              nexty = 1

             if(i == "<circle"):
                next = 1


          MolDisplay.header = f"""<svg version="1.1" id=\"svgT\"  width="700px" height="700px" viewBox="{minX-600} {minY-600} {maxX+600} {maxY+600}"\nxmlns="http://www.w3.org/2000/svg">
<rect x="0" y="0" width="100%" height="100%"/>"""
          MolDisplay.header += db.radial_gradients()

          svgString = mol.svg()
          x = json.dumps(svgString)
          self.send_response(200)
          self.send_header("Content-type", "application/json")
          self.send_header("Content-length", len(x))
          self.end_headers()
            
          self.wfile.write(x.encode())


        elif self.path == "/validateElement":
          string = str(elementCheck)
          x = json.dumps(string)
          self.send_response(200)
          self.send_header("Content-type", "application/json")
          self.send_header("Content-length", len(x))
          self.end_headers()
            
          self.wfile.write(x.encode())

        elif self.path == "/validateSDF":
          string = str(moleculeCheck)
          x = json.dumps(string)
          self.send_response(200)
          self.send_header("Content-type", "application/json")
          self.send_header("Content-length", len(x))
          self.end_headers()
            
          self.wfile.write(x.encode())
           
            
        else:
            self.send_response(404)
            self.end_headers()

            self.wfile.write(bytes("404: not found", "utf-8"))

    #do_POST: Outputs the molecule that has been parsed from the svg file inputed from the web server
    def do_POST(self):
      



      
      if self.path == "/load":
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        #print( repr( body.decode('utf-8') ) );
        postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

        elementNo = int(postvars['elementNo'][0])
        elementCode = postvars['elementCode'][0]
        elementName = postvars['elementName'][0]
        colour1 = postvars['colour1'][0]
        colour2 = postvars['colour2'][0]
        colour3 = postvars['colour3'][0]
        radius =  int(postvars['radius'][0])
        check = 0

        if(elementNo > 118 or elementNo < 1):
          check = 1
        elif(len(elementCode) > 2 or elementCode == None):
          check = 1
        elif(len(elementName) > 100):
           check = 1
        elif(radius < 1):
           check = 1
        
        if(len(colour1) == 6 and len(colour2) == 6 and len(colour3) == 6):
          for i in (colour1):
            if(i not in ("1234567890ABCDEF")):
                check = 1
                i = 1000000
            if(len(colour2) == 6):
              for i in (colour2):
                  if(i not in ("1234567890ABCDEF")):
                    check = 1
                    i = 1000000
            if(len(colour3) == 6):
              for i in (colour3):
                  if(i not in ("1234567890ABCDEF")):
                    check = 1
                    i = 1000000
        else:
           check = 1
      
            
        if(check == 0):
          listOfNames = db.select_Elements_Names()
          listOfCode = db.select_Elements_Code()
          listOfNo = db.select_Elements_No()
          
          for i in listOfNames:
            if(elementName == i[0]):
              check = 2
          for i in listOfCode:
            if(elementCode == i[0]):
              check = 2
          for i in listOfNo:
            if(elementNo == i[0]):
              check = 2
          
           

        global elementCheck
        elementCheck = check






        if(check == 0):
          db['Elements'] = (postvars['elementNo'][0], postvars['elementCode'][0], postvars['elementName'][0],
          postvars['colour1'][0],postvars['colour2'][0],postvars['colour3'][0],postvars['radius'][0],)

        message = ""
        self.send_response( 200 ); # OK
        self.send_header( "Content-type", "text/plain" );
        self.send_header( "Content-length", len(message) );
        self.end_headers();

        self.wfile.write( bytes( message, "utf-8" ) );

      elif self.path == "/removeElement":
         content_length = int(self.headers['Content-Length'])
         body = self.rfile.read(content_length)

         #print( repr( body.decode('utf-8') ) );
         postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )

         db.delete_Element(postvars)
         

      elif self.path == "/verifyName":
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
         


      elif self.path == "/uploadSDF":
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
        moleculeName = postvars[' name'][1]
        moleculeName = moleculeName.replace("\n"," ").replace("\r"," ").split()
        moleculeName = moleculeName[1]

        fileContents = postvars[' filename'][0]

        file = open("test.sdf", "w")
        file.write(fileContents) 
        file.close()

        file = open("test.sdf", "r")

        for i in range(3):
          file.readline()
        
        moleculeClass = MolDisplay.Molecule()
        check = moleculeClass.parse(file)

        moleculeNames = db.select_Molecule_Names()
        for i in range(len(moleculeNames)):
          if(moleculeName == moleculeNames[i][0] and i == 0):
              check = 2
          if(moleculeName == moleculeNames[i][0] and i != len(moleculeNames)-1):
             check = 2

        global moleculeCheck
        moleculeCheck = check
        if (check == 0):
          db.add_molecule(moleculeName, moleculeClass)
        self.send_response( 200 ); # OK


      elif self.path == "/sendId":
        self.send_response(200)
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )
        global currentName
        currentName = postvars['molName'][0]

      elif self.path == "/rotation":
        self.send_response(200)

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        postvars = urllib.parse.parse_qs( body.decode( 'utf-8' ) )


        xR = int(postvars['xR'][0])
        xY = int(postvars['xY'][0])
        xZ = int(postvars['xZ'][0])

        mol = db.load_mol( postvars['molName'][0])

        mol.sort()


        if(xR > 0):
          mx = molecule.mx_wrapper(xR,0,0)
          mol.xform(mx.xform_matrix)


        if(xY > 0):
          my = molecule.mx_wrapper(0,xY,0)
          mol.xform(my.xform_matrix)
        if(xZ > 0):
          mz = molecule.mx_wrapper(0,0,xZ)
          mol.xform(mz.xform_matrix)


        svgString = mol.svg()
        global currentSVG
        currentSVG = svgString
        

         
        

        

      elif self.path == "/setFile":

        self.send_response(200)


        #Skipping the first 4 lines
        for i in range(4):
          self.rfile.readline()


      else:
          self.send_response(404)
          self.end_headers()

          self.wfile.write( bytes("404: not found", "utf-8"))

        




#    <form action="molecule" enctype="multipart/form-data" method="post">

httpd = HTTPServer(('localhost', int(sys.argv[1])), BaseHTTPRequestHandler)

try: 
  httpd.serve_forever();
except KeyboardInterrupt:
  print('')

httpd.server_close()