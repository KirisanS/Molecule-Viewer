/* 
Name: Kirisan Suthanthireswaran
ID: 1186029
Assignment: 1
Date: 2023/01/31
*/

#include "mol.h"



//atomset(): Sets atom to the values found in the parameters inputted
void atomset(atom * atom, char element[3], double * x, double * y, double * z)
{
    strcpy(atom->element, element);

    atom->x = *x;
    atom->y = *y;
    atom->z = *z;

}

//atomget(): Sets the pointer values to the information stored in the atom variable
void atomget(atom * atom, char element[3], double * x, double * y, double * z)
{
    strcpy(element, atom->element);

    *x = atom->x;
    *y = atom->y;
    *z = atom->z;
}

//bondset(): Set the bond variable to the parameters inputted
void bondset(bond * bond, unsigned short * a1, unsigned short * a2, atom ** atoms, unsigned char *epairs)
{
    if (bond != NULL)
    {
        bond->a1 = *a1;
        bond->a2 = *a2;
        bond->atoms = *atoms;
        bond->epairs = *epairs;
        compute_coords(bond);
    }
}

//bondget(): Sets the pointer values to the information stored in the bond variable
void bondget(bond * bond, unsigned short * a1, unsigned short * a2, atom ** atoms, unsigned char *epairs)
{
    if(bond != NULL)
    {
        *a1 = bond->a1;
        *a2 = bond->a2;
        *atoms = bond->atoms;
        *epairs = bond->epairs;
    }
}

/*molmalloc(): Allocate the neccessary memory for the molecule. Sets values to either
the respective paramters or 0 and returns a pointer to said molecule
*/
molecule * molmalloc(unsigned short atom_max, unsigned short bond_max)
{
    //Memory Allocation
    molecule * moleCule = malloc(sizeof(molecule));

    //Assigning Flat Values
    moleCule->atom_max = atom_max;
    moleCule->atom_no = 0;
    moleCule->bond_max = bond_max;
    moleCule->bond_no = 0;
    
    //Allocation of memory for Atoms
    moleCule->atoms = malloc(sizeof(atom)*atom_max);
    moleCule->atom_ptrs = malloc(sizeof(atom*)*atom_max);

    //Allocation of memory for Bonds
    moleCule->bonds = malloc(sizeof(bond)*bond_max);
    moleCule->bond_ptrs = malloc(sizeof(bond*)*bond_max);

    

    return moleCule;

}

//molcopy(): creates a molecule and copies the information found in src to the new molecule 
molecule * molcopy(molecule *src) 
{

    molecule * moleCule;

    //Calling upon molmalloc to allocate the neccessary space for the copied molecule
    moleCule = molmalloc(src->atom_max, src->bond_max);

    
    //For each atom that exists within the exisitng molecule, append to the newly formed molecule
    for(int i = 0; i < src->atom_no; i++) 
    {
        molappend_atom(moleCule, &src->atoms[i]);
    }

    //For each bond that exists within the exisitng molecule, append to the newly formed molecule
    for(int i = 0; i < src->bond_no; i++) 
    {
        molappend_bond(moleCule, &src->bonds[i]);
        moleCule->bond_ptrs[i]->atoms = moleCule->atoms;
    }

    return moleCule;

}

//molfree(): Free up all existing space that the molecule takes 
void molfree(molecule *ptr)
{
    //Freeing all existing allocations inside of the struct
    free(ptr->atoms);
    free(ptr->atom_ptrs);
    free(ptr->bonds);
    free(ptr->bond_ptrs);

    //Freeing the entire struct 
    free(ptr);
}

