---
name: pixelmood
description: "GeekMagic SmallTV Ultra (240x240 Wi-Fi 픽셀 디스플레이)에 Claude Code 감정 상태 자동 표시 설정. /pixelmood setup으로 초기 설정, /pixelmood status로 현재 상태 확인. SmallTV Ultra pixel display emotion display setup for Claude Code."
---

# PixelMood — SmallTV Ultra × Claude Code

GeekMagic SmallTV Ultra(AliExpress ~9,000원짜리 240x240 Wi-Fi 디스플레이)에 Claude Code의 현재 상태를 자동으로 표시합니다.

대화 중엔 CHAT, 파일 읽을 땐 SEARCHING, 코드 실행 중엔 WORKING, 완료되면 NICE! — 기기가 자동으로 전환됩니다.

## 지원 디바이스

- **GeekMagic SmallTV Ultra** (펌웨어 Ultra-V9.x+)
- Wi-Fi 2.4GHz 연결 필수 (5GHz 미지원)
- 구매: AliExpress "SmallTV Ultra" 검색

## 감정 이미지 목록 (10가지)

| 파일명 | 표시 상황 |
|--------|----------|
| `chat.jpg` | 사용자 메시지 수신 |
| `thinking.jpg` | Agent 실행 중 |
| `searching.jpg` | 파일 읽기/검색/웹 검색 |
| `working.jpg` | Bash 실행 / 파일 쓰기 |
| `done.jpg` | 도구 실행 완료 |
| `nice.jpg` | Claude 응답 완료 |
| `error.jpg` | 오류 발생 시 수동 사용 |
| `question.jpg` | Yes/No 질문 시 수동 사용 |
| `idea.jpg` | 아이디어 제안 시 수동 사용 |
| `careful.jpg` | 주의 필요 시 수동 사용 |

## 설정 방법 (/pixelmood setup)

사용자가 `/pixelmood` 또는 `/pixelmood setup`을 입력하면 아래 단계를 실행하세요.

### Step 1: 전제 조건 확인

```bash
python3 -c "from PIL import Image; print('Pillow OK')" 2>&1
```

Pillow가 없으면: `pip3 install Pillow`

### Step 2: 디바이스 IP 확인

사용자에게 SmallTV Ultra의 IP 주소를 물어보세요.
- 기기 웹 콘솔: 기기를 Wi-Fi에 연결한 후 라우터에서 IP 확인
- 기기가 보내는 IP 주소 (192.168.x.x 형태)

연결 테스트:
```bash
curl -s --compressed http://<IP>/ | head -5
```

`<!Doctype html>` 응답이 오면 연결 성공.

### Step 3: 감정 이미지 생성

플러그인의 `scripts/generate_images.py`를 사용하거나, 아래 코드를 직접 실행하세요:

```bash
python3 "$(find ~/.claude -name 'generate_images.py' -path '*/pixelmood*' 2>/dev/null | head -1)" --output /tmp/pixelmood
```

스크립트를 찾지 못하면 `/tmp/generate_pixelmood.py`에 직접 작성 후 실행:
```bash
python3 /tmp/generate_pixelmood.py --output /tmp/pixelmood
```

### Step 4: 기기 저장 공간 확인 및 기존 이미지 정리

```bash
# 여유 공간 확인
curl -s "http://<IP>/space.json"

# 여유 공간이 500KB 미만이면 기존 이미지 전체 삭제 (사용자 확인 후)
curl -s "http://<IP>/set?clear=image"
```

### Step 5: 이미지 업로드

```bash
for emotion in thinking working done nice error question searching idea careful chat; do
  result=$(curl -s -o /dev/null -w "%{http_code}" -X POST "http://<IP>/doUpload?dir=/image/" \
    -F "file=@/tmp/pixelmood/${emotion}.jpg;type=image/jpeg")
  echo "$emotion: $result"
done
```

모든 항목이 `200`이면 성공.

### Step 6: 앨범 테마로 전환 및 테스트

```bash
# 앨범 모드로 전환
curl -s "http://<IP>/set?theme=3"

# chat 이미지 표시 테스트
curl -s "http://<IP>/set?img=%2Fimage%2F%2Fchat.jpg"
```

