# 11_score.py
# 게임 스코어 처리
# 목표 점수 (1500)
# 현재 점수 (?)
import os # 경로를 위해 os 라이브러리 불러오기
import pygame # 파이게임 라이브러리 불러오기
import math # radians를 사용하기 위해서 math 라이브러리 불러오기


# 집게 클래스 (보석 클래스와 거의 동일!)
class Claw(pygame.sprite.Sprite):
    def __init__(self, image, position):
        super().__init__()
        self.image = image # 회전한 이미지를 가질 예정!
        self.original_image = image # 처음 이미지를 그대로 가지고 있는다!
        self.rect = image.get_rect(center = position)

        self.offset = pygame.math.Vector2(default_offset_x_claw, 0) # x위치는 100만큼 이동, y위치는 그대로
        self.position = position

        self.direction = LEFT # 집게의 이동 방향 (숫자값)
        self.angle_speed = 2.5 # 1프레임당 집게의 각도 변경폭 (좌우 이동 속도)
        self.angle = 10 # 최초 각도 정의 (오른쪽 끝)
        

    def update(self, to_x): # 보통 게임을 만들 때 캐릭터가 가만히 있을 때 숨쉬는 동작을 담당하는 부분!
        if self.direction == LEFT : # 왼쪽 방향으로 이동하고 있다면
            self.angle += self.angle_speed # 이동 속도만큼 각도를 증가
        elif self.direction == RIGHT : # 오른쪽 방향으로 이동하고 있다면
            self.angle -= self.angle_speed #이동 속도만큼 각도를 감소
        
        # 만약에 허용 각도 범위를 벗어나면?
        if self.angle > 170:
            self.angle = 170
            self.set_direction(RIGHT)
        elif self.angle < 10:
            self.angle = 10
            self.set_direction(LEFT)

        self.offset.x += to_x

        self.rotate()
        # print(self.angle, self.direction) 테스트용
        # rect_center = self.position + self.offset # 위에서 만든 두 변수를 더해줌!!
        # self.rect = self.image.get_rect(center = rect_center) # update 메소드를 실행하면 self.rect가 업데이트 되고, draw를 하면 바뀐 rect를 기준으로 화면에 출력!


    def rotate(self): # 원본 이미지가 아닌 새로운 이미지를 만드는 메소드!
        self.image = pygame.transform.rotozoom(self.original_image, -self.angle, 1)
        # 기본 사진을 주어진 각도만큼 회전 (실제로는 반시계방향으로 각도가 계산되지만, 우리는 시계방향으로 거꾸로 적용하기 위해 -를 붙였다!), 이미지의 크기 변동은 X(1)
        # self.image는 회전을 하고 나서 새롭게 만들어진 이미지를 넣기 위한 변수!! (rotozoom은 이미지 회전, 크기설정을 할 수 있는 메소드!)
        # rotozoom은 회전 대상 이미지, 회전 각도, 이미지 크기(scale)을 매개변수로 받는다!

        offset_rotated = self.offset.rotate(self.angle) # Vector2를 이용해 받아온 offset 데이터를 각도에 맞춰서 회전시킨 offset을 받아온다 (40으로 설정한 것을 기억하자!)
        # print(offset_rotated) # 확인용

        self.rect = self.image.get_rect(center = self.position + offset_rotated) # 집게의 중심점 기준으로 회전하게 만들어준다!
        # print(self.rect) # 확인용
        # pygame.draw.rect(screen, RED, self.rect, 1) # rect 확인용


    def set_direction(self, direction):
        self.direction = direction # 매개변수로 받은 direction을 self.direction으로 설정

    
    def draw(self, screen):
        screen.blit(self.image, self.rect) # 스크린의 blit을 이용해 Claw 클래스로 만든 객체의 이미지와 위치 정보를 이용해 그 내용을 화면에 출력한다! 
        # pygame.draw.circle(screen, RED, self.position, 3) # screen에 빨간 점을 적겠다, 위치는 self.position, 반지름은 3으로 하겠다! - 중심점 표시
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # 직선 그리기
        # 스크린에 선을 그릴 것이고, 검은 색이고, self.position(중심점)부터 rect.center(집게의 중심점)까지 직선의 두께는 5로 연결하겠다!

    def set_init_state(self): # 각도와 이동방향을 초기화하는 메소드
        self.offset.x = default_offset_x_claw # 원위치
        self.angle = 10 # 오른쪽 끝에서 다시 실행하도록 설정
        self.direction = LEFT # 왼쪽으로 이동하도록 설정



