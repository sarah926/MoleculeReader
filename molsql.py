import os;
import sqlite3;
import MolDisplay;
from colour import Color
header = """<html><script src="test.js"></script><head><link rel="stylesheet" type="text/css" href="style.css" /></head>\n<body>""";
footer = """</body></html>""";
class Database:
    
    def __init__(self, reset=False):
        if(reset == True):
            os.remove('molecules.db');
        self.conn = sqlite3.connect('molecules.db');
        self.cursor = self.conn.cursor();
    #create all the tables to store data
    def create_tables(self):
            self.cursor.execute(  """CREATE TABLE IF NOT EXISTS Elements
                                    ( ELEMENT_NO INTEGER NOT NULL,
                                    ELEMENT_CODE VARCHAR(3) NOT NULL,
                                    ELEMENT_NAME VARCHAR(32) NOT NULL,
                                    COLOUR1 CHAR(6) NOT NULL,
                                    COLOUR2 CHAR(6) NOT NULL,
                                    COLOUR3 CHAR(6) NOT NULL,
                                    RADIUS DECIMAL(3) NOT NULL,
                                    PRIMARY KEY (ELEMENT_NO)); """);
            self.cursor.execute(  """CREATE TABLE IF NOT EXISTS Atoms
                                    ( ATOM_ID INTEGER NOT NULL,
                                    ELEMENT_CODE VARCHAR(3) NOT NULL,
                                    X DECIMAL(7,4) NOT NULL,
                                    Y DECIMAL(7,4) NOT NULL,
                                    Z DECIMAL(7,4) NOT NULL,
                                    PRIMARY KEY (ATOM_ID),
                                    FOREIGN KEY (ELEMENT_CODE) REFERENCES Elements(ELEMENT_CODE)); """);
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Bonds
                                    (BOND_ID INTEGER NOT NULL,
                                    A1 INTEGER NOT NULL,
                                    A2 INTEGER NOT NULL,
                                    EPAIRS INTEGER NOT NULL,
                                    PRIMARY KEY (BOND_ID));""");
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS Molecules
                                (MOLECULE_ID INTEGER NOT NULL,
                                NAME TEXT NOT NULL UNIQUE,
                                PRIMARY KEY (MOLECULE_ID));""");
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoleculeAtom
                                (MOLECULE_ID INTEGER NOT NULL,
                                ATOM_ID INTEGER NOT NULL,
                                PRIMARY KEY(MOLECULE_ID, ATOM_ID),
                                FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID),
                                FOREIGN KEY(ATOM_ID) REFERENCES Atoms(ATOM_ID));""");
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS MoleculeBond
                                (MOLECULE_ID INTEGER NOT NULL,
                                BOND_ID INTEGER NOT NULL,
                                PRIMARY KEY(MOLECULE_ID, BOND_ID),
                                FOREIGN KEY(BOND_ID) REFERENCES Bonds(BOND_ID),
                                FOREIGN KEY(MOLECULE_ID) REFERENCES Molecules(MOLECULE_ID));""");
    def __setitem__(self, table, values):
        if(table == 'Elements'):
            self.cursor.execute("""INSERT INTO ELEMENTS VALUES (?,?,?,?,?,?,?)""",values);
        elif(table == 'Atoms'):
            self.cursor.execute("""INSERT INTO ELEMENTS VALUES (?,?,?,?,?)""",values);
        elif(table == 'Bonds'):
            self.cursor.execute("""INSERT INTO ELEMENTS VALUES (?,?,?,?)""",values);
        else:
            self.cursor.execute("""INSERT INTO ELEMENTS VALUES (?,?)""",values);
    #add atom data to tables
    def add_atom(self, molname, atom):
        self.cursor.execute(f"""INSERT INTO Atoms(ELEMENT_CODE, X, Y, Z)
                            VALUES('{atom.element}', {atom.x}, {atom.y}, {atom.z});""");
        atom_id = self.cursor.execute(f"""SELECT ATOM_ID FROM Atoms WHERE X='{atom.x}' AND Y={atom.y} AND Z={atom.z} AND ELEMENT_CODE='{atom.element}';""").fetchone();
        mol_id = self.cursor.execute(f"""SELECT MOLECULE_ID FROM Molecules WHERE NAME='{molname}';""").fetchone();
        self.cursor.execute(f"""INSERT INTO MoleculeAtom
                            VALUES({mol_id[0]},{atom_id[0]});""");
        self.conn.commit();
    #add bond data to tables
    def add_bond(self,molname,bond):
        self.cursor.execute(f""" INSERT INTO Bonds(A1, A2, EPAIRS)
                                VALUES({bond.a1}, {bond.a2}, '{bond.epairs}');""");
        mol_id = self.cursor.execute(f"""SELECT MOLECULE_ID FROM Molecules WHERE NAME='{molname}'""").fetchone();
        bond_id = self.cursor.execute(f"""SELECT BOND_ID FROM Bonds WHERE A1={bond.a1} AND A2 = {bond.a2} AND EPAIRS={bond.epairs}""").fetchone();
        self.cursor.execute(f"""INSERT INTO MoleculeBond
                                VALUES({mol_id[0]}, {bond_id[0]});""");
        self.conn.commit();
    #add molecule data to tables
    def add_molecule(self, name, fp):
        mol = MolDisplay.Molecule();
        mol.parse(fp);
        try:
            self.cursor.execute(f"""INSERT INTO Molecules(NAME)
                                VALUES ('{name}'); """);
        except sqlite3.IntegrityError as e:
            print("unique constraint failed");
            return;
        for i in range(mol.atom_no):
            atom = mol.get_atom(i);
            self.add_atom(name, atom);
        for i in range(mol.bond_no):
            bond = mol.get_bond(i);
            self.add_bond(name, bond);
        self.conn.commit();
    
    #loads data from tables into molecules
    def load_mol(self, name):
        mol = MolDisplay.Molecule();
        #with joins
        atoms = self.cursor.execute(f""" SELECT * FROM Molecules, MoleculeAtom, Atoms WHERE (Molecules.NAME = '{name}' AND Atoms.ATOM_ID = MoleculeAtom.ATOM_ID AND Molecules.MOLECULE_ID = MoleculeAtom.MOLECULE_ID) ORDER BY Atoms.ATOM_ID""").fetchall();
        bonds = self.cursor.execute(f"""SELECT * FROM Molecules, MoleculeBond, Bonds WHERE (Molecules.NAME = '{name}' AND Bonds.BOND_ID = MoleculeBond.BOND_ID AND Molecules.MOLECULE_ID = MoleculeBond.MOLECULE_ID) ORDER BY Bonds.BOND_ID""").fetchall();
       #add atoms and bonds
        for i in range(len(atoms)):
            mol.append_atom(atoms[i][5], atoms[i][6], atoms[i][7], atoms[i][8]);
        for i in range(len(bonds)):
            mol.append_bond(bonds[i][5], bonds[i][6], bonds[i][7]);
        self.conn.commit();
        return mol;
    
    #create radius dictionary to map element code to radius
    def radius(self):
        element_num = self.cursor.execute(f""" SELECT COUNT(*) FROM Elements""").fetchone();
        element_list = self.cursor.execute(f""" SELECT ELEMENT_CODE FROM Elements""").fetchall();
        rad_dictionary = {};
        for i in range(0,int(element_num[0])):
            rad = self.cursor.execute(f""" SELECT RADIUS FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            rad_dictionary[element_list[i][0]] = rad[0];
        return rad_dictionary;

    #create element name dictionary to map element code to element name
    def element_name(self):
        element_num = self.cursor.execute(f""" SELECT COUNT(*) FROM Elements""").fetchone();
        element_list = self.cursor.execute(f""" SELECT ELEMENT_CODE FROM Elements""").fetchall();
        name_dictionary = {}
        for i in range(0, int(element_num[0])):
            name = self.cursor.execute(f""" SELECT ELEMENT_NAME FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            name_dictionary[element_list[i][0]] = name[0];
        return name_dictionary;

    #returns radial gradients for all the elements
    def radial_gradients(self):
        returning = "";
        element_num = self.cursor.execute(f""" SELECT COUNT(*) FROM Elements""").fetchone();
        element_list = self.cursor.execute(f""" SELECT ELEMENT_CODE FROM Elements""").fetchall();
        
        for i in range(0, int(element_num[0])):
            name = self.cursor.execute(f""" SELECT ELEMENT_NAME FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            colour1 = self.cursor.execute(f""" SELECT COLOUR1 FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            colour2 = self.cursor.execute(f""" SELECT COLOUR2 FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            colour3 = self.cursor.execute(f""" SELECT COLOUR3 FROM Elements WHERE ELEMENT_CODE='{element_list[i][0]}'""").fetchone();
            radialGradientSVG = """
    <radialGradient id="%s" cx="-50%%" cy="-50%%" r="220%%" fx="20%%" fy="20%%">
        <stop offset="0%%" stop-color="#%s"/>
        <stop offset="50%%" stop-color="#%s"/>
        <stop offset="100%%" stop-color="#%s"/>
    </radialGradient>""" % (name[0], colour1[0], colour2[0], colour3[0])
            returning = returning + radialGradientSVG; 
        return returning;

    def makeMolListSVG(self):
        list = header + """ <h1>Current Molecule List</h1>""" +"""<ol style="border: 2px solid blue">\n"""
        mol_num = self.cursor.execute(f""" SELECT COUNT(*) FROM Molecules""").fetchone();
        mol_list =  self.cursor.execute(f""" SELECT NAME FROM Molecules""").fetchall();
        for i in range(0,int(mol_num[0])):
            bond_num = self.cursor.execute(f""" SELECT COUNT(*) FROM MoleculeBond WHERE MOLECULE_ID = {i+1}""").fetchone();
            atom_num = self.cursor.execute(f""" SELECT COUNT(*) FROM MoleculeAtom WHERE MOLECULE_ID = {i+1}""").fetchone();
            list = list + """   <li id="list1"><a href="/view/%s">%s: [%d atoms %d bonds]</li>\n""" % (mol_list[i][0],mol_list[i][0], int(atom_num[0]), int(bond_num[0]))
        list = list + """</ol>""" + """ <form action="home" enctype="multipart/form-data" method="post">
        <button type="submit" id="back">Back</button>
    </form>""" +footer;
        #print(list)
        return list;

    def makeElementListSVG(self):
        elementList = header + """<ol style="border: 2px solid blue">\n""";
        dict = self.element_name();
        keys = list(dict.keys());
        for i in range(0,len(dict)):
            elementList = elementList + """   <li id="list1"><a href="/element_list">%s: %s</li>\n""" % (keys[i], dict[keys[i]]);
        elementList = elementList + """</ol>""" + footer;
        #print(elementList);
        return elementList;
    def validateElement(self, values):
        print("hi");
        #validate element number
        if(values[0].isnumeric() == False or int(values[0])>118 or int(values[0])<0 or len(values[0]) == 0):
            print("val1")
            return False;
        #validate element code
        elif(len(values[1]) >2 or len(values[1]) ==0 or values[1].isnumeric() == True):
            print("val2")
            return False;
        #validate elmenet name
        elif(values[2].isnumeric()==True or len(values[2]) == 0):
            print("val3")
            return False;
        #validate colors 1-3
        elif(len(values[3])>0 and len(values[4]) >0 and len(values[5])>0):
            try:
                Color(values[3]);
                Color(values[4]);
                Color(values[5]);
            except:
                print("exc")
                return False;
        #validate radius
        if(values[6].isnumeric==False or int(values[6])<=0 or len(values[6])==0):
            print("val7");
            return False;
        return True;
    def validateRemoveElement(self, code):
        total = self.cursor.execute(""" SELECT COUNT(*) FROM ELEMENTS""").fetchone();
        #4 default that can not be removed
        dict = self.element_name();
        if(code in dict.keys()):
            return False;
        elif(code == "H" or code == "C" or code == "N" or code == "O"):
            return False;
        return True;
    def removeElement(self, code):
        try:
            self.cursor.execute(f""" DELETE FROM Elements WHERE ELEMENT_CODE ={code}""");
        except:
            print("fail");

if __name__ == "__main__":
    # db = Database(reset=True);
    # db.create_tables();
    # db['Elements'] = ( 1, 'H', 'Hydrogen', 'FFFFFF', '050505', '020202', 25 );
    # db['Elements'] = ( 6, 'C', 'Carbon', '808080', '010101', '000000', 40 );
    # db['Elements'] = ( 7, 'N', 'Nitrogen', '0000FF', '000005', '000002', 40 );
    # db['Elements'] = ( 8, 'O', 'Oxygen', 'FF0000', '050000', '020000', 40 );
    # fp = open( 'water-3D-structure-CT1000292221.sdf' );
    # db.add_molecule( 'Water', fp );
    # fp = open( 'caffeine-3D-structure-CT1001987571.sdf' );
    # db.add_molecule( 'Caffeine', fp );
    # fp = open( 'CID_31260.sdf' );
    # db.add_molecule( 'Isopentanol', fp );
    # # display tables
    # # print( db.conn.execute( "SELECT * FROM Elements;" ).fetchall() );
    # # print( db.conn.execute( "SELECT * FROM Molecules;" ).fetchall() );
    # # print( db.conn.execute( "SELECT * FROM Atoms;" ).fetchall() );
    # # print( db.conn.execute( "SELECT * FROM Bonds;" ).fetchall() );
    # # print( db.conn.execute( "SELECT * FROM MoleculeAtom;" ).fetchall() );
    # # print( db.conn.execute( "SELECT * FROM MoleculeBond;" ).fetchall() )
    # db = Database(reset=False); # or use default
    # db.create_tables();
    # MolDisplay.radius = db.radius();
    # MolDisplay.element_name = db.element_name();
    # MolDisplay.header += db.radial_gradients();
    
    # for molecule in [ 'Water','Caffeine', 'Isopentanol' ]:
    #     mol = db.load_mol( molecule );
    #     mol.sort();
    #     fp = open( molecule + ".svg", "w" );
    #     fp.write( mol.svg() );
    #     fp.close();
    # db.makeMolListSVG();
    try:
        b = Color("red");
    except:
        print(b);