### Step 7: 제어 스크립트 생성

`~/smalltv.sh`를 생성하세요:

```bash
cat > ~/smalltv.sh << 'SCRIPT'
#!/bin/bash
# PixelMood — SmallTV Ultra 감정 전환 스크립트
# 사용법: ~/smalltv.sh <emotion>

DEVICE="http://<IP>"
EMOTION="${1:-chat}"
VALID="thinking working done nice error question searching idea careful chat"

if [[ ! " $VALID " =~ " $EMOTION " ]]; then
  echo "지원 감정: $VALID"
  exit 1
fi

ENCODED=$(python3 -c "import urllib.parse; print(urllib.parse.quote('/image//$EMOTION.jpg'))")
curl -s "$DEVICE/set?img=$ENCODED" > /dev/null
SCRIPT

chmod +x ~/smalltv.sh
```

**중요**: `<IP>`를 실제 기기 IP로 교체하세요.

### Step 8: Claude Code Hooks 설정

`~/.claude/settings.json`의 `hooks` 섹션에 아래 항목을 **병합**하세요 (기존 hooks 유지):

**UserPromptSubmit** 에 추가:
```json
{
  "hooks": [{"type": "command", "command": "~/smalltv.sh chat", "async": true}]
}
```

**PreToolUse** 에 추가:
```json
{"matcher": "Bash", "hooks": [{"type": "command", "command": "~/smalltv.sh working", "async": true}]},
{"matcher": "Read|Glob|Grep", "hooks": [{"type": "command", "command": "~/smalltv.sh searching", "async": true}]},
{"matcher": "Write|Edit", "hooks": [{"type": "command", "command": "~/smalltv.sh working", "async": true}]},
{"matcher": "Agent", "hooks": [{"type": "command", "command": "~/smalltv.sh thinking", "async": true}]},
{"matcher": "WebFetch|WebSearch", "hooks": [{"type": "command", "command": "~/smalltv.sh searching", "async": true}]}
```

**PostToolUse** 에 추가 (없으면 새로 생성):
```json
{"hooks": [{"type": "command", "command": "~/smalltv.sh done", "async": true}]}
```

**Stop** 에 추가:
```json
{"hooks": [{"type": "command", "command": "~/smalltv.sh nice", "async": true}]}
```

settings.json 수정 후 JSON 유효성 검사:
```bash
jq '.' ~/.claude/settings.json > /dev/null && echo "JSON OK" || echo "JSON ERROR"
```

### 설정 완료

설정이 완료되면 사용자에게 알려주세요:
- 기기 IP, 업로드한 이미지 수, hooks 적용 여부
- 다음 메시지부터 자동 전환 시작

## 상태 확인 (/pixelmood status)

```bash
# 스크립트 존재 확인
ls -la ~/smalltv.sh 2>/dev/null && echo "Script: OK" || echo "Script: NOT FOUND"

# 현재 기기 IP 추출
IP=$(grep -o 'http://[0-9.]*' ~/smalltv.sh 2>/dev/null | head -1)
echo "Device IP: $IP"

# 기기 연결 확인
[ -n "$IP" ] && curl -s "$IP/v.json" || echo "Device: OFFLINE"

# hooks 확인
jq '.hooks.PostToolUse' ~/.claude/settings.json 2>/dev/null
```

## 수동 이미지 전환

언제든지 수동으로 이미지 전환 가능:
```bash
~/smalltv.sh error     # 에러 표시
~/smalltv.sh question  # Yes/No 질문
~/smalltv.sh idea      # 아이디어 제안
~/smalltv.sh careful   # 주의 필요
```

## 이미지 커스터마이징

`scripts/generate_images.py`를 수정하여 색상/텍스트 변경 가능:
- `EMOTIONS` 리스트에서 `bg`(배경색), `accent`(강조색), `label`(텍스트) 수정
- 수정 후 재생성 및 재업로드 필요

## 알려진 제한사항

- SmallTV Ultra 저장 공간: ~3MB (이미지 최대 약 20개)
- Wi-Fi 2.4GHz만 지원 (5GHz 미지원)
- 기기가 같은 Wi-Fi에 연결되어 있어야 함
- macOS 전용 (Helvetica 폰트 사용)