# 보석 클래스
class Gemstone(pygame.sprite.Sprite): # pygame의 Sprite를 상속해와서 사용한다!!
    def __init__(self, image, position, price, speed): # 생성자 (사진인 image와 보석의 위치인 position을 매개변수로 받는다!)
        super().__init__() # 상속받은 Sprite의 생성자를 불러온다! (상속 받았으니 뭔지는 몰라도 초기화 해준다!)
        # 아래 2개의 변수는 Sprite 메소드를 사용하기 위해서 반드시 정의해야 함!!
        self.image = image # 캐릭터가 가진 이미지 정보 - 매개변수로 받아온다!
        self.rect = image.get_rect(center = position) # 캐릭터가 가지는 좌표, 크기 정보
        # 보석마다 위치가 달라져야 하기 때문에 받아온 이미지의 중앙이 매개변수로 받은 position에 맞춰서 rect를 가져오도록 설정한다!
        self.price = price
        self.speed = speed

    def set_position(self, position, angle): # 집게 이미지의 중심 좌표가 position
        # rect.size의 0번째 요소가 width, 1번째 요소가 height
        r = self.rect.size[0] // 2 # 동그라미 이미지를 기준으로 반지름, 정사각형이라면 한 변의 절반 (width의 절반)
        rad_angle = math.radians(angle) # 각도(세타값)
        to_x = r * math.cos(rad_angle) # 삼각형의 밑변
        to_y = r * math.sin(rad_angle) # 삼각형의 높이
        # position에서 (to_x, to_y)를 더한 값이 보석의 중심 위치가 되면 된다

        self.rect.center = (position[0] + to_x, position[1] + to_y)


def setup_gemstone(): # 보석 클래스에서 설정한 보석의 사진과 위치 정보를 gemstone_group에 넣는 함수! 작은 금은 이해를 위해 나눠서 작성했고, 큰 금부터는 한번에 작성!
    # 보석 가격과 끌어오는 속도 설정
    small_gold_price, small_gold_speed = 100, 5
    big_gold_price, big_gold_speed = 300, 2
    stone_price, stone_speed = 10, 2
    diamond_price, diamond_speed = 600, 7

    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380), small_gold_price, small_gold_speed) # 0번째 이미지를 (200, 300) 위치에 둬라
    gemstone_group.add(small_gold) # 그룹에 추가
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300,500), big_gold_price, big_gold_speed))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300,380), stone_price, stone_speed))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900,420), diamond_price, diamond_speed))


def update_score(score): # 보석의 price값을 받는다!
    global curr_score # 전역공간에 있는 curr_score를 사용한다는 것을 명시!!
    curr_score += score # 현재 점수를 더해준다!

def display_score(): # 화면에 현재 점수와 목표 점수 출력
    # render 메소드와 f함수를 이용해 출력 (global을 선언하지 않아도 전역 변수를 값만 가져다 쓸 수는 있다!)
    txt_curr_score = game_font.render(f"Curr Score : {curr_score:,}", True, BLACK) # f함수에서 :,을 통해 세 자리마다 콤마 삽입 가능!
    screen.blit(txt_curr_score, (50, 20)) # 화면 왼쪽 위 기준으로 (50, 20)에 현재 점수 출력

    txt_goal_score = game_font.render(f"Goal Score : {goal_score:,}", True, BLACK)
    screen.blit(txt_goal_score, (50, 80)) # 현재 점수의 조금 아래에 목표 점수 출력


pygame.init() # 파이게임 초기화

# 스크린 크기 지정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # 이걸 통해 게임의 창 크기를 설정
pygame.display.set_caption("Gold Miner") # 게임 제목 설정 "Gold Miner"

clock = pygame.time.Clock() # 프레임값을 조정하기 위한 clock변수 설정
game_font = pygame.font.SysFont("arialrounded", 30) # 게임 폰트 설정 (font.Font를 쓰면 파이인스톨러 사용 불가!)


# 점수 관련 변수
goal_score = 1500 # 목표 점수
curr_score = 0 # 현재 점수


# 게임 관련 변수
default_offset_x_claw = 40 # 중심점으로부터 집게까지의 기본 x 간격
to_x = 0 # x 좌표 기준으로 집게 이미지를 이동시킬 값을 저장하는 변수
caught_gemstone = None # 집게를 뻗어서 잡은 보석 정보

# 속도 변수
move_speed = 12 # 발사할 때 이동 스피드 (x 좌표 기준으로 증가되는 값)
return_speed = 20 # 아무것도 없이 돌아올 때의 이동 스피드

# 방향 변수
LEFT = -1 # 왼쪽 방향
STOP = 0 # 이동 방향이 좌우가 아닌 고정인 상태 (집게를 뻗음)
RIGHT = 1 # 오른쪽 방향



# 색깔 변수
RED = (255, 0, 0) # RGB값, 빨간색
BLACK = (0, 0, 0) # 검은색


