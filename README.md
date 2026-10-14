# Boiler Tray

Purdue dining court 음식(Earhart, Ford, Hillenbrand, Wiley, Windsor)을 탭해서 칼로리와 영양소를 하루 합계로 계산하는 웹앱이에요. 매일 아침 GitHub가 새 메뉴를 자동으로 받아 와요.

## 처음 한 번만 설정하기 (약 5분)

1. github.com에서 로그인하고 새 저장소(repository)를 만들어요. 이름은 `boiler-tray`처럼 아무거나 괜찮고, Public으로 만들어요.
2. 이 폴더의 파일을 전부 저장소에 올려요. `.github/workflows/daily-menu.yml` 파일도 같은 경로로 올라가야 해요. 저장소 화면에서 "Add file → Upload files"로 폴더째 끌어다 놓으면 돼요.
3. 저장소의 **Settings → Actions → General**에서 "Workflow permissions"를 **Read and write permissions**로 바꾸고 저장해요.
4. 저장소의 **Actions** 탭에서 "Update Purdue menu"를 열고 **Run workflow**를 눌러요. 1분쯤 뒤 `menu.json`이 생기면 성공이에요.
5. **Settings → Pages**에서 Source를 "Deploy from a branch", Branch를 `main` / `(root)`로 정하고 저장해요. 잠시 뒤 `https://<내 아이디>.github.io/boiler-tray/` 주소가 생겨요.
6. 그 주소를 폰에서 열고, 브라우저 메뉴의 "홈 화면에 추가"를 하면 앱처럼 쓸 수 있어요.

이후에는 매일 오전 5시쯤(미국 동부 여름시간 기준) 자동으로 메뉴가 갱신돼요. 앱을 열 때마다 최신 `menu.json`을 읽어요.

## 파일 설명

- `index.html`: 앱 본체예요.
- `purdue_menu.py`: Purdue 공개 메뉴 서버에서 오늘 메뉴와 영양 정보를 받아 `menu.json`으로 저장해요. 컴퓨터에서 `python3 purdue_menu.py`로 직접 실행해도 돼요.
- `.github/workflows/daily-menu.yml`: 위 스크립트를 매일 실행하는 설정이에요.

## 참고

- 영양 정보가 없는 메뉴(샐러드바 등 직접 담는 항목)는 목록에서 빠져요. 그런 음식은 앱의 "직접 추가"로 넣어 주세요.
- 수치는 1회 제공량 기준이에요. 실제로 담은 양과 다르면 수량(×0.5, ×1.5 등)을 조절하세요.
- 이 앱은 대략적인 기록용이에요. 식사나 건강 관련 결정은 필요하면 의료진이나 영양사와 상의하세요.
