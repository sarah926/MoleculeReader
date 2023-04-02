#include "mol.h"
#include "math.h"
//copies values in x,y, and z into atom stored at atom
void atomset( atom *atom, char element[3], double *x, double *y, double *z ){
    strcpy(atom->element,element);
    atom->x = *x;
    atom->y = *y;
    atom->z = *z;
}
//copies values from atom into x, y and z
void atomget( atom *atom, char element[3], double *x, double *y, double *z ){
    //copy into what is at the address, so use a *
    strcpy(element, atom->element);
    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}
//copy values a1, a2, and epairs into bond, not copying atom structs, only address of them
void bondset( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    bond->a1 = *a1;
    bond->a2 = *a2;
    bond->epairs = *epairs;
    bond->atoms = *atoms;
    //call compute function
    compute_coords(bond);
}
// ************change
//copy bond values into a1, a2, and epairs, not copying atom structs, only address of them
void bondget( bond *bond, unsigned short *a1, unsigned short *a2, atom **atoms, unsigned char *epairs ){
    a1 = &bond->a1;
    a2 = &bond->a2;
    epairs = &bond->epairs;
    *atoms = bond->atoms;
}
void compute_coords( bond *bond ){
    //x and y
    //printf("called");
    bond->x1 = bond->atoms[bond->a1].x;
    bond->x2 = bond->atoms[bond->a2].x;
    bond->y1 = bond->atoms[bond->a1].y;
    bond->y2 = bond->atoms[bond->a2].y;
    //compute z
    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z)/2.0;
    //compute len
    bond->len = sqrt((bond->x1 - bond->x2) * (bond->x1 - bond->x2) + (bond->y1 - bond->y2) * (bond->y1 - bond->y2));
    //dx is x unit vector
    bond->dx = (bond->x2 - bond->x1)/bond->len;
    //dy is y unit vector
    
    bond->dy = (bond->y2 - bond->y1)/bond->len;
}
//return address of malloced memory for a molecule
//sets molecule attributes to parameters and numbers to 0
molecule *molmalloc( unsigned short atom_max, unsigned short bond_max ){
    molecule * m = (molecule *)malloc(sizeof(struct molecule));
    //set atoms values in a molecule
    m->atom_max = atom_max;
    m->atom_no = 0;
    m->atoms = malloc(sizeof(struct atom) * atom_max);
    m->atom_ptrs = malloc(sizeof(struct atom*) * atom_max);
    //set bonds values in a molecule
    m->bond_max = bond_max;
    m->bond_no = 0;
    m->bonds = malloc(sizeof(struct bond) * bond_max);
    m->bond_ptrs = malloc(sizeof(struct bond*) * bond_max);
    return m;
}
//return address of malloced memory for a molecule
//sets molecule attributes to parameters using molmalloc, sets atom numbers to samea as src
molecule *molcopy( molecule *src ){
    molecule * m =  molmalloc(src->atom_max, src->bond_max);
    for(int i = 0; i < src->atom_no; i++){
        molappend_atom(m, &src->atoms[i]);
    }
    for(int j = 0; j < src->bond_no; j++){
        molappend_bond(m, &src->bonds[j]);
    }
    return m;
}
//frees memory used by a molecule
void molfree( molecule *ptr ){
    //free atom array memory
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);
    //free the struct
    free(ptr);
}
//copies first atom into atoms array in molecule and set 
//first empty pointer in atom_ptrs to same atom
void molappend_atom( molecule *molecule, atom *atom ){
    //check if no memory allocated
    if(molecule->atom_max == 0){
        //if no space, change to one
        molecule->atom_max = 1;
        //allocating memory
        //molmalloc(molecule->atom_max, molecule->bond_max);
        molecule->atoms = realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));
        for(int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }
    //check if memory at max
    else if(molecule->atom_no == molecule->atom_max){
        //need to realloc, double memory
        molecule->atom_max = molecule->atom_max * 2;
        molecule->atoms = realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));
        for(int i = 0; i < molecule->atom_no; i++){
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }
    //after memory fixed put atom in the array
    molecule->atoms[molecule->atom_no] = *atom;
    //printf("setting atom pointer to %p", &atom);
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];
    //increment atom numbers
    molecule->atom_no +=1;
}
//copies first bond into bonds array in molecule and set 
//first empty pointer in bond_ptrs to same bond
void molappend_bond( molecule *molecule, bond *bond ){
    if(molecule->bond_max == 0){
        //if no space, change to 1
        molecule->bond_max = 1;
        molecule->bonds = realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));
        for(int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    } else if(molecule->bond_no == molecule->bond_max){
        //need to realloc, double memory
        molecule->bond_max = molecule->bond_max * 2;
        molecule->bonds = realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));
        for(int i = 0; i < molecule->bond_no; i++){
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        }
    }
    //after memory fixed put bond into the array
    molecule->bonds[molecule->bond_no] = *bond;
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    //increment bond numbers
    molecule->bond_no +=1;
}
//sort atom_ptrs in order of increasing z value
//sort bond_ptrs in order of increasing average of atom z value
void molsort( molecule *molecule ){
    //use qsort for atoms
    qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(atom*), compatom);
    //use qsort for atoms
    qsort(molecule->bond_ptrs,molecule->bond_no, sizeof(bond*), bond_comp);
}
//write for use in qsort sorting atoms
int compatom(const void * a1, const void * a2){
    //return difference showing which one is bigger
    struct atom ** a1_ptr, **a2_ptr;
    a1_ptr = (struct atom **)a1;
    a2_ptr = (struct atom **)a2;
    if((*a1_ptr)->z > (*a2_ptr)->z){
        return 1;
    }
    else if((*a1_ptr)->z < (*a2_ptr)->z){
        return -1;
    }
    else{
        return 0;
    }
    //return ((*a1_ptr)->z > (*a2_ptr)->z);
}
//used in qsort for sorting bonds
int bond_comp( const void *a, const void *b ){
    struct bond ** bond1_ptr, **bond2_ptr;
    bond1_ptr = (struct bond **)a;
    bond2_ptr = (struct bond **)b;
   /* //calculate average of each atom in bond to create "z" value
    double z1 = (((*bond1_ptr)->a1)->z + ((*bond1_ptr)->a2)->z)/2;
    double z2 = (((*bond2_ptr)->a1)->z + ((*bond2_ptr)->a2)->z)/2;
    //return difference showing which one is bigger
    */
    double z1 = (*bond1_ptr)->z;
    double z2 = (*bond2_ptr)->z;
    if(z1>z2){
        return 1;
    }
    else if(z1<z2){
        return -1;
    }
    else{
        return 0;
    }
}
void xrotation( xform_matrix xform_matrix, unsigned short deg ){
    double r = rad(deg);
    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(r);
    xform_matrix[1][2] = -1 *sin(r);
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(r);
    xform_matrix[2][2] = cos(r);
}
void yrotation( xform_matrix xform_matrix, unsigned short deg ){
    double r = rad(deg);
    xform_matrix[0][0] = cos(r);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(r);
    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = -1 * sin(r);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(r);    
}
void zrotation( xform_matrix xform_matrix, unsigned short deg ){
    double r = rad(deg);
    xform_matrix[0][0] = cos(r);
    xform_matrix[0][1] = -1 * sin(r);
    xform_matrix[0][2] = 0;
    xform_matrix[1][0] = sin(r);
    xform_matrix[1][1] = cos(r);
    xform_matrix[1][2] = 0;
    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;   
}
void mol_xform( molecule *molecule, xform_matrix matrix ){
    double x1,y1,z1;
    for(int i = 0; i < molecule->atom_no; i++){
        x1 = 0;
        y1 = 0;
        z1 = 0;
        x1 = molecule->atoms[i].x * matrix[0][0] + molecule->atoms[i].y * matrix[0][1] 
        + molecule->atoms[i].z * matrix[0][2];
        y1 = molecule->atoms[i].x * matrix[1][0] + molecule->atoms[i].y * matrix[1][1] 
        + molecule->atoms[i].z * matrix[1][2];
        z1 = molecule->atoms[i].x * matrix[2][0] + molecule->atoms[i].y * matrix[2][1] 
        + molecule->atoms[i].z * matrix[2][2];
        molecule->atoms[i].x = x1;
        molecule->atoms[i].y = y1;
        molecule->atoms[i].z = z1; 
    }
    //added
    for(int i = 0; i <molecule->bond_no; i++){
       compute_coords(&molecule->bonds[i]); 
    }
    
}
double rad(unsigned short deg){
    return deg * (M_PI /180.0);
}