# 배경 이미지 불러오기
current_path = os.path.dirname(__file__) # os.path.dirname을 이용해서 현재 파일의 위치(2_background.py 위치) 반환 
background = pygame.image.load(os.path.join(current_path, "background.png")) # 현재 위치의 파일이 있는 폴더의 background.png파일을 선택하게 됨!!


# 4개 보석 이미지 불러오기 (작은 금, 큰 금, 돌, 다이아몬드) - 배경을 가져오는 과정과 동일!!
gemstone_images = [
    pygame.image.load(os.path.join(current_path, "small_gold.png")), # 작은 금
    pygame.image.load(os.path.join(current_path, "big_gold.png")), # 큰 금
    pygame.image.load(os.path.join(current_path, "stone.png")), # 돌
    pygame.image.load(os.path.join(current_path, "diamond.png")) # 다이아몬드
]


# 보석 그룹
gemstone_group = pygame.sprite.Group() # 젬스톤 그룹 생성
setup_gemstone() # 게임에 원하는 만큼의 보석을 정의


# 집게 이미지 불러오기 (보석 이미지 불러오는 방식과 동일!)
claw_image = pygame.image.load(os.path.join(current_path, "claw.png"))
claw = Claw(claw_image, (screen_width // 2, 110)) # Claw 클래스를 이용해서 객체 생성!!
# 가로 위치는 화면 가로 크기 기준으로 절반, 위에서 110px에 위치


# 게임이 반복해서 수행될 수 있도록 게임 루프를 만든다!
running = True
while running: # 게임이 진행중이라면? while문을 계속해서 반복하게 된다!
    clock.tick(30) # FPS 값이 30으로 고정

    for event in pygame.event.get(): # 이벤트를 받아오고
        if event.type == pygame.QUIT: # 게임이 꺼지는 이벤트가 발생했다면
            running = False # running 변수를 False로 바꿔준다!

        if event.type == pygame.MOUSEBUTTONDOWN: # 마우스 버튼이 눌렸을 때 집게를 뻗음
            claw.set_direction(STOP) # 좌우 멈춤
            to_x = move_speed # move_speed 만큼 빠르게 쭉 뻗음


    # 화면의 양 옆과 아랫쪽 끝에 도달했을 때 다시 되돌아오도록 설정
    if claw.rect.left < 0 or claw.rect.right > screen_width or claw.rect.bottom > screen_height:
        to_x = -return_speed


    # 원위치에 오면 다시 원래대로 rotate하도록 설정
    if claw.offset.x < default_offset_x_claw:
        to_x = 0 # to_x 다시 초기화
        claw.set_init_state() # 각도와 이동 방향도 함께 초기화 하기 위해 set_init_state 메소드 실행

        if caught_gemstone: # 가져온 보석이 있다면
            update_score(caught_gemstone.price) # 점수 업데이트 처리
            gemstone_group.remove(caught_gemstone) # 그룹에서 잡힌 보석 제외
            caught_gemstone = None # 잡은 보석이 없도록 다시 None으로 초기화


    if not caught_gemstone: # 잡힌 보석이 없다면 충돌 체크
        for gemstone in gemstone_group: # 우리가 만들어준 gemstone 그룹에 있는 보석들을 하나하나 대입해서
            if claw.rect.colliderect(gemstone.rect): # 그 보석의 rect와 집게가 충돌했다면 - 직사각형 기준으로 충돌 처리
            # if pygame.sprite.collide_mask(claw, gemstone): # 투명 영역은 제외하고 실제 이미지가 존재하는 부분에 대해 충돌 처리
                caught_gemstone = gemstone # caught_gemstone은 바로 그 보석의 정보를 담게 된다!
                to_x = -gemstone.speed # 원점으로 되돌아가야 하므로 잡힌 보석의 속도에 -를 붙인 값을 이동 속도로 설정!
                break # for문 탈출해서 게임이 진행되도록 설정!


    if caught_gemstone: # 잡은 보석이 있다면
        caught_gemstone.set_position(claw.rect.center, claw.angle) # 집게의 중심 좌표 정보와 집게의 각도를 전달


    screen.blit(background, (0, 0)) # 맨 왼쪽 맨 위부터 ((0,0) 좌표부터)그림을 그려주도록 만들어준다!

    gemstone_group.draw(screen) # gemstone_group에 있는 모든 Sprite를 screen에다가 그려라!
    claw.update(to_x)
    claw.draw(screen)

    # 점수 정보를 보여줌
    display_score()

    pygame.display.update() # 설정한 배경화면 이미지를 pygame에 반영! (display에 업데이트!!)

pygame.quit() # while문을 빠져나가면 게임이 끝나도록 설정