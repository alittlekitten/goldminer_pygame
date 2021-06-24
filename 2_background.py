# 2_background.py
# 배경 이미지 설정
import os # 경로를 위해 os 라이브러리 불러오기
import pygame # 파이게임 라이브러리 불러오기

pygame.init() # 파이게임 초기화
# 스크린 크기 지정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # 이걸 통해 게임의 창 크기를 설정
pygame.display.set_caption("Gold Miner") # 게임 제목 설정 "Gold Miner"

clock = pygame.time.Clock() # 프레임값을 조정하기 위한 clock변수 설정


# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # os.path.dirname을 이용해서 현재 파일의 위치(2_background.py 위치) 반환 
background = pygame.image.load(os.path.join(current_path, "background.png")) # 현재 위치의 파일이 있는 폴더의 background.png파일을 선택하게 됨!!



# 게임이 반복해서 수행될 수 있도록 게임 루프를 만든다!
running = True
while running: # 게임이 진행중이라면? while문을 계속해서 반복하게 된다!
    clock.tick(30) # FPS 값이 30으로 고정

    for event in pygame.event.get(): # 이벤트를 받아오고
        if event.type == pygame.QUIT: # 게임이 꺼지는 이벤트가 발생했다면
            running = False # running 변수를 False로 바꿔준다!

    screen.blit(background, (0, 0)) # 맨 왼쪽 맨 위부터 ((0,0) 좌표부터)그림을 그려주도록 만들어준다!
    pygame.display.update() # 설정한 배경화면 이미지를 pygame에 반영! (display에 업데이트!!)

pygame.quit() # while문을 빠져나가면 게임이 끝나도록 설정