//molappend_atom(): Append an atom to the existing atoms found within the molecule 
void molappend_atom(molecule * molecule, atom * atom)
{

    //If the number of atoms in the molecule have reached the maximum amount, allocate new space
    if (molecule->atom_no == molecule->atom_max) 
    {
        //Incrementing by 1 if atom_max was equal to 0, otherwise double
        if (molecule->atom_max == 0)
        {
            molecule->atom_max = 1;
        } else 
        {
            molecule->atom_max = molecule->atom_max * 2;
        }

        //Reallocating Memory
        molecule->atoms = realloc(molecule->atoms, molecule->atom_max * sizeof(struct atom));
        molecule->atom_ptrs = realloc(molecule->atom_ptrs, molecule->atom_max * sizeof(struct atom*));

        //if either realloc has failed, exit the program 
        if (molecule->atoms == NULL || molecule->atom_ptrs == NULL) {
            exit(0);
        }

        //Assigning each atom pointer to point to the newly formed atoms
        for (int i = 0; i < molecule->atom_no; i++) 
        {
            molecule->atom_ptrs[i] = &molecule->atoms[i];
        }
    }

    //Adding the information from atom to the list of atoms 
    molecule->atoms[molecule->atom_no].x = atom->x;
    molecule->atoms[molecule->atom_no].y = atom->y;
    molecule->atoms[molecule->atom_no].z = atom->z;
    strcpy(molecule->atoms[molecule->atom_no].element, atom->element);

    //Setting the pointer to the new atom appended and incrementing atom_no
    molecule->atom_ptrs[molecule->atom_no] = &molecule->atoms[molecule->atom_no];


    molecule->atom_no++;

}

//molappend_bond(): Appending a new bond to the amount of bonds found in the molecule
void molappend_bond(molecule * molecule, bond * bond) 
{
    //If the number of bonds have reached the maximum amount, increase the size
    if(molecule->bond_no == molecule->bond_max)
    {
        //If bond_max = 0, set it to one. Otherwise we increase the allocated memory by double the previous amount
        if (molecule->bond_max == 0)
        {
            molecule->bond_max = 1;
        }
        else
        {
            molecule->bond_max = molecule->bond_max * 2;
        }

        //Reallocating Memory
        molecule->bonds = realloc(molecule->bonds, molecule->bond_max * sizeof(struct bond));
        molecule->bond_ptrs = realloc(molecule->bond_ptrs, molecule->bond_max * sizeof(struct bond*));

        //if either realloc has failed, exit the program 
        if (molecule->bonds == NULL || molecule->bond_ptrs == NULL) {
            exit(0);
        }

        //Assigning each bondptr to the newly appended bond
        for (int i = 0; i < molecule->bond_no; i++) 
        {
            molecule->bond_ptrs[i] = &molecule->bonds[i];
        } 
    }

    //Assigning the values to the newly appended bond
    molecule->bonds[molecule->bond_no].a1 = bond->a1;
    molecule->bonds[molecule->bond_no].a2 = bond->a2;
    molecule->bonds[molecule->bond_no].epairs = bond->epairs;
    molecule->bonds[molecule->bond_no].atoms = bond->atoms;
    compute_coords(&molecule->bonds[molecule->bond_no]);


    //Assigning the newest bond pointer to the new bond and incrementing bond_no
    molecule->bond_ptrs[molecule->bond_no] = &molecule->bonds[molecule->bond_no];
    molecule->bond_no++;
    
}

//cmpAtomFunction(): Compare Function used to help sort out the atom pointers in the molecule
int cmpAtomFunction(const void * a, const void * b) 
{
    struct atom **a_ptr, **b_ptr;

    a_ptr = (struct atom **)a;
    b_ptr = (struct atom **)b;


    //return ((*a_ptr)->z - (*b_ptr)->z);

    if ((*a_ptr)->z > (*b_ptr)->z) 
    {
        return 1;
    } else if ((*a_ptr)->z < (*b_ptr)->z)
    {
        return -1;
    } else 
    {
        return 0;
    }
}

//cmpBondFunction(): Compare Function used to help sort out the bond pointers in the molecule
int cmpBondFunction(const void * a, const void * b) 
{
    struct bond ** a_ptr, **b_ptr;

    a_ptr = (struct bond **) a;
    b_ptr = (struct bond **) b;


    if ((*a_ptr)->z > (*b_ptr)->z) {
        return 1;
    } else if ((*a_ptr)->z < (*b_ptr)->z) {
        return -1;
    } else {
        return 0;
    }


}

//molsort(): Sorting the molecules atoms and bonds based on their respective z value. 
void molsort(molecule * molecule)
{
    
    //In the event that the current molecule has no atoms or bonds 
    if (molecule->atom_max > 0) 
    {
        qsort(molecule->atom_ptrs, molecule->atom_no, sizeof(struct atom*), cmpAtomFunction);
    }
    if (molecule->bond_max > 0)
    {
        qsort(molecule->bond_ptrs, molecule->bond_no, sizeof(struct bond*), cmpBondFunction);
    }
    
}

