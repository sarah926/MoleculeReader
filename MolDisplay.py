import molecule
import molsql
import pdb

header = """<html><svg version="1.1" width="1000" height="1000"
                    xmlns="http://www.w3.org/2000/svg">""";
footer = """</svg></html>""";
offsetx = 500;
offsety = 500;

class Atom:
    def __init__(self, c_atom):
        self.c_atom = c_atom;
        self.z = c_atom.z;
    def __str__(self):
        return '''%s'%f'%f'%f"''' % (self.element , self.x, self.y, self.z);
    def svg(self, rad, el):
        return ' <circle cx="%.2f" cy="%.2f" r="%d" fill="url(#%s)"/>\n' % (
            (self.c_atom.x * 100.0 + offsetx), 
            (self.c_atom.y * 100.0 + offsety), 
            rad[self.c_atom.element], 
            el[self.c_atom.element])

class Bond:
    def __init__(self, c_bond):
        self.c_bond = c_bond;
        self.z = c_bond.z;
    def __str__(self):
        return '''%d'%d'%d"''' % self.c_bond.x1, self.y1, self.z;
    def svg(self):
        return '  <polygon points="%.2f,%.2f %.2f,%.2f %.2f,%.2f %.2f,%.2f" fill="green"/>\n' % (
            ((self.c_bond.x1*100.0 + offsetx) - (self.c_bond.dy * 10.0)), 
            ((self.c_bond.y1*100.0 + offsety) + (self.c_bond.dx * 10.0)), 
            ((self.c_bond.x2*100.0 + offsetx) - (self.c_bond.dy * 10.0)), 
            ((self.c_bond.y2*100.0 + offsety) + (self.c_bond.dx * 10.0)), 
            ((self.c_bond.x2*100.0 + offsetx) + (self.c_bond.dy * 10.0)), 
            ((self.c_bond.y2*100.0 + offsety) - (self.c_bond.dx * 10.0)), 
            ((self.c_bond.x1*100.0 + offsetx) + (self.c_bond.dy * 10.0)), 
            ((self.c_bond.y1*100.0 + offsety) - (self.c_bond.dx * 10.0))
            );

class Molecule(molecule.molecule):
    def __str__(self):
        return '''%lf'%d'%d'%d"''' % (Atom(self.get_atom(1)).z, Atom(self.get_atom(2)).z, self.get_atom(2).z, self.bond_no);
    def svg(self, rad, el, grad):
        stacka = [];
        stackb = [];
        returning = "";
        #add all to the stack
        for i in range(self.bond_no-1, -1, -1):
            stackb.append(Bond(self.get_bond(i)));
        for i in range(self.atom_no-1, -1, -1):
            stacka.append(Atom(self.get_atom(i)));
        
        a1 = stacka.pop();
        b1 = stackb.pop();
        while (len(stacka) != 0) and (len(stackb) != 0):
            if a1.z < b1.z:
                returning = returning + a1.svg(rad, el);
                a1 = stacka.pop();
            else:
                returning = returning + b1.svg();
                b1 = stackb.pop();
        #b finished first - only one b left
        while(len(stacka)>0):
            if a1.z < b1.z:
                returning = returning + a1.svg(rad, el);
                a1 = stacka.pop();
            else:
                returning = returning + b1.svg();
                while(len(stacka)>0):
                    returning = returning + a1.svg(rad,el);
     
                    a1 = stacka.pop();
                returning = returning + a1.svg(rad,el);
                break;
        while(len(stackb)>0):
            if a1.z < b1.z:
                returning = returning + a1.svg(rad, el);
                while(len(stackb)>0):
                    returning = returning + b1.svg();
                    b1 = stackb.pop();
                returning = returning + b1.svg();
                break;
            else:
                returning = returning + b1.svg();
                b1 = stackb.pop();
       
        return header + grad + returning + footer;
    def parse(self, file):
        totalLines = file.readlines();
        firstLine = totalLines[3].split();
        atomCount = int(firstLine[0]);
        bondCount = int(firstLine[1]);
        for a in range(0,atomCount):
            lines = totalLines[int(a) + 4].split();
            #import pdb; pdb.set_trace();
            self.append_atom(lines[3], float(lines[0]), float(lines[1]), float(lines[2]));
            #print(float(lines[2]));
        for b in range(0,bondCount):
            lines = totalLines[int(b)+ int(atomCount) + 4].split();
            self.append_bond(int(lines[0])-1, int(lines[1])-1, int(lines[2]));

if __name__ == "__main__":
    f = open("CID_31260.sdf", "r");
   
    #MolDisplay.header += db.radial_gradients();
    mol = Molecule();
    mol.parse(f);
    mol.sort();
    mol.svg();
    print(mol.svg());