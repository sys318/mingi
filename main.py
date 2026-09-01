import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(page_title="김탁곤드레밥 생존기", page_icon="🇨🇳", layout="centered")

# --- 상태 초기화 ---
if 'alive' not in st.session_state:
    st.session_state.alive = True
    st.session_state.stage = 'birth'
    st.session_state.death_message = ""
    st.session_state.death_title = ""
    st.session_state.last_click_time = time.time()  # 마지막으로 행동한 시간 기록

def reset_game():
    st.session_state.alive = True
    st.session_state.stage = 'birth'
    st.session_state.death_message = ""
    st.session_state.death_title = ""
    st.session_state.last_click_time = time.time()

def die(reason, title):
    st.session_state.alive = False
    st.session_state.death_message = reason
    st.session_state.death_title = title

def check_time_based_death():
    """1초당 1% 확률로 억까 사망 발생 (고민한 시간만큼 확률 누적)"""
    current_time = time.time()
    elapsed_seconds = int(current_time - st.session_state.last_click_time)
    st.session_state.last_click_time = current_time  # 시간 초기화
    
    if elapsed_seconds > 0:
        # 1초당 1% 확률 (n초가 지났을 때 죽을 확률 = 1 - (0.99^n))
        death_probability = 1.0 - (0.99 ** elapsed_seconds)
        
        if random.random() < death_probability:
            reasons = [
                ("아무것도 안해서 뒤1졌습니다!", "무소유의 최후"),
                ("그냥 뒤졌습니다!", "이유 없는 반항")
            ]
            reason, title = random.choice(reasons)
            die(reason, title)
            return True
            
    return False

def do_action(next_stage=None, fatal=False, fatal_reason="", fatal_title=""):
    """버튼 클릭 시 실행되는 범용 함수"""
    # 1. 가만히 고민한 시간 때문에 죽었는지 먼저 체크
    if check_time_based_death():
        return
        
    # 2. 다른 억까 메시지 (5% 확률)
    other_sudden_deaths = [
        ("사망 매시지가 마춤뻡을 틀려서 주것씁이다!!", "세종대왕 극대노"),
        ("방금 나타난 사망 메시지가 오타가 나서 죽었습니다!", "버그 갓겜"),
        ("놀라서 뒤1졌습니다!", "진성 개복치"),
    ]
    if not fatal and random.random() < 0.05:
        r, t = random.choice(other_sudden_deaths)
        die(r, t)
        return

    # 3. 확정 사망 선택지를 고른 경우
    if fatal:
        die(fatal_reason, fatal_title)
    # 4. 무사히 다음 스테이지로 넘어가는 경우
    elif next_stage:
        st.session_state.stage = next_stage


# --- 게임 화면 구성 ---
st.title("🇨🇳 김탁곤드레밥 생존기 🇨🇳")
st.markdown("⚠️ **주의:** 선택을 너무 오래 고민하면 아무것도 안해서 뒤집니다! (1초당 사망 확률 1% 누적)")
st.markdown("---")

if not st.session_state.alive:
    # 사망 화면
    st.error(f"## 💀 [{st.session_state.death_title}]")
    st.header(f"사인: {st.session_state.death_message}")
    st.markdown("---")
    st.button("🔄 다시 환생하기", on_click=reset_game, use_container_width=True)

