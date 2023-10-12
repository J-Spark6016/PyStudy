import pygame
import sys
import time
import random

# 시작
pygame.init()

# 창 설정
width = 640
height = 480
screen = pygame.display.set_mode((width, height)) # 해상도
pygame.display.set_caption("Shell Game")

# 색
c_black = 0, 0, 0
c_white = 255, 255, 255
c_gray = 100, 100, 100
c_ltgray = 200, 200, 200

# 폰트
font10 = pygame.font.Font('consola.ttf', 10)
font18 = pygame.font.Font('consola.ttf', 18)
font36 = pygame.font.Font('consola.ttf', 36)
font72 = pygame.font.Font('consola.ttf', 72)

# 이미지
img_cup = pygame.image.load("cup.png")
img_ball = pygame.image.load("ball.png")

#변수
fps = 60
game_stat = 0 # 0 : 메인, 1 : 게임화면

#변수 - 인게임
game_step = 0
cup_xpos = [150 * (i-1) for i in range(3)]
cup_ypos = [-150 - height//2 for i in range(3)]
answer = 1
player_choice = 0
an = [0 for i in range(1)] # 애니메이션 함수
an_step = [0 for i in range(1)] # 애니메이션 단계 함수
random_a, random_b = [0 for i in range(100)], [0 for i in range(100)] # 랜덤하게 선택되는 수
level = 80

#함수
def var_reset() :
    global game_step, cup_xpos, cup_ypos, answer, player_choice, an, an_step, random_a, random_b, level
    game_step = 0 # 0 : 시작, 1 : 섞는중, 2 : 고르기
    cup_xpos = [150 * (i-1) for i in range(3)]
    cup_ypos = [-150 - height//2 for i in range(3)]
    answer = 1
    player_choice = 0
    an = [0 for i in range(1)] # 애니메이션 함수
    an_step = [0 for i in range(1)] # 애니메이션 단계 함수
    random_a, random_b = [0 for i in range(100)], [0 for i in range(100)] # 랜덤하게 선택되는 수
    level = 1

def draw_text(x,y,text, font=font18, color = c_black,mode=0) : # 텍스트 렌더링
    text_render = font.render(text, True, color)  # 텍스트 렌더링
    text_rect = text_render.get_rect()
    if mode == 0 :
        text_rect.center = (x, y)  # 위치
    screen.blit(text_render, text_rect)  # 화면에 표시

def draw_UI_button1(x, y, text) :
    text_w = 150
    text_h = 50
    if  (-text_w//2 < x - mouse_x <= text_w//2) and (-text_h//2 < y - mouse_y <= text_h//2) :
        draw_text(x, y, text, font36, c_ltgray)
        if mouse_buttons[0] == True : # 마우스 왼쪽 버튼 클릭
            return True
        else :
            return False
    else :
        draw_text(x, y, text, font36, c_gray)
        return False

def draw_UI_button2(x, y) :
    text_w = 150
    text_h = 150
    if  (-text_w//2 < x - mouse_x <= text_w//2) and (-text_h//2 < y - mouse_y <= text_h//2) :
        draw_text(x, y, 'Click', font18, c_white)
        if mouse_buttons[0] == True : # 마우스 왼쪽 버튼 클릭
            return True
        else :
            return False
    else :
        return False

def draw_ball() :
    if game_step != 1 :
        draw_image(img_ball,150 * (answer-1)+width//2,height//5*3+43,23,23,0)

def draw_image(image, x, y, xscale, yscale, angle) :
    img = image
    real_img = pygame.transform.scale(pygame.transform.rotate(img, angle),(xscale,yscale))
    img_rect = real_img.get_rect()
    img_rect.center = (x, y)
    screen.blit(real_img, img_rect)

def draw_cups() :
    anchor_x, anchor_y = width//2, height//5*3
    for i in range(3) :
        draw_image(img_cup, anchor_x + cup_xpos[i], anchor_y + cup_ypos[i], 170, 170, 180)

def animation_end(i=0) :
    an_step[i] = 0
    an[i] = 0

def RandomlyChoice() : 
    choice = [0, 1, 2]
    a = random.choice(choice)
    choice.remove(a)
    b = random.choice(choice)
    return a, b

def bezier(_value,to_value,to_an,_point=1,i=0) :
    if an[i] <= 0 :
        result = _value
    elif an[i] >= to_an :
        result = to_value
    else :
        u = an[i]/to_an
        bezier_point = _value + (to_value - _value)*_point
        result = _value*(1-u)*(1-u) + bezier_point*2*u*(1-u) +to_value*u*u

    return result

def shuffle(an_process, frame, cup_1, cup_2) :
    global answer
    if abs(cup_1 - cup_2) >= 2 :
        frame = round(frame*1.3)
    if animation_process(an_process, frame) :
        cup_xpos[cup_1] = bezier(150 * (cup_1-1),150 * (cup_2-1),frame,0.7)
        cup_xpos[cup_2] = bezier(150 * (cup_2-1),150 * (cup_1-1),frame,0.7)
        if an[0] == 1 :
            if answer == cup_1 :
                answer = cup_2
            elif answer == cup_2 :
                answer = cup_1

def animation_process(Step ,Duration=1, i=0) :
    if an_step[i] == Step :
        if an[i] < Duration :
            an[i] += 1
            return True
        else :
            for i_ in range(3) :
                cup_xpos[i_] = 150 * (i_-1)
            an[i] = 0
            an_step[i] += 1
            return False
    else :
        return False

def game_management() :
    global game_step, game_stat, player_choice, level

    if game_step == 0 : # 인트로
        if animation_process(0, 15) :
            cup_ypos[0] = bezier(-150 - height//2,0,15,0)
        elif animation_process(1, 15) :
            cup_ypos[1] = bezier(-150 - height//2,0,15,0)
        elif animation_process(2, 15) :
            cup_ypos[2] = bezier(-150 - height//2,0,15,0)
        elif animation_process(3, 45) :
            draw_text(width//2,height//3+bezier(10,0,15),'Ready!',font36)
        elif animation_process(4, 30) :
            draw_text(width//2,height//3+bezier(10,0,15),'1',font36)
        elif animation_process(5, 30) :
            draw_text(width//2,height//3+bezier(10,0,15),'2',font36)
        elif animation_process(6, 30) :
            draw_text(width//2,height//3+bezier(10,0,15),'3',font36)
        elif animation_process(7) :
            animation_end()
            for i in range(100) :
                random_a[i],random_b[i] = RandomlyChoice()
            game_step = 1
    elif game_step == 1 : # 셔플
        count = min(100,(level//5)*3+5)
        frame = max(30 - (level//5),5)
        for i in range(count) :
            shuffle(i,frame,random_a[i],random_b[i])
        if animation_process(count) :
            animation_end()
            for i in range(100) :
                random_a[i],random_b[i] = RandomlyChoice()
            game_step = 2
    elif game_step == 2 : # 선택
        if animation_process(0, 600) :
            draw_text(width//2,height//3+bezier(10,0,15),'Choose!',font36)
            pygame.draw.rect(screen, c_ltgray, (width//2 - 150*(1 - an[0]/(600)),height//6*5, 300*(1 - an[0]/(600)), 5*bezier(0,1,20)))
            for i_ in range(3) :
                if draw_UI_button2(150 * (i_-1)+width//2,height//5*3) :
                    player_choice = i_
                    animation_end()
                    if player_choice == answer :
                        game_step = 3
                    else :
                        game_step = 4
        elif animation_process(1) :
            animation_end()
            game_step = 5
    elif game_step == 3 : # 성공
        if animation_process(0, 15) :
            cup_ypos[answer] = bezier(0,-60,15,1)
        elif animation_process(1, 60) :
            draw_text(width//2,height//5+bezier(10,0,15),'Success!',font36)
        elif animation_process(2, 15) :
            cup_ypos[answer] = bezier(-60,0,15,0)
        elif animation_process(3) :
            animation_end()
            level += 1
            game_step = 1
    elif game_step == 4 : # 실패
        if animation_process(0, 15) :
            cup_ypos[player_choice] = bezier(0,-60,15,1)
        animation_process(1, 60)
        if animation_process(2, 15) :
            cup_ypos[player_choice] = bezier(-60,-60,15,1)
            cup_ypos[answer] = bezier(0,-60,15,1)
        elif animation_process(3, 60) :
            draw_text(width//2,height//5+bezier(10,0,15),'Miss...',font36)
        elif animation_process(4) :
            animation_end()
            var_reset()
            game_stat = 0
    elif game_step == 5 : # 실패 - 타임아웃
        if animation_process(0, 15) :
            cup_ypos[answer] = bezier(0,-60,15,1)
        elif animation_process(1, 120) :
            draw_text(width//2,height//5+bezier(10,0,15),'Time Out!',font36)
        elif animation_process(2) :
            animation_end()
            var_reset()
            game_stat = 0
    

# 게임 루프
while True:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # 변수
    mouse_buttons = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # 화면 채우기
    screen.fill(c_white)

    if game_stat == 0 : # 메인화면
        draw_text(width//2,height//4 + 5,'Shell Game', font72, c_ltgray) # 로고 그림자
        draw_text(width//2,height//4,'Shell Game', font72) # 로고
        draw_text(width//2,height//8*7,'Computational Thinking A4 Team | Developed By Junseo Park', font10, c_gray) # 정보
        if draw_UI_button1(width//2,height//3*2, '> Start!') :
            game_stat = 1
    
    elif game_stat == 1 : # 게임 화면
        draw_ball()
        draw_cups()
        game_management()
        draw_text(width//2,height//8,"Level "+str(level), font18, c_gray) # 레벨



    # 화면 업데이트
    pygame.display.flip()
    time.sleep(1/fps)