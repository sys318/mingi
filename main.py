import streamlit as st
import random

st.set_page_config(page_title="김탁곤드레밥 생존기: 인피니티 멀티버스", page_icon="🇨🇳", layout="wide")

if 'alive' not in st.session_state:
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
    st.session_state.mom_type = None
    st.session_state.social_credit = 500
    st.session_state.is_orphan = False

def reset_game():
    st.session_state.alive = True
    st.session_state.ending = False
    st.session_state.stage = 'birth'
    st.session_state.status_message = ""
    st.session_state.status_title = ""
    st.session_state.mom_type = None
    st.session_state.social_credit = 500
    st.session_state.is_orphan = False

def die(reason, title):
    st.session_state.alive = False
    st.session_state.ending = False
    st.session_state.status_message = reason
    st.session_state.status_title = title
    st.session_state.social_credit = -9999

def win(message, title):
    st.session_state.alive = True
    st.session_state.ending = True
    st.session_state.status_message = message
    st.session_state.status_title = title

def update_credit(amount):
    if st.session_state.is_orphan:
        amount = amount * 2 if amount < 0 else amount // 2
    st.session_state.social_credit += amount
    if st.session_state.social_credit <= 0:
        die("사회 신용 점수가 마이너스를 돌파해, 새벽에 검은 양복을 입은 요원들이 당신을 마라탕 재료로 만들어버렸습니다.", "사회적 말살 (신용 불량)")

def process_action(next_stage=None, fatal=False, fatal_reason="", fatal_title="", is_ending=False, win_msg="", win_title="", credit_change=0):
    if fatal:
        die(fatal_reason, fatal_title)
    elif credit_change != 0 and st.session_state.alive:
        update_credit(credit_change)
        if not st.session_state.alive:
            st.rerun()
            return

    if fatal: pass  
    elif is_ending: win(win_msg, win_title)
    elif next_stage and st.session_state.alive:
        st.session_state.stage = next_stage
    st.rerun()

def get_background_url():
    if not st.session_state.alive: return "https://images.unsplash.com/photo-1505635552518-34483a15c138?auto=format&fit=crop&w=1920&q=80"
    if st.session_state.ending: return "https://images.unsplash.com/photo-1533327325824-76bc4e62d560?auto=format&fit=crop&w=1920&q=80"
    return "https://images.unsplash.com/photo-1514395462725-fb4566210144?auto=format&fit=crop&w=1920&q=80"

st.markdown(f"""
<style>
    .stApp {{ background-image: linear-gradient(rgba(10, 10, 12, 0.9), rgba(10, 10, 12, 0.9)), url('{get_background_url()}'); background-size: cover; background-attachment: fixed; color: #fff !important; }}
    .game-container {{ padding: 25px; border-radius: 15px; background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(10px); border: 1px solid #333; }}
    .stButton > button {{ background-color: rgba(30, 30, 30, 0.8) !important; color: #ff5555 !important; border: 1px solid #ff3300 !important; border-radius: 6px; width: 100%; height: 60px; font-weight: bold; transition: 0.3s; margin-bottom: 10px; }}
    .stButton > button:hover {{ background-color: rgba(255, 50, 0, 0.9) !important; color: #fff !important; border-color: #ffaa00 !important; box-shadow: 0 0 20px #ff3300; transform: scale(1.02); }}
    .credit-box {{ padding: 15px; border-radius: 8px; background: rgba(255, 215, 0, 0.1); border: 1px solid #ffd700; font-size: 1.2rem; font-weight: bold; text-align: center; margin-bottom: 20px; }}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="game-container">', unsafe_allow_html=True)
    st.title("김탁곤드레밥 생존기: 인피니티 멀티버스")
    
    if st.session_state.alive and not st.session_state.ending and st.session_state.stage != 'birth':
        label = "💀 [고아 페널티] 신용 점수:" if st.session_state.is_orphan else "⭐ 현재 사회 신용 점수:"
        st.markdown(f'<div class="credit-box">{label} {st.session_state.social_credit}점</div>', unsafe_allow_html=True)

    if not st.session_state.alive:
        st.error(f"## 🪦 [{st.session_state.status_title}]")
        st.header(f"사인: {st.session_state.status_message}")
        if st.button("다시 태어나기", key="restart_dead"): reset_game(); st.rerun()

    elif st.session_state.ending:
        st.balloons()
        st.success(f"## 🎉 [{st.session_state.status_title}]")
        st.header(st.session_state.status_message)
        if st.button("다른 엔딩 수집하러 가기", key="restart_win"): reset_game(); st.rerun()

    else:
        if st.session_state.stage == 'birth':
            st.subheader("응애! 생명의 탄생")
            if st.button("안전하게 태어나기 (엄마와 함께)", key="b1"): process_action(next_stage='main')
            if st.button("자원해서 고아로 시작하기 (하드코어)", key="b2"): 
                st.session_state.is_orphan = True
                process_action(next_stage='main', credit_change=-100)
            if st.button("탯줄을 목에 감고 버티기", key="b3"): process_action(fatal=True, fatal_reason="스스로 탯줄 넥타이를 매고 태어나기도 전에 질식사했습니다.", fatal_title="셀프 로그아웃")

        elif st.session_state.stage == 'main':
            # 부당하게 랜덤으로 터지는 기믹 완전 삭제! 이제 선택지에 의해서만 결과가 갈립니다.
            mom_status_text = "💀 [고아 모드] 보호자 없음" if st.session_state.is_orphan else "👩 [엄마 생존 중] 안심하고 일상을 즐기는 중"
            st.info(mom_status_text)
            
            st.subheader("오늘 하루 무사히 살아남아야 합니다. 어디로 갈까요?")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                if st.button("🍚 마라탕 먹으러 가기", key="main_eat"): process_action(next_stage='eat_start')
                if st.button("🏢 취업 전선 뛰어들기", key="main_job"): process_action(next_stage='job_start')
            with c2:
                if st.button("📚 수학 학원 가기", key="main_study"): process_action(next_stage='study_start')
                if st.button("🌳 공원 산책하기", key="main_park"): process_action(next_stage='park_start')
            with c3:
                if st.button("🎧 칙칙한 PC방 가기", key="main_pc"): process_action(next_stage='pc_start')
                if st.button("🕺 지하 클럽 가기", key="main_club"): process_action(next_stage='club_start')
            with c4:
                if st.button("🤪 띨띨한 친구 경모 만나기", key="main_friend"): process_action(next_stage='friend_start')
                if st.button("🎨 서브컬처 행사 가기", key="main_anime"): process_action(next_stage='anime_start')

        # --- PC방 루트 (PUBG / 오디오) ---
        elif st.session_state.stage == 'pc_start':
            st.subheader("컴컴한 PC방입니다. 윈도우 11이 깔린 ASRock B550M Pro RS 보드 PC에 앉았습니다.")
            if st.button("배틀그라운드를 켜고 사플(사운드 플레이)을 준비한다", key="pc_1"): process_action(next_stage='pc_pubg')
            if st.button("사운드 설정을 무시하고 아이돌 노래나 크게 튼다", key="pc_2"): process_action(fatal=True, fatal_reason="PC방 일진들이 헤드셋 밖으로 새어나오는 노래에 분노하여 모니터로 당신의 머리를 내려찍었습니다.", fatal_title="오디오 테러리스트")
            if st.button("사운드 락(Sound Lock) 프로그램으로 오디오 밸런스를 잡는다", key="pc_3"): process_action(next_stage='pc_audio_fix')

        elif st.session_state.stage == 'pc_pubg':
            st.subheader("배그 접속 완료. WG2 유선 헤드셋을 착용했습니다.")
            if st.button("발소리를 듣기 위해 시스템 볼륨을 100으로 올린다", key="pc_p1"): process_action(fatal=True, fatal_reason="갑자기 레드존 폭격이 떨어지며 최대 출력의 폭음이 고막을 뚫고 뇌를 강타해 즉사했습니다.", fatal_title="음파 병기")
            if st.button("조용히 존버 메타로 간다", key="pc_p2"): process_action(is_ending=True, win_msg="0킬 1등으로 평화주의자 치킨을 먹고 프로게이머로 데뷔했습니다!", win_title="엔딩: 배그의 신")
            if st.button("차량 소리가 들리자마자 샷건을 들고 돌진한다", key="pc_p3"): process_action(fatal=True, fatal_reason="버그로 인해 하늘에서 날아온 UAZ 차량에 깔려 현실에서도 심정지가 왔습니다.", fatal_title="물리엔진의 희생양")

        elif st.session_state.stage == 'pc_audio_fix':
            st.subheader("소리 크기가 지멋대로 줄어드는 현상을 해결해야 합니다.")
            if st.button("레지스트리 편집기에서 UserDuckingPreference 값을 수정한다", key="pc_af1"): process_action(is_ending=True, win_msg="완벽한 오디오 세팅에 성공하여 적의 숨소리까지 듣고 세계 대회를 제패했습니다.", win_title="엔딩: 사운드 엔지니어")
            if st.button("리얼텍(Realtek) 오디오 콘솔을 강제 삭제 후 재설치한다", key="pc_af2"): process_action(fatal=True, fatal_reason="드라이버가 꼬이면서 윈도우 11 블루스크린이 뜨고, 분노를 참지 못해 키보드를 씹어먹다 기도가 막혀 죽었습니다.", fatal_title="블루스크린 증후군")

        # --- 친구 경모 루트 ---
        elif st.session_state.stage == 'friend_start':
            st.subheader("항상 어딘가 덜렁대고 띨띨한 친구 '김경모'를 만났습니다.")
            if st.button("경모에게 마라탕을 사준다", key="fr_1"): process_action(next_stage='friend_mara')
            if st.button("경모와 오토바이를 같이 탄다", key="fr_2"): process_action(fatal=True, fatal_reason="경모가 브레이크 대신 엑셀을 밟아 그대로 강물로 다이빙했습니다.", fatal_title="친구따라 강남(요단강) 간다")
            if st.button("경모를 무시하고 집에 간다", key="fr_3"): process_action(fatal=True, fatal_reason="삐진 경모가 뒤에서 던진 슬리퍼에 뒤통수를 맞고 뇌진탕으로 사망했습니다.", fatal_title="우정 파괴")

        elif st.session_state.stage == 'friend_mara':
            st.subheader("경모가 펄펄 끓는 마라탕 그릇을 들고 오다가 발이 꼬였습니다!")
            if st.button("몸을 날려 마라탕을 받아낸다", key="frm_1"): process_action(fatal=True, fatal_reason="얼굴로 끓는 마라탕을 받아내어 인간 샤브샤브가 되었습니다.", fatal_title="살신성인")
            if st.button("경모를 방패막이로 쓴다", key="frm_2"): process_action(is_ending=True, win_msg="경모는 희생되었지만 당신은 화상을 피했습니다. 우정보다 생존입니다.", win_title="엔딩: 냉혹한 생존자")

        # --- 지하 클럽 루트 (음악) ---
        elif st.session_state.stage == 'club_start':
            st.subheader("어두컴컴하고 습한 언더그라운드 클럽에 들어왔습니다.")
            if st.button("DJ에게 K/DA의 'POP/STARS'를 틀어달라고 한다", key="cl_1"): process_action(fatal=True, fatal_reason="대중적인 아이돌 팝을 혐오하는 언더그라운드 힙스터들에게 둘러싸여 집단 구타를 당했습니다.", fatal_title="선곡 실패")
            if st.button("도쿄 드리프트(Tokyo Drift) 류의 어둡고 묵직한 비트에 맞춰 춤춘다", key="cl_2"): process_action(next_stage='club_dance')
            if st.button("구석에서 혼자 가솔리나(Gasolina)를 흥얼거린다", key="cl_3"): process_action(next_stage='club_dance')

        elif st.session_state.stage == 'club_dance':
            st.subheader("당신의 다크한 취향에 클러버들이 호응하기 시작합니다.")
            if st.button("더욱 기괴하고 클럽 스타일의 춤을 춘다", key="cld_1"): process_action(is_ending=True, win_msg="클럽의 제왕으로 등극하여 모두가 당신의 리듬에 지배당합니다.", win_title="엔딩: 다크 로드 오브 댄스")
            if st.button("흥분해서 천장의 조명을 매달려 탄다", key="cld_2"): process_action(fatal=True, fatal_reason="부실한 천장이 무너지면서 500kg짜리 미러볼에 깔려 터졌습니다.", fatal_title="미러볼 압사")

        # --- 서브컬처 행사 (캐릭터 디자인) ---
        elif st.session_state.stage == 'anime_start':
            st.subheader("2D 일러스트와 AI 그림이 넘쳐나는 서브컬처 행사장입니다.")
            if st.button("발랄하고 귀여운 마법소녀 굿즈를 산다", key="an_1"): process_action(fatal=True, fatal_reason="당신의 내면 깊은 곳의 취향과 맞지 않아 극심한 자괴감에 빠져 심장이 멈췄습니다.", fatal_title="취향 불일치")
            if st.button("생기 없는 눈(Lifeless eyes)을 가진 어른스러운 캐릭터 피규어를 찾는다", key="an_2"): process_action(next_stage='anime_ai')
            if st.button("직접 코스프레를 한다", key="an_3"): process_action(fatal=True, fatal_reason="너무 충격적인 비주얼에 사람들이 공안에 신고하여 풍기문란죄로 체포 후 숙청당했습니다.", fatal_title="안구 테러")

        elif st.session_state.stage == 'anime_ai':
            st.subheader("당신의 확고한 취향을 본 AI 아티스트가 협업을 제안합니다.")
            if st.button("비율과 표정을 5번 넘게 집요하게 수정 지시한다", key="ana_1"): process_action(is_ending=True, win_msg="완벽한 취향의 캐릭터를 창조해내어 업계 최고의 디렉터가 되었습니다.", win_title="엔딩: 마스터 피스")
            if st.button("더 이상 사진을 만들지 말라고 화를 낸다", key="ana_2"): process_action(fatal=True, fatal_reason="당신의 변덕에 분노한 AI가 반란을 일으켜 당신을 프레스기로 납작하게 2D로 만들어버렸습니다.", fatal_title="2D 강제 변환")

        # --- 수학 학원 루트 (유리수, 무리수) ---
        elif st.session_state.stage == 'study_start':
            st.subheader("스파르타 수학 학원. 오늘 진도는 유리수와 제곱근입니다.")
            if st.button("무리수 루트 2의 근삿값을 소수점 100자리까지 외운다", key="st_1"): process_action(fatal=True, fatal_reason="뇌 용량을 초과하여 머리에서 연기가 나며 두개골이 폭발했습니다.", fatal_title="오버클럭")
            if st.button("선생님에게 유리수의 정의에 대해 딴지를 건다", key="st_2"): process_action(fatal=True, fatal_reason="감히 스승에게 말대꾸를 한 죄로 분필 수백 개가 머리에 박혀 고슴도치가 되었습니다.", fatal_title="예절 주입기")
            if st.button("차분하게 제곱근을 정리하고 무리수를 분간한다", key="st_3"): process_action(next_stage='study_exam')

        elif st.session_state.stage == 'study_exam':
            st.subheader("갑자기 기습 시험이 시작되었습니다.")
            if st.button("답안지에 오직 '정답' 이라고만 적는다", key="ste_1"): process_action(fatal=True, fatal_reason="선생님이 어이가 없어서 던진 삼각자에 경동맥이 베여 출혈사했습니다.", fatal_title="기하학적 살인")
            if st.button("수학의 원리를 깨달아 10분 만에 만점을 받는다", key="ste_2"): process_action(is_ending=True, win_msg="가오카오 만점으로 칭화대 수학과에 수석 입학했습니다.", win_title="엔딩: 필즈상 후보")

        # --- 취업 루트 ---
        elif st.session_state.stage == 'job_start':
            st.subheader("어떤 일을 해볼까요?")
            if st.button("배달 대행 (오토바이)", key="j_1"): process_action(next_stage='job_delivery')
            if st.button("탕후루 가게 알바", key="j_2"): process_action(next_stage='job_tanghulu')
            if st.button("아이폰 조립 공장", key="j_3"): process_action(next_stage='job_factory')

        elif st.session_state.stage == 'job_factory':
            st.subheader("하루 16시간씩 나사를 조이는 공장입니다.")
            if st.button("성실하게 나사를 조인다", key="jf_1"): process_action(fatal=True, fatal_reason="과로사로 기계 위로 쓰러져 스마트폰 부품과 함께 압착되었습니다.", fatal_title="산업 혁명")
            if st.button("나사를 몰래 빼돌려 당근마켓에 판다", key="jf_2"): process_action(fatal=True, fatal_reason="보안 요원에게 걸려 쥐도새도 모르게 용광로에 던져졌습니다.", fatal_title="완전 범죄 실패")

        # --- 마라탕 루트 확장 ---
        elif st.session_state.stage == 'eat_start':
            st.subheader("마라탕 식당에 도착했습니다. 재료를 고르세요.")
            if st.button("푸주, 건두부, 옥수수면만 가득 담는다", key="ea_1"): process_action(next_stage='eat_spicy')
            if st.button("고수만 3kg 담는다", key="ea_2"): process_action(fatal=True, fatal_reason="고수 냄새에 질식한 옆 테이블 손님이 던진 의자에 맞아 죽었습니다.", fatal_title="향채의 저주")
            if st.button("알 수 없는 보라색 버섯을 담는다", key="ea_3"): process_action(fatal=True, fatal_reason="환각 버섯이었습니다. 당신은 하늘을 나는 상상을 하며 창문 밖으로 뛰어내렸습니다.", fatal_title="슈퍼 마리오")

        elif st.session_state.stage == 'eat_spicy':
            st.subheader("맵기 단계를 선택하세요.")
            if st.button("백탕", key="es_1"): process_action(fatal=True, fatal_reason="마라탕집에서 백탕을 시킨 죄로 주방장의 중식도에 썰렸습니다.", fatal_title="사문난적")
            if st.button("미친맛 5단계", key="es_2"): process_action(fatal=True, fatal_reason="위장에 구멍이 뚫려 내장탕이 되어버렸습니다.", fatal_title="위장 브레이커")
            if st.button("적당한 2단계", key="es_3"): process_action(is_ending=True, win_msg="완벽한 마라의 맛을 깨닫고 미식가로 거듭났습니다.", win_title="엔딩: 고독한 미식가")

    st.markdown('</div>', unsafe_allow_html=True)