else:
    # 생존 화면
    if st.session_state.stage == 'birth':
        st.subheader("응애! 생명의 탄생")
        st.write("김탁곤드레밥이 세상에 나오려 합니다. 과연 무사히 태어날 수 있을까요?")
        
        def do_birth():
            st.session_state.last_click_time = time.time()
            fate = random.randint(1, 4)
            if fate == 1:
                die("태어나서 죽었습니다!", "초광속 스피드런")
            elif fate == 2:
                die("입양당해서 죽었습니다!", "가혹한 운명")
            else:
                st.session_state.stage = 'main'
                    
        st.button("🍼 힘차게 태어나기", on_click=do_birth, use_container_width=True)

    # ==========================================
    # 메인 메뉴 (1차 선택)
    # ==========================================
    elif st.session_state.stage == 'main':
        st.success("✅ 기적적으로 숨을 쉬고 있습니다! 무엇을 할까요? (빨리 누르세요!)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.button("🍚 밥 먹으러 가기", on_click=do_action, args=('eat_start',), use_container_width=True)
            st.button("🚶 집 밖으로 외출하기", on_click=do_action, args=('out_menu',), use_container_width=True)
        with col2:
            st.button("🗣️ 대륙의 얼 표출하기", on_click=do_action, args=('chinese_menu',), use_container_width=True)
            st.button("🛏️ 방구석에서 잉여짓 하기", on_click=do_action, args=('idle_menu',), use_container_width=True)

    # ==========================================
    # 밥 먹으러 가기 (빌드업 4단계)
    # ==========================================
    elif st.session_state.stage == 'eat_start':
        st.subheader("밥을 먹기로 결심했습니다. 어디로 갈까요?")
        st.button("🔥 마라탕 골목으로 간다", on_click=do_action, args=('eat_walk',), use_container_width=True)
        st.button("🍚 든든한 백반집으로 간다", on_click=do_action, args=('eat_walk_normal',), use_container_width=True)

    elif st.session_state.stage == 'eat_walk':
        st.subheader("마라탕집으로 걷는 중입니다. 앞에 횡단보도가 초록불입니다.")
        st.button("🚶 여유롭게 건넌다", on_click=do_action, args=(None, True, "파란불에 여유롭게 걷다가 배달 오토바이에 치여서 길을 걷다가 납치를 당해서 죽었습니다!", "무법지대"), use_container_width=True)
        st.button("🏃 좌우를 살피며 전력질주한다", on_click=do_action, args=('eat_door',), use_container_width=True)

    elif st.session_state.stage == 'eat_door':
        st.subheader("마라탕집 문 앞에 도착했습니다. 문에 [당기시오]라고 적혀있습니다.")
        st.button("🚪 힘차게 당긴다", on_click=do_action, args=('eat_order',), use_container_width=True)
        st.button("🚪 상남자답게 밀고 들어간다", on_click=do_action, args=(None, True, "문을 힘차게 밀다가 유리에 머리를 박고 놀라서 뒤1졌습니다!", "진성 개복치"), use_container_width=True)
        
    elif st.session_state.stage == 'eat_order':
        st.subheader("가게에 들어왔습니다. 마라탕 맵기를 선택하세요.")
        st.button("🌶️ 0단계 (백탕)", on_click=do_action, args=(None, True, "마라탕집에서 백탕을 시켰다가 주방장에게 암살당해 죽었습니다!", "명예훼손"), use_container_width=True)
        st.button("🌶️🌶️🌶️ 4단계 (미친맛)", on_click=do_action, args=(None, True, "마라탕을 너무 맵게 먹어서 뒤1졌습니다1!!!1!", "위장관 용암지대"), use_container_width=True)

    elif st.session_state.stage == 'eat_walk_normal':
        st.subheader("백반집에 도착해 밥을 한 숟갈 떴습니다.")
        st.button("🥢 허겁지겁 입에 밀어넣는다", on_click=do_action, args=(None, True, "밥먹다가 그냥 죽었ㅅ브니다!", "식도 가출"), use_container_width=True)
        st.button("🥢 반찬 투정을 한다", on_click=do_action, args=(None, True, "반찬 투정하다가 식당 이모한테 등짝을 맞고 사1망했습니다!", "유리몸"), use_container_width=True)

    # ==========================================
    # 기존 상황들 (외출, 틱톡, 잉여짓)
    # ==========================================
    elif st.session_state.stage == 'out_menu':
        st.subheader("집 밖으로 나왔습니다.")
        st.button("🛣️ 큰 길가로 걷기", on_click=do_action, args=(None, True, "길을 걷다가 납치를 당해서 죽었습니다!", "인체의 신비"), use_container_width=True)
        st.button("👊 친구들 불러내기", on_click=do_action, args=(None, True, "친구들을 패다가 손이 너무 아파서 사1망했습니다!", "유리주먹"), use_container_width=True)

    elif st.session_state.stage == 'chinese_menu':
        st.subheader("내 안의 대륙의 핏물이 요동칩니다.")
        st.button("🇨🇳 자부심 넘치게 외치기", on_click=do_action, args=(None, True, "워 쓰 중꿔러! 하오! 하오! 하오쯔! 타 쿼 스!", "대륙의 기상"), use_container_width=True)
        st.button("🎤 요즘 유행하는 힙합 랩", on_click=do_action, args=(None, True, "탁원이 탁원이 (RED RED) 중국인 중국인 (RED RED) 워쓰어중궈러(GET IT GET IT) 죽었습니다!", "쇼미더대륙"), use_container_width=True)
        st.button("🗣️ 중국어 성조 연습하기", on_click=do_action, args=(None, True, "중국어 성조를 잘못 발음해서 죽었 쓰! 니다!", "성조 파괴자"), use_container_width=True)

    elif st.session_state.stage == 'idle_menu':
        st.subheader("방바닥에 누웠습니다.")
        st.button("🛒 타오바오 앱 쇼핑하기", on_click=do_action, args=(None, True, "택배를 뜯자마자 배터리가 폭발해서 그냥 뒤졌습니다!", "이유 없는 반항"), use_container_width=True)
