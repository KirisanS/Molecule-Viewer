'''
Name: Kirisan Suthanthireswaran
ID: 1186029
Assignment: 2
Due Date: 2023/02/28 
'''

import molecule




'''radius = { 'H' : 25,
           'C' : 40,
           'O' : 40,
           'N' : 40,
         };

element_name = { 'H' : 'grey',
                 'C' : 'black',
                 'O' : 'red',
                 'N' : 'blue',
               }'''

header = """"""

footer = """</svg>""";

offsetx = 500;
offsety = 500;


#Atom Class: Wrapper class for the atom_c struct. 
class Atom():

    #Atom Class Constructur: Takes in one arguement (atom_c struct) and sets member variables
    def __init__ (self,atom):
        self.atom = atom
        self.z = atom.z
        
    #__st__ method: Returns the contents of the atom 
    def __str__ (self):
        contentString = self.atom.element, self.atom.x, self.atom.y, self.atom.z
        return contentString

    #svg method: Creates svg string to display the current atom depending on its values and element 
    def svg(self):
        svgString = ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % ((self.atom.x * 100.0) + offsetx, (self.atom.y * 100.0) + offsety,
        radius[self.atom.element], element_name[self.atom.element])
        return svgString

#Bond Class: Wrapper class for bond structure in c
class Bond():

    #Bond Class Constructur: Takes in one argument (Bond structure) and sets member variables
    def __init__(self, bond):
        self.bond = bond
        self.z = bond.z
    
    #__str__ method: Returns the contents of the bond structure
    def __str__(self):
        bondString = "Bond: ", "A1: ",self.bond.a1, "A2: ",self.bond.a2, "epairs: ",self.bond.epairs, 
        "\nX1: ",self.bond.x1, "Y1: ",self.bond.y1, "X2: ",self.bond.x2, "Y2: ",self.bond.y2, 
        "Z: ",self.bond.z, "\nLength: ",self.bond.len, "dx: ", self.bond.dx, "dy: ", self.bond.dy
        return bondString

    #svg method: Computes the svg line that represents the bond between two molecules. 
    def svg(self):
        bondString = ' <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (((self.bond.x1 * 100.0) + offsetx + self.bond.dy*10.0), 
        ((self.bond.y1 * 100.0 + offsety) - self.bond.dx*10.0),
        (self.bond.x1 * 100.0 + offsetx - self.bond.dy*10.0), ((self.bond.y1 * 100.0 + offsety) + self.bond.dx*10.0),
        (self.bond.x2 * 100.0 + offsetx - self.bond.dy*10.0), ((self.bond.y2 * 100.0 + offsety) + self.bond.dx*10.0),
        (self.bond.x2 * 100.0 + offsetx + self.bond.dy*10.0), ((self.bond.y2 * 100.0 + offsety) - self.bond.dx*10.0))
        return bondString

#Molecule Class: subclass of the molecule structre in c
class Molecule(molecule.molecule):

    #Molecule Class Constructor: sets molecule
    def __init__(self):
        super().__init__()

        

    #__str__ method: Returns each atom and bond within the molecule
    def __str__(self):
        for i in range(self.atom_no):
            atom = self.get_atom(i)
            print("Atom (%d) : " % i, atom.element, atom.x, atom.y, atom.z)
        
        for i in range(self.bond_no):
            bond = self.get_bond(i)
            print("Bond: ", bond.a1, bond.a2, bond.epairs, bond.x1, bond.y1, bond.x2, bond.y2, "z:",bond.z, "len:",bond.len,
            "dx", bond.dx, "dy", bond.dy)
    
    #svg method: creates the svg of the molecule 
    def svg(self):
        svgString = header

        atomStack = []
        bondStack = []

        #Creates a stack of each atom and bond
        for i in range(self.atom_no):
            atom = self.get_atom(i)
            atomStack.append(atom)
        for i in range(self.bond_no):
            bond = self.get_bond(i)
            bondStack.append(bond)

        #While both have something in the stack, pop it out and compare z values
        while atomStack and bondStack:

            a1 = atomStack[0]
            b1 = bondStack[0]

            #Add either atom or bond to the svgString based on their respective class
            if a1.z < b1.z:
                if atomStack:
                    atomClass = Atom(a1)
                    svgString = svgString + atomClass.svg()
                    atomStack.pop(0)

            elif b1.z < a1.z:
                if bondStack:
                    bondClass = Bond(b1)
                    svgString = svgString + bondClass.svg()
                    bondStack.pop(0)

        #If there exists some atoms/bonds still in the stack, add them to the svgString 
        while atomStack:
            a1 = atomStack.pop(0)
            atomClass = Atom(a1)
            svgString = svgString + atomClass.svg()
            
        while bondStack:
            bondClass = Bond(b1)
            svgString = svgString + bondClass.svg()
            b1 = bondStack.pop(0)



        svgString = svgString + footer
        return svgString

    #parse method: Reading from an svg file to obtain atoms and bonds of the molecule
    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def parse(self, file):

        #Reading in the filler lines from the svg
        headerLine = file.readline()
        filler = file.readline() + file.readline()

        #Reading in the amount of atoms and bonds 
        count = file.readline().split()

        if(count[0].isdigit() and count[1].isdigit):
            atomCount = count[0]
            bondCount = count[1]
        else:
            return -1

        #Appending each atom to the current molecule
        for i in range(int(atomCount)):
            currentAtom = file.readline().split()

            if (self.isfloat(currentAtom[0]) and self.isfloat(currentAtom[1])
                and self.isfloat(currentAtom[2]) and len(currentAtom[3]) <= 2):
                self.append_atom(currentAtom[3], float(currentAtom[0]), float(currentAtom[1]), float(currentAtom[2]))
            else:
                return -1



        #Appending each bond to the current molecule
        for j in range(int(bondCount)):
            currentBond = file.readline().split()
            if(currentBond[0].isdigit() and currentBond[1].isdigit() and currentBond[2].isdigit()):
                self.append_bond(int(currentBond[0])-1  , int(currentBond[1])-1, int(currentBond[2]))
            else:
                return -1
        return 0
