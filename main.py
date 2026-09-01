import time
import random
import sys

class ChaosTak:
    def __init__(self):
        self.name = "김탁곤드레밥"
        self.alive = True

    def die(self, reason, title):
        print("\n========================================")
        print(f"💀 [{title}]")
        print(f"사인: {reason}")
        print("========================================\n")
        self.alive = False
        sys.exit() # 얄짤없이 게임 강제 종료

    def birth(self):
        print("=== [ 생명의 탄생 ] ===")
        print("응애! 김탁곤드레밥이 태어났... 어?")
        time.sleep(1)
        
        fate = random.randint(1, 3)
        if fate == 1:
            self.die("태어나서 죽었습니다!", "초광속 스피드런")
        elif fate == 2:
            self.die("입양당해서 죽었습니다!", "가혹한 운명")
        else:
            print("기적적으로 탄생의 고비를 넘겼습니다.\n")

    def random_sudden_death(self):
        # 행동과 무관하게 그냥 억울하게 죽는 풀
        sudden_deaths = [
            ("아무것도 안해서 뒤1졌습니다!", "무소유의 최후"),
            ("그냥 뒤졌습니다!", "이유 없는 반항"),
            ("사망 매시지가 마춤뻡을 틀려서 주것씁이다!!", "세종대왕 극대노"),
            ("방금 나타난 사망 메시지가 오타가 나서 죽었습니다!", "버그 갓겜"),
            ("놀라서 뒤1졌습니다!", "진성 개복치")
        ]
        if random.random() < 0.2: # 20% 확률로 행동 전에 숨짐
            reason, title = random.choice(sudden_deaths)
            self.die(reason, title)

    def action_eat(self):
        print("\n배가 고파서 밥을 먹으려 합니다.")
        print("1. 마라탕 먹기")
        print("2. 그냥 평범한 밥 먹기")
        choice = input("선택 (1/2): ")
        
        if choice == '1':
            self.die("마라탕을 너무 맵게 먹어서 뒤1졌습니다1!!!1!", "위장관 용암지대")
        else:
            self.die("밥먹다가 그냥 죽었ㅅ브니다!", "식도 가출")

    def action_walk(self):
        print("\n소화를 시킬 겸 밖으로 나왔습니다.")
        print("1. 길 걷기")
        print("2. 친구들 만나기")
        choice = input("선택 (1/2): ")
        
        if choice == '1':
            self.die("길을 걷다가 납치를 당해서 죽었습니다!", "인체의 신비")
        else:
            self.die("친구들을 패다가 손이 너무 아파서 사1망했습니다!", "유리주먹")

    def action_chinese(self):
        print("\n갑자기 내 안의 대륙의 피가 끓어오릅니다.")
        print("1. 중국어로 말하기")
        print("2. 정체불명의 랩 하기")
        choice = input("선택 (1/2): ")
        
        if choice == '1':
            if random.random() < 0.5:
                self.die("워 쓰 중꿔러! 하오! 하오! 하오쯔! 타 쿼 스!", "대륙의 기상")
            else:
                self.die("중국어 성조를 잘못 발음해서 죽었 쓰! 니다!", "성조 파괴자")
        else:
            self.die("탁원이 탁원이 (RED RED) 중국인 중국인 (RED RED) 워쓰어중궈러(GET IT GET IT) 죽었습니다!", "쇼미더대륙")

def play_game():
    print("🇨🇳 [주의] 툭하면 죽는 김탁곤드레밥 키우기 🇨🇳\n")
    
    player = ChaosTak()
    player.birth()
    
    while player.alive:
        player.random_sudden_death()
        
        print(f"[{player.name}은(는) 살아있습니다. 무엇을 할까요?]")
        print("1. 밥 먹기")
        print("2. 산책하기")
        print("3. 대륙의 얼 표출하기")
        
        choice = input("선택 (1/2/3): ")
        
        if choice == '1': player.action_eat()
        elif choice == '2': player.action_walk()
        elif choice == '3': player.action_chinese()
        else:
            player.random_sudden_death()

if __name__ == "__main__":
    play_game()
