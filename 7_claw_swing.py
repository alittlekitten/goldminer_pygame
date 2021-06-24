# 7_claw_swing.py
# 집게를 좌우로 이동시키기
import os # 경로를 위해 os 라이브러리 불러오기
import pygame # 파이게임 라이브러리 불러오기


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
        

    def update(self): # 보통 게임을 만들 때 캐릭터가 가만히 있을 때 숨쉬는 동작을 담당하는 부분!
        if self.direction == LEFT : # 왼쪽 방향으로 이동하고 있다면
            self.angle += self.angle_speed # 이동 속도만큼 각도를 증가
        elif self.direction == RIGHT : # 오른쪽 방향으로 이동하고 있다면
            self.angle -= self.angle_speed #이동 속도만큼 각도를 감소
        
        # 만약에 허용 각도 범위를 벗어나면?
        if self.angle > 170:
            self.angle = 170
            self.direction = RIGHT
        elif self.angle < 10:
            self.angle = 10
            self.direction = LEFT

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
        pygame.draw.rect(screen, RED, self.rect, 1)


    
    def draw(self, screen):
        screen.blit(self.image, self.rect) # 스크린의 blit을 이용해 Claw 클래스로 만든 객체의 이미지와 위치 정보를 이용해 그 내용을 화면에 출력한다! 
        pygame.draw.circle(screen, RED, self.position, 3) # screen에 빨간 점을 적겠다, 위치는 self.position, 반지름은 3으로 하겠다! - 중심점 표시
        pygame.draw.line(screen, BLACK, self.position, self.rect.center, 5) # 직선 그리기
        # 스크린에 선을 그릴 것이고, 검은 색이고, self.position(중심점)부터 rect.center(집게의 중심점)까지 직선의 두께는 5로 연결하겠다!


# 보석 클래스
class Gemstone(pygame.sprite.Sprite): # pygame의 Sprite를 상속해와서 사용한다!!
    def __init__(self, image, position): # 생성자 (사진인 image와 보석의 위치인 position을 매개변수로 받는다!)
        super().__init__() # 상속받은 Sprite의 생성자를 불러온다! (상속 받았으니 뭔지는 몰라도 초기화 해준다!)
        # 아래 2개의 변수는 Sprite 메소드를 사용하기 위해서 반드시 정의해야 함!!
        self.image = image # 캐릭터가 가진 이미지 정보 - 매개변수로 받아온다!
        self.rect = image.get_rect(center = position) # 캐릭터가 가지는 좌표, 크기 정보
        # 보석마다 위치가 달라져야 하기 때문에 받아온 이미지의 중앙이 매개변수로 받은 position에 맞춰서 rect를 가져오도록 설정한다!


def setup_gemstone(): # 보석 클래스에서 설정한 보석의 사진과 위치 정보를 gemstone_group에 넣는 함수! 작은 금은 이해를 위해 나눠서 작성했고, 큰 금부터는 한번에 작성!
    # 작은 금
    small_gold = Gemstone(gemstone_images[0], (200, 380)) # 0번째 이미지를 (200, 300) 위치에 둬라
    gemstone_group.add(small_gold) # 그룹에 추가
    # 큰 금
    gemstone_group.add(Gemstone(gemstone_images[1], (300,500)))
    # 돌
    gemstone_group.add(Gemstone(gemstone_images[2], (300,380)))
    # 다이아몬드
    gemstone_group.add(Gemstone(gemstone_images[3], (900,420)))


pygame.init() # 파이게임 초기화
# 스크린 크기 지정
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height)) # 이걸 통해 게임의 창 크기를 설정
pygame.display.set_caption("Gold Miner") # 게임 제목 설정 "Gold Miner"

clock = pygame.time.Clock() # 프레임값을 조정하기 위한 clock변수 설정


# 게임 관련 변수
default_offset_x_claw = 40 # 중심점으로부터 집게까지의 기본 x 간격
LEFT = -1 # 왼쪽 방향
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

    screen.blit(background, (0, 0)) # 맨 왼쪽 맨 위부터 ((0,0) 좌표부터)그림을 그려주도록 만들어준다!

    gemstone_group.draw(screen) # gemstone_group에 있는 모든 Sprite를 screen에다가 그려라!
    claw.update()
    claw.draw(screen)

    pygame.display.update() # 설정한 배경화면 이미지를 pygame에 반영! (display에 업데이트!!)

pygame.quit() # while문을 빠져나가면 게임이 끝나도록 설정