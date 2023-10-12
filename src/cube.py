import math
import time

di_width = 50
di_height = 40
fps = 60

pix = [[0 for i_ in range(di_height)] for i in range(di_width)] # di_width * di_height 2차원 배열

def dot(x, y, z) : # 점 함수
    axis_x = di_width/2
    axis_y = di_height/2

    if 0 <= round(axis_x+x) < di_width and 0 <= round(axis_y-y) < di_height :
            pix[round(axis_x+x)][round(axis_y-y)] = 1

def line(x, y, z, to_x, to_y, to_z) : # 선 함수
    axis_x = di_width/2
    axis_y = di_height/2

    dot(x, y, z)
    dot(to_x,to_y,to_z)

    if 0 <= round(axis_x+x) < di_width and 0 <= round(axis_y+y) < di_height and 0 <= round(axis_x+to_x) < di_width and 0 <= round(axis_y+to_y) < di_height :
        pix_width = abs(round(x)-round(to_x))
        pix_height = abs(round(y)-round(to_y))
        
        if abs(to_x) >= 0 : # 변수 정렬
            X = x
        else :
            X = abs(to_x) + x
        if abs(to_y) >= 0 :
            Y = -y
        else :
            Y = abs(to_y) - y

        if x == to_x and y == to_y :
            pix[round(axis_x+x)][round(axis_y+y)] = 1
        elif x != to_x and y == to_y :
            for ix in range(pix_width) :
                if to_x-x >= 0 :
                    pix[round(axis_x+X+ix)][round(axis_y+Y)] = 1
                else :
                    pix[round(axis_x+X+ix-pix_width)][round(axis_y+Y)] = 1
        elif y != to_y and x == to_x:
            for iy in range(pix_height) :
                if to_y-y < 0 :
                    pix[round(axis_x+X)][round(axis_y+Y+iy)] = 1
                else :
                    pix[round(axis_x+X)][round(axis_y+Y+iy-pix_height)] = 1
        else :
            if (to_x - x) * (to_y - y) >= 0 :
                if to_x - x >= 0 :
                    axis_y -= pix_height
                else :
                    axis_x -= pix_width
                    
                rev = 0 # 증가 방향 선
            else :
                if to_x - x < 0 :
                    axis_x -= pix_width
                    axis_y -= pix_height
                        
                rev = 1 # 감소 방향 선

            pix_acc = 0

            for iy in range(pix_height) :
                
                pix_remain = pix_width%pix_height # 나머지 픽셀
                pix_assign = pix_width//pix_height # 할당 픽셀
                
                if pix_remain != 0 :
                    for i in range(pix_remain) :
                        if round((pix_height/pix_remain)*i) == iy :
                            pix_assign += 1
                
                if pix_assign == 0 :
                    pix_assign = 1
                    pix_acc -= 1

                for ix in range(pix_assign) :
                    if rev == 1 :
                        pix[round(axis_x+X)+pix_acc+ix][round(axis_y+Y)+iy] = 1 # 감소 방향
                    else :
                        pix[round(axis_x+X)-pix_acc-ix+pix_width][round(axis_y+Y)+iy] = 1 # 증가 방향
                
                pix_acc += pix_assign

#Cube 정의
cube_size = 3
cube_pos = {"x":0,"y":0,"z":0}
cube_xrot = 30
cube_yrot = 0
cube_zrot = 0
point = [{"x":0,"y":0,"z":0} for i in range(8)] # point[1~8][x, y, z] = 0

while True :

    for i_y in range(di_height) : # pix 변수 초기화
        for i_x in range(di_width) :
            pix[i_x][i_y] = 0

    cube_xrot += 1 * (60 / fps)
    cube_yrot += 1.5 * (60 / fps)
    cube_zrot += 0.1 * (60 / fps)
    cube_size += 0.05

    for i in range(8) :
        distance = cube_size
        xrot = math.radians(cube_xrot)
        yrot = math.radians(cube_yrot + 45 + 90 * (i%4)) 
        zrot = math.radians(cube_zrot)
        x_fix = (distance/math.sqrt(2)) * math.cos(yrot)
        y_fix = (distance/math.sqrt(2)) *  math.sin(yrot) * math.sin(xrot) + (distance/2) * math.cos(xrot + math.radians(180)*(i//4))
        point[i]["x"] = cube_pos["x"] + x_fix * math.cos(-zrot) - y_fix * math.sin(-zrot)
        point[i]["y"] = cube_pos["y"] + x_fix * math.sin(-zrot) + y_fix * math.cos(-zrot)
        point[i]["z"] = cube_pos["z"] # z축 미구현

    '''for i in range(8) : # 점 함수 <-> point 동기화
        dot(point[i]["x"], point[i]["y"], point[i]["z"])'''

    for i in range(12) : # 선 함수 <-> point 동기화
        if 0 <= i < 4 :
            fp = i
            fs = (i + 1)%4
        elif 4 <= i < 8 :
            fp = i - 4
            fs = i
        else :
            fp = i - 4
            fs = (i + 1)%4 + 4

        line(point[fp]["x"], point[fp]["y"], point[fp]["z"],point[fs]["x"], point[fs]["y"], point[fs]["z"])

    disp = ""
    for i_y in range(di_height) : # 출력

        for i_x in range(di_width) :
            if pix[i_x][i_y] == 0 :
                disp += "  "
            elif pix[i_x][i_y] == 1 :
                disp += "% "
            else :
                disp += str(pix[i_x][i_y])
        disp += "\n"
    print(disp)

    time.sleep(1/fps)