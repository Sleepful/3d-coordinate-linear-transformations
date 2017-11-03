from tkinter import *
import numpy as np

canvas_width = 800
canvas_height = 600

PString      = ""
BString      = ""
PList        = [0.0,0.0,0.0]
BList1       = [0.0,0.0,0.0]
BList2       = [0.0,0.0,0.0]
BList3       = [0.0,0.0,0.0]
BList1_name  = ""
BList2_name  = ""
BList3_name  = ""
Screen_msg   = ""
ZRotation    = 0.0

def es_lineal_independiente():
    global BList1
    global BList2
    global BList3
    matrix = np.array(
        [
            BList1,
            BList2,
            BList3
        ])
    det =  np.linalg.det(matrix)
    if (det==0):
        return False
    return True

def print_Screenmsg():
    global w
    w.create_text(canvas_width / 2,
        30,
        fill = "red",
        font = "Helvetica 16",
        text=Screen_msg)

def string_valido():
    global Screen_msg
    global PList
    if (not es_lineal_independiente()):
        clear_screen()
        Screen_msg = "No es linealmente independiente"
        print_Screenmsg()
    else:
        print ("es linealmente independiente")
        xyz = get_coordinate_vector(PList[0],PList[1],PList[2])
        val1 = xyz[0]
        val2 = xyz[1]
        val3 = xyz[2]

        Screen_msg = (
            "Coordenadas de P en la base B: "
            "{"
            + str(val1) + ","
            + str(val2) + ","
            + str(val3) + "}"
            )
        graficar()

def graficar():
    clear_screen()
    #draw_test()
    draw_guidelines()
    draw_basis_guidelines()
    draw_P_dot()
    draw_P_dot_guidelines()
    print_Screenmsg()

def verificar_input():
    global Screen_msg
    global PString
    global BString
    if (verify_P(PString) and verify_B(BString)):
        #print (PString) #para pruebas
        #print (BString) #para pruebas
        string_valido()
    else:
        clear_screen()
        Screen_msg = "String no valido"
        print_Screenmsg()

def P_entry_callback(sv):
    global PString
    PString = sv.get()
    verificar_input()

def B_entry_callback(sv):
    global BString
    BString = sv.get()
    verificar_input()

def slider_callback(var):
    global ZRotation
    ZRotation = np.deg2rad(int(var))
    verificar_input()

def is_digit(n):
    try:
        float(n)
        return True
    except ValueError:
        return  False

def verify_P(s):
    try:
        s = s.replace(" ",'')
        if (s[0]!="(" or s[-1]!=")"):
            print("formato de parentesis incorrecto")
            raise Exception
        s     = s[1:-1]
        slist = s.split(",")
        if (len(slist)!=3):
            print("cantidad incorrecta de elementos")
            raise Exception
        for elem in slist:
            if (not is_digit(elem)):
                print("elementos no son numeros")
                raise Exception
    except Exception:
        #cambiar no valido
        print("string no valido en entrada P") 
        return False
    else:
        global PList
        for i in range(0,3):
            PList[i]=int(slist[i])
            #print(PList[i])
        #string valido
        # print("Plist{} {} {}", str(PList[0]), str(PList[1]), str(PList[2]))
        return True

def verify_B(x):
    try:
        x = x.replace(" ",'')
        blist = x.split(";")
        if (len(blist)!=3):
            print("cantidad incorrecta de elementos")
            raise Exception
        for elem in blist:
            elemlist = elem.split("=")
            if  (
                len(elemlist)!=2 or
                not elemlist[0].isalpha
                ):
                print("formato de string incorrecto")
            s = elemlist[1]

            if (s[0]!="(" or s[-1]!=")"):
                print("formato de parentesis incorrecto")
                raise Exception
            s     = s[1:-1]
            slist = s.split(",")
            if (len(slist)!=3):
                print("cantidad incorrecta de elementos")
                raise Exception
            for elem in slist:
                if (not is_digit(elem)):
                    print("elementos no son numeros")
                    raise Exception
    except Exception:
        #cambiar no valido
        print("string no valido en entrada B") 
        return False
    else:
        global BList1
        global BList2
        global BList3
        global BList1_name
        global BList2_name
        global BList3_name
        templist            = blist[0].split("=")
        BList1_name         = templist[0]
        templist[1]         = templist[1][1:-1]
        otherlist           = templist[1].split(",")
        for i in range(0,3):
            BList1[i]=float(otherlist[i])
        templist            = blist[1].split("=")
        BList2_name         = templist[0]
        templist[1]         = templist[1][1:-1]
        otherlist           = templist[1].split(",")
        for i in range(0,3):
            BList2[i]=float(otherlist[i])
        templist            = blist[2].split("=")
        BList3_name         = templist[0]
        templist[1]         = templist[1][1:-1]
        otherlist           = templist[1].split(",")
        for i in range(0,3):
            BList3[i]=float(otherlist[i])
        #string valido
        #print("blist1 " + BList1_name + " blist2-2 " + str(BList2[1]))
        return True


