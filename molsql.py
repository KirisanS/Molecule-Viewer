import os;
import sqlite3;
#import molecule as cMolecule
import MolDisplay

# DataBase Class that handles the creation of the molecule database
class Database():

    #__init__(): Database constructor that creates a new database. If reset == true, it creates a fresh
    # new database
    def __init__(self, reset=False):
      if (reset == True):
        os.remove('molecules.db')
      self.data = sqlite3.connect('molecules.db')
    
    # create_tables(): Creates the required tables in the database
    def create_tables(self):
      self.data.execute("""CREATE TABLE IF NOT EXISTS Elements 
                  ( ELEMENT_NO    INTEGER     NOT NULL,
                    ELEMENT_CODE  VARCHAR(3)  NOT NULL,
                    ELEMENT_NAME  VARCHAR(32) NOT NULL,
                    COLOUR1       CHAR(6)     NOT NULL,
                    COLOUR2       CHAR(6)     NOT NULL,
                    COLOUR3       CHAR(6)     NOT NULL,
                    RADIUS        DECIMAL(6)  NOT NULL,
                    PRIMARY KEY   (ELEMENT_CODE) );""")

      self.data.execute("""CREATE TABLE IF NOT EXISTS Atoms
                  ( ATOM_ID       INTEGER         PRIMARY KEY   AUTOINCREMENT   NOT NULL,
                    ELEMENT_CODE  VARCHAR(3)      NOT NULL,
                    X             DECIMAL(7, 4)   NOT NULL,
                    Y             DECIMAL(7, 4)   NOT NULL,
                    Z             DECIMAL(7, 4)   NOT NULL,
                    FOREIGN KEY   (ELEMENT_CODE)  REFERENCES Elements );""")

      self.data.execute("""CREATE TABLE IF NOT EXISTS Bonds
                  ( BOND_ID       INTEGER         PRIMARY KEY   AUTOINCREMENT   NOT NULL,
                    A1            INTEGER         NOT NULL,
                    A2            INTEGER         NOT NULL,
                    EPAIRS        INTEGER         NOT NULL)""")

      self.data.execute(""" CREATE TABLE IF NOT EXISTS Molecules
                  ( MOLECULE_ID   INTEGER         PRIMARY KEY   AUTOINCREMENT   NOT NULL,
                    NAME          TEXT            UNIQUE        NOT NULL);""")

      self.data.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom
                  ( MOLECULE_ID   INTEGER         NOT NULL,
                    ATOM_ID       INTEGER         NOT NULL,
                    PRIMARY KEY   (MOLECULE_ID,ATOM_ID),
                    FOREIGN KEY   (MOLECULE_ID)   REFERENCES Molecules,
                    FOREIGN KEY   (ATOM_ID)       REFERENCES Atoms);""")

      self.data.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond
                  ( MOLECULE_ID   INTEGER         NOT NULL,
                    BOND_ID       INTEGER         NOT NULL,
                    PRIMARY KEY   (MOLECULE_ID,BOND_ID),
                    FOREIGN KEY   (MOLECULE_ID)   REFERENCES Molecules,
                    FOREIGN KEY   (BOND_ID)       REFERENCES Bonds); """)

    # find_molecule_id(): Helper function that returns the Molecules ID 
    def find_molecule_id(self, molname):

      moleculeID = self.data.execute(f"""SELECT MOLECULE_ID 
                                        FROM   Molecules
                                        WHERE  NAME = "{molname}";""").fetchone()
      return (moleculeID[0])

    # __setitem__(): Set the inputted item into its specifided table
    def __setitem__(self, table, values):
      tempString = "( " + "?, "*(len(values)-1) + "? " + ")"

      self.data.execute(f"""INSERT OR IGNORE
                           INTO   {table}
                           VALUES {tempString}  ;""", values)
      self.data.commit()

    #add_atom(): Adds atom to the atom table and MoleculeAtom table
    def add_atom(self, molname, atom):

      self.__setitem__('Atoms',(None, atom.element, atom.x, atom.y, atom.z))
      moleculeID = self.find_molecule_id(molname)

      atomID = self.data.execute(f"""SELECT ATOM_ID
                                    FROM Atoms
                                    WHERE ELEMENT_CODE = "{atom.element}"
                                    AND X = {atom.x}
                                    AND Y = {atom.y}
                                    AND Z = {atom.z};""").fetchone()


      self.__setitem__('MoleculeAtom',(moleculeID, atomID[0]))
    
    #add_bond(): Adds bond to Bonds table and MoleculeBonds table
    def add_bond(self, molname, bond):
      self.__setitem__('Bonds',(None, bond.a1, bond.a2, bond.epairs))

      moleculeID = self.find_molecule_id(molname)

      bondID = self.data.execute(f"""SELECT BOND_ID
                                    FROM Bonds
                                    WHERE A1 = "{bond.a1}"
                                    AND A2 = {bond.a2}
                                    AND EPAIRS = {bond.epairs};""").fetchone()

      self.__setitem__('MoleculeBond',(moleculeID, bondID[0]))

    #add_molecule(): Parse sdf file and create a molecule to put into the database by calling add_atom 
    # and add_bond
    def add_molecule(self, name, mol):

      #moleculeClass = MolDisplay.Molecule(mol)

      self.__setitem__('Molecules', (None, name))

      atomCount = mol.atom_no
      bondCount = mol.bond_no

      # For each atom and bond, call respective method to add into the database
      for i in range(atomCount):  

        atom = mol.get_atom(i)
        self.add_atom(name, atom)

      for i in range(bondCount):

        bond = mol.get_bond(i)
        self.add_bond(name, bond)
        
    def delete_Element(self, values):
      self.data.execute(f"""DELETE FROM Elements
                         WHERE  Elements.ELEMENT_NO = {values['elementNo'][0]}
                         AND Elements.ELEMENT_NAME = "{values['elementName'][0]}" """)
      self.data.commit()
      
    #load_mol(): Load the molecule with information from the database
    def load_mol(self, name):
      #Finding the Molecule ID: 
      moleculeID = self.find_molecule_id(name)
      
      # Creating a joined table where the molecule ID's match between atoms and bonds
      table = self.data.execute(f"""SELECT ATOM_ID,BOND_ID FROM (MoleculeAtom INNER JOIN MoleculeBond
                           ON
                           MoleculeAtom.MOLECULE_ID = MoleculeBond.MOLECULE_ID)
                           WHERE MoleculeAtom.MOLECULE_ID = {moleculeID}
                           AND MoleculeBond.MOLECULE_ID = {moleculeID}""").fetchall()

      mol = MolDisplay.Molecule()

      # Atoms and Bonds
      uniqueAtomCheck = []
      uniqueBondCheck = []

      #Checking if it is an unique atom, then appending the information found in the joined table to the molecule
      for i in range(0, len(table)):
        if(table[i][0] not in uniqueAtomCheck):
          
          uniqueAtomCheck.append(table[i][0])
          row = self.data.execute(f"""SELECT *
                                     FROM Atoms
                                     WHERE ATOM_ID = {table[i][0]};""").fetchone()
          print(row[1])
          mol.append_atom(row[1], row[2], row[3], row[4])

      #Checking if it is an unique bond, then appending the information found in the joined table to the molecule
      for i in range(0, len(table)):
        if(table[i][1] not in uniqueBondCheck):
          uniqueBondCheck.append(table[i][1])
          row = self.data.execute(f"""SELECT *
                                     FROM Bonds
                                     WHERE BOND_ID = {table[i][1]};""").fetchone()

          mol.append_bond(row[1], row[2], row[3])

          

      return (mol)
      

    def select_Elements(self):
      table = self.data.execute(""" SELECT *
                                FROM Elements;""").fetchall()
      return table
    
    def select_Elements_Names(self):
      table = self.data.execute("""SELECT ELEMENT_NAME
                                FROM Elements""")
      return table
    def select_Elements_Code(self):
      table = self.data.execute("""SELECT ELEMENT_CODE
                                FROM Elements""")
      return table
    def select_Elements_No(self):
      table = self.data.execute("""SELECT ELEMENT_NO
                                FROM Elements""")
      return table
    def select_Molecule_Names(self):
      table = self.data.execute(""" SELECT NAME
                                from Molecules""").fetchall()
      return table

    def select_Molecule(self, name):
      moleculeID = self.find_molecule_id(name)

      table = self.data.execute(f"""SELECT ATOM_ID,BOND_ID FROM (MoleculeAtom INNER JOIN MoleculeBond
                           ON
                           MoleculeAtom.MOLECULE_ID = MoleculeBond.MOLECULE_ID)
                           WHERE MoleculeAtom.MOLECULE_ID = {moleculeID}
                           AND MoleculeBond.MOLECULE_ID = {moleculeID}""").fetchall()
      
      return(table)


    #radius(): Create dictionary for the radius of each element in the database
    def radius(self):
      
      elementRow = self.data.execute("""SELECT  ELEMENT_CODE, RADIUS
                                        FROM Elements;""").fetchall()

      atomRow = self.data.execute("""SELECT ELEMENT_CODE
                                     FROM Atoms""").fetchall()

      radius = {}


      check = 0
      for i in range(len(atomRow)):
        check = 0
        for j in range(len(elementRow)):

          if(atomRow[i][0] == elementRow[j][0]):
            radius[elementRow[j][0]] = elementRow[j][1]
            check = 1
            
        if(check == 0):
          radius[atomRow[i][0]] = 40


      return (radius)
    
    #element_name(): Create dictionary for each element_name 
    def element_name(self):
      
      elementRow = self.data.execute("""SELECT  ELEMENT_CODE, ELEMENT_NAME
                                        FROM Elements;""").fetchall()
      

      atomRow = self.data.execute("""SELECT ELEMENT_CODE
                                     FROM Atoms""").fetchall()
      print(atomRow)
      print(elementRow)
      element_name = {}

      check = 0
      for i in range(len(atomRow)):
        check = 0
        for j in range(len(elementRow)):
          if(atomRow[i][0] == elementRow[j][0]):
            element_name[elementRow[j][0]] = elementRow[j][1]
            check = 1
        if(check == 0):
          element_name[atomRow[i][0]] = "default"


      print("HUH!?" + element_name['H'])
      return (element_name)
    
    #radial_gradients(): Create the header svg for the gradients of each atom 
    def radial_gradients(self):

      elementTable = self.data.execute("""SELECT * 
                                          FROM Elements;""").fetchall()

      radialGradientSVG = ""
      
      #Default x``
      radialGradientSVG = radialGradientSVG + """
      <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/>
        <stop offset="50%%" stop-color="#%s"/>
        <stop offset="100%%" stop-color="#%s"/>
      </radialGradient>""" % ("default", "FFFFFF", "FFFFFF", "FFFFFF")


      for i in range(len(elementTable)):
        radialGradientSVG = radialGradientSVG + """
        <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
          <stop offset="0%%" stop-color="#%s"/>
          <stop offset="50%%" stop-color="#%s"/>
          <stop offset="100%%" stop-color="#%s"/>
        </radialGradient>""" % (elementTable[i][2], elementTable[i][3], elementTable[i][4], elementTable[i][5])

      return (radialGradientSVG + '\n')

'''if __name__ == "__main__":
  db = Database(reset=True);
  db.create_tables();
  db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
  db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
  db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
  db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
  fp = open( 'water-3D-structure-CT1000292221.sdf' );
  db.add_molecule( 'Water', fp );
  fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
  db.add_molecule( 'Caffeine', fp );
  fp = open( 'CID_31260.sdf' );
  db.add_molecule( 'Isopentanol', fp );

  MolDisplay.radius = db.radius();
  MolDisplay.element_name = db.element_name();
  MolDisplay.header += db.radial_gradients();
  for molecule in [ 'Water', 'Caffeine', 'Isopentanol']:
    mol = db.load_mol( molecule );
    mol.sort();
    fp = open( molecule + ".svg", "w" );
    fp.write( mol.svg() );
    fp.close();'''
