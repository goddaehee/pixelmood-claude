# PixelMood — SmallTV Ultra × Claude Code

> Claude Code와 대화하는 동안 GeekMagic SmallTV Ultra 픽셀 디스플레이에 감정 상태가 자동으로 표시됩니다.

[![Claude Code Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-orange)](https://github.com/goddaehee/pixelmood-claude)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

![PixelMood Demo](https://github.com/goddaehee/pixelmood-claude/raw/main/assets/demo.jpg)

## 어떻게 동작하나요?

| Claude 상태 | 디스플레이 |
|------------|-----------|
| 메시지 받을 때 | 💬 CHAT |
| 파일 읽기/검색 | 🔍 ANALYZING... |
| 코드 실행 중 | ⚙️ WORKING... |
| Agent 실행 중 | 🤔 THINKING |
| 도구 완료 | ✅ DONE! |
| 응답 완료 | 😊 NICE! |

## 지원 디바이스

**GeekMagic SmallTV Ultra** — AliExpress에서 약 9,000원

- 240×240 픽셀 컬러 디스플레이
- Wi-Fi 2.4GHz 내장
- 내장 웹 서버 (HTTP API)

## 설치 방법

### 1. Claude Code에 플러그인 등록

> **전역 설정 권장**: SmallTV는 물리적 디바이스이므로 프로젝트와 무관하게 항상 동작해야 합니다.
> `~/.claude/settings.json`(전역)에 추가하세요. 특정 프로젝트에서만 사용하려면 `.claude/settings.json`에 추가하면 됩니다.

`~/.claude/settings.json`에 추가:

```json
{
  "extraKnownMarketplaces": {
    "pixelmood": {
      "source": {
        "source": "github",
        "repo": "goddaehee/pixelmood-claude"
      }
    }
  },
  "enabledPlugins": {
    "pixelmood-claude@pixelmood": true
  }
}
```

### 2. 설정 실행

Claude Code에서:

```
/pixelmood
```

대화형 설정 마법사가 시작됩니다. SmallTV Ultra의 IP 주소만 알면 됩니다.

### 3. 완료!

다음 대화부터 자동으로 감정 이미지가 전환됩니다.

## 전제 조건

- macOS (Helvetica 폰트 필요)
- Python 3 + Pillow (`pip3 install Pillow`)
- SmallTV Ultra가 같은 Wi-Fi에 연결되어 있을 것

## 수동 제어

```bash
~/smalltv.sh error     # 에러 표시
~/smalltv.sh question  # Yes/No 질문
~/smalltv.sh idea      # 아이디어 제안
~/smalltv.sh careful   # 주의 필요
```

## 파일 구조

```
pixelmood-claude/
├── .claude-plugin/
│   ├── marketplace.json
│   └── plugin.json
├── skills/
│   └── pixelmood/
│       └── SKILL.md       # /pixelmood 스킬 정의
├── scripts/
│   └── generate_images.py # 감정 이미지 생성기
└── README.md
```

## 라이선스

MIT License — [goddaehee](https://github.com/goddaehee)