master = Tk()

Label(master,
    text="Rotar alrededor del eje Z",
    fg = "light green",
    font = "Helvetica 16").pack()

scal = Scale(master, from_=0, to=720, length=500, width=30,
    orient=HORIZONTAL, command=slider_callback).pack()

Label(master,
    text="P=",
    fg = "light green",
    font = "Helvetica 16").pack()

svP = StringVar()
svP.trace("w", lambda name, index, mode,
    svP=svP: P_entry_callback(svP))
entryP = Entry(master,
    fg = "light blue",
    font = "Helvetica 16",
    textvariable=svP
    ).pack()

Label(master,
    text="Base B=",
    fg = "light green",
    font = "Helvetica 16").pack()

svB = StringVar()
svB.trace("w", lambda name, index, mode,
    svB=svB: B_entry_callback(svB))
entryB = Entry(master,
    fg = "light blue",
    font = "Helvetica 16",
    width=30,
    textvariable=svB
    ).pack()

def get_coordinate_vector(x,y,z):
    #basis is B
    basis = np.array([
                [BList1[0],BList2[0],BList3[0]],
                [BList1[1],BList2[1],BList3[1]],
                [BList1[2],BList2[2],BList3[2]]
            ])
    vector = np.array([x,y,z])
    coordinate_vector = np.linalg.solve(
                                       basis,
                                       vector
                                       )
    return coordinate_vector;



def rotate_transformation(x,y,z):
    ZRotation_Matrix = np.array(
        [
        [np.cos(ZRotation), -(np.sin(ZRotation)),  0],
        [np.sin(ZRotation), np.cos(ZRotation),     0],
        [0,                 0,                     1]
        ])
    return linear_transformation(ZRotation_Matrix,x,y,z)

def linear_transformation(sq_matrix,x,y,z):
    line_matrix = np.array(
        [x,y,z]
        )
    return sq_matrix.dot(line_matrix)

#adjust x
def _x(x):
    return (x+canvas_width/2)

#adjust y
def _y(y):
    return (-y+canvas_height/2)

#isometrica con rotacion
def isor_x(x,y,z):
    xyz = rotate_transformation(x,y,z)
    return iso_x(xyz[0],xyz[1],xyz[2])

#isometrica con rotacion
def isor_y(x,y,z):
    xyz = rotate_transformation(x,y,z)
    return iso_y(xyz[0],xyz[1],xyz[2])

#isometrica
def iso_x(x,y,z):
    return y-x

#isometrica
def iso_y(x,y,z):
    return (-1/2)*(x+y-(2*z))

def create_dot_3D(x,y,z,color):
    create_dot(
        isor_x(x,y,z),
        isor_y(x,y,z),
        color
        )
def create_dotline_3D(
    x_base,y_base,z_base,x_tip,y_tip,z_tip,color):
    create_dotline(
        isor_x(x_base,y_base,z_base),
        isor_y(x_base,y_base,z_base),
        isor_x(x_tip,y_tip,z_tip),
        isor_y(x_tip,y_tip,z_tip),
        color
        )

def name_arrow_3D(
    x_base,y_base,z_base,x_tip,y_tip,z_tip,color,name):
    name_arrow(
        isor_x(x_base,y_base,z_base),
        isor_y(x_base,y_base,z_base),
        isor_x(x_tip,y_tip,z_tip),
        isor_y(x_tip,y_tip,z_tip),
        color,
        name
        )
def create_arrow_3D(
    x_base,y_base,z_base,x_tip,y_tip,z_tip,color):
    create_arrow(
        isor_x(x_base,y_base,z_base),
        isor_y(x_base,y_base,z_base),
        isor_x(x_tip,y_tip,z_tip),
        isor_y(x_tip,y_tip,z_tip),
        color
        )