//xrotation(): creation of the xmatrix based on value deg for x rotations
void xrotation(xform_matrix xform_matrix, unsigned short deg)
{
    //Computing the radians of the inputted degree
    double radian = deg * (PI) / 180.0;

    xform_matrix[0][0] = 1;
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = cos(radian);
    xform_matrix[1][2] = -sin(radian);

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = sin(radian);
    xform_matrix[2][2] = cos(radian);
      
}

//yrotation(): creation of the ymatrix based on value deg for y rotations
void yrotation(xform_matrix xform_matrix, unsigned short deg)
{
    //Computing the radians of the inputted degree
    double radian = deg * (PI) / 180.0;

    xform_matrix[0][0] = cos(radian);
    xform_matrix[0][1] = 0;
    xform_matrix[0][2] = sin(radian);

    xform_matrix[1][0] = 0;
    xform_matrix[1][1] = 1;
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = -sin(radian);
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = cos(radian);
}

//zrotation(): creation of the zmatrix based on value deg for z rotations
void zrotation(xform_matrix xform_matrix, unsigned short deg)
{
    //Computing the radians of the inputted degree
    double radian = deg * (PI) / 180;

    xform_matrix[0][0] = cos(radian);
    xform_matrix[0][1] = -sin(radian);
    xform_matrix[0][2] = 0;

    xform_matrix[1][0] = sin(radian);
    xform_matrix[1][1] = cos(radian);
    xform_matrix[1][2] = 0;

    xform_matrix[2][0] = 0;
    xform_matrix[2][1] = 0;
    xform_matrix[2][2] = 1;
      
}

//mol_xform(): rotation of the molecules based on the inputted matrix 
void mol_xform(molecule * molecule, xform_matrix matrix)
{
    double tempX, tempY, tempZ;
    

    //For each atom within the molecule
    for (int i = 0; i < molecule->atom_no; i++)
    {
        //Completing the matrix multipication 
        tempX = (molecule->atom_ptrs[i]->x * matrix[0][0]) + (molecule->atom_ptrs[i]->y * matrix[0][1])
        + (molecule->atom_ptrs[i]->z * matrix[0][2]);

        tempY = (molecule->atom_ptrs[i]->x * matrix[1][0]) + (molecule->atom_ptrs[i]->y * matrix[1][1])
        + (molecule->atom_ptrs[i]->z * matrix[1][2]);

        tempZ = (molecule->atom_ptrs[i]->x * matrix[2][0]) + (molecule->atom_ptrs[i]->y * matrix[2][1])
        + (molecule->atom_ptrs[i]->z * matrix[2][2]);

        molecule->atom_ptrs[i]->x = tempX;
        molecule->atom_ptrs[i]->y = tempY;
        molecule->atom_ptrs[i]->z = tempZ;


        //ASK ABOUT THIS KEKERS
        //compute_coords(&molecule->bonds[i]);
    }
    for (int i = 0; i < molecule->bond_no; i++)
    {
        compute_coords(molecule->bond_ptrs[i]);
    }
}

void compute_coords(bond * bond)
{
    bond->x1 = bond->atoms[bond->a1].x;
    bond->y1 = bond->atoms[bond->a1].y;
    //printf("\nBOND A1: %d BOND A2: %d \n\n", bond->a1, bond->a2);
    //printf("bond->x1: %f bond->y1 %f\n", bond->x1, bond->y1);

    bond->x2 = bond->atoms[bond->a2].x;
    bond->y2 = bond->atoms[bond->a2].y;
    //printf("bond->x2: %f bond->y2: %f\n", bond->x2, bond->y2);

    bond->z = (bond->atoms[bond->a1].z + bond->atoms[bond->a2].z) / 2;
    //printf("z: %f\n", bond->z);

    bond->len = sqrt((bond->x2 - bond->x1) * (bond->x2 - bond->x1) + (bond->y2 - bond->y1) * (bond->y2 - bond->y1));
    //printf("len %f\n", bond->len);
    bond->dx = (bond->x2 - bond->x1) / bond->len;
    bond->dy = (bond->y2 - bond->y1) / bond->len;

    
}