def create_dot(x,y,color):
    w.create_oval(
        _x(x-1),
        _y(y-1),
        _x(x+1),
        _y(y+1),
        fill  = color,
        width = 5,
        outline = color)

def create_dotline(x_base,y_base,x_tip,y_tip,color):
    linewidth = 2,
    w.create_line(
        _x(x_base),
        _y(y_base),
        _x(x_tip),
        _y(y_tip),
        fill=color,
        dash=(4,4),
        width=linewidth)

def name_arrow(x_base,y_base,x_tip,y_tip,color,name):
    new_x = (x_base + x_tip)/2
    new_y = (y_base + y_tip)/2
    w.create_text(
        _x(new_x),
        _y(new_y),
        fill = color,
        font = "Helvetica 10",
        text=name)

def create_arrow(x_base,y_base,x_tip,y_tip,color):
    linewidth = 2
    tiplength = 14
    w.create_line(
        _x(x_base),
        _y(y_base),
        _x(x_tip),
        _y(y_tip),
        arrow=LAST,
        fill=color, width=linewidth)

w = Canvas(
          master,
          width=canvas_width,
          height=canvas_height,
          bg="black"
          )

def clear_screen():
    w.delete("all")

def draw_test():
    create_arrow_3D(50,50,0,0,200,200,"light blue")
    create_arrow_3D(50,50,0,0,100,100,"orange")
    create_arrow_3D(50,50,0,0,-70,-70,"light green")

    create_arrow_3D(0,0,0,100,0,0,"grey")
    create_arrow_3D(0,0,0,0,100,0,"grey")
    create_arrow_3D(0,0,0,0,0,100,"grey")

    name_arrow_3D(50,50,0,0,100,100,"white","help")
    create_dot_3D(0,0,0,"red")
    create_dot_3D(0,10,0,"green")
    create_dotline_3D(-50,-50,0,0,-100,-100,"light green")

def draw_basis_guidelines():
    global BList1_name
    global BList2_name
    global BList3_name
    length = 200
    xyz1 = get_coordinate_vector(length,0,0)
    xyz2 = get_coordinate_vector(0,length,0)
    xyz3 = get_coordinate_vector(0,0,length)
    create_arrow_3D(0,0,0,xyz1[0],xyz1[1],xyz1[2],"orange")
    name_arrow_3D(0,0,0,xyz1[0],xyz1[1],xyz1[2],"white",BList1_name)
    create_arrow_3D(0,0,0,xyz2[0],xyz2[1],xyz2[2],"orange")
    name_arrow_3D(0,0,0,xyz2[0],xyz2[1],xyz2[2],"white",BList2_name)
    create_arrow_3D(0,0,0,xyz3[0],xyz3[1],xyz3[2],"orange")
    name_arrow_3D(0,0,0,xyz3[0],xyz3[1],xyz3[2],"white",BList3_name)

def draw_P_dot():
    xyz1 = get_coordinate_vector(PList[0],PList[1],PList[2])
    create_dot_3D(xyz1[0],xyz1[1],xyz1[2],"red")

def draw_P_dot_guidelines():
    global BList1_name
    global BList2_name
    global BList3_name

    xyza = get_coordinate_vector(0,PList[1],PList[2])
    xyzb = get_coordinate_vector(PList[0],0,PList[2])
    xyzc = get_coordinate_vector(PList[0],PList[1],0)

    xyzd = get_coordinate_vector(PList[0],PList[1],PList[2])

    xyz1 = get_coordinate_vector(0,0,PList[2])
    xyz2 = get_coordinate_vector(PList[0],0,0)
    xyz3 = get_coordinate_vector(0,PList[1],0)
    create_dotline_3D (
        xyz3[0],xyz3[1],xyz3[2],
        xyzc[0],xyzc[1],xyzc[2],
        "light green"
        )
    create_dotline_3D (
        xyz2[0],xyz2[1],xyz2[2],
        xyzc[0],xyzc[1],xyzc[2],
        "light green"
        )
    create_dotline_3D (
        xyzc[0],xyzc[1],xyzc[2],
        xyzd[0],xyzd[1],xyzd[2],
        "light green"
        )


def draw_guidelines():
    create_arrow_3D(0,0,0,250,0,0,"grey")
    create_arrow_3D(0,0,0,0,250,0,"grey")
    create_arrow_3D(0,0,0,0,0,250,"grey")

#draw_test()


w.pack()


mainloop()
