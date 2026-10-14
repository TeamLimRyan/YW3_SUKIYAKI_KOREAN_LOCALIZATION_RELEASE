# 요괴워치3 스키야키 한국어 패치 v0.9

## 무단 추출 및 재배포 금지

본 패치에 포함된 번역문, 한글화 이미지, 수정된 리소스 및 기타 제작 결과물을 제작팀의 사전 허가 없이 추출하여 별도로 배포하거나, 다른 패치·프로젝트·자료에 재사용하는 행위를 금지합니다.

패치 파일 전체 또는 일부를 임의로 재패키징·재업로드·미러링하여 배포하는 행위 역시 허용하지 않습니다.

CIA, ROM, 키, 펌웨어, 원본 게임 데이터는 포함하지 않습니다.

## 대상과 범위

일본판 요괴워치3 스키야키 본편 v0 복호화 CCI와 Update 4.0 복호화 CIA를 대상으로 합니다. 아래 SHA-256과 정확히 같은 사용자 소유 원본 두 파일이 필요하며 두 패치를 모두 적용해야 합니다. 다른 버전이나 암호화 파일은 지원하지 않습니다.

한국어 텍스트·폰트·조합식 이름 입력·수수께끼 정답과 한국어 이미지 2,076개를 포함합니다. 이미지 목록 25,286개 중 23,210개는 교체하지 않았습니다(원본 유지 10,254개, 한국어 결과 없음 12,956개). 목록에는 글자가 없는 이미지도 포함됩니다. 작업 중이거나 원본을 유지한 이미지의 일본어는 그대로 남습니다. 전자 설명서는 3DS 시스템 폰트에 한글이 없어 일본어를 유지합니다. 이름의 띄어쓰기는 반각 공백을 사용합니다. 일부 긴 문장은 정적 폭 검사에서 경고가 있으며 실제 화면 잘림 여부는 확정되지 않았습니다.

## 입력·패치·결과

파일명만으로 원본을 판단하지 말고 SHA-256을 대조하십시오. 결과 CCI/CIA는 패키지에 포함되지 않으며 원본에 패치를 적용하면 생성됩니다.

| 역할 | 파일 | 바이트 | SHA-256 |
|---|---|---:|---|
| base 원본 | Youkai Watch 3 - Sukiyaki (Japan)-decrypted.cci | 3270860800 | d98a9430f3edc0b25fc1a4e0d147d0b976db1b0bdce8e042c50f0e84a738f4d8 |
| base 패치 | YW3_Sukiyaki_KO_base_v0.9.xdelta | 76474858 | 365c6bb4c70d8cabfc4f94ae7692da1676eee359548d92e491d164c496e2869b |
| base 결과 | YW3_Sukiyaki_KO_base.cci | 3278712832 | d0dc26b3e00c14bc322e5b02ac26a5d08996f50c92d2f2ad2abdb426cf402f2e |
| update 원본 | Youkai Watch 3 - Sukiyaki Update v4.0 (Japan) (Patch)-decrypted.cia | 196408320 | 95d5e28eb4920a68bfc3c0ae407a308ddc06a11ab229da3d28cfa4976af58082 |
| update 패치 | YW3_Sukiyaki_KO_update_v0.9.xdelta | 12287076 | e25a443c6b98f9558429299588ee35ef88158a81b3739a8431e0ffbcbdb98847 |
| update 결과 | YW3_Sukiyaki_KO_update4.cia | 196301824 | 73adda215b3c929cca7cb0d544b686957ca7c4e2d354a77d9f342924d7a35453 |

manifest.json에도 같은 파일 크기와 SHA-256이 있습니다. SHA256SUMS.txt는 그 파일 자체를 제외한 패키지 전체 파일의 SHA-256 목록입니다.

## Windows 적용

1. 원본 두 파일을 보존하고 결과를 저장할 새 폴더를 만듭니다. 적용 시 약 7GB 이상의 여유 공간을 권장합니다.
2. 공식 [xdelta3 3.2.2 Windows x64 배포본](https://github.com/jmacd/xdelta/releases/download/v3.2.2/xdelta3-3.2.2-windows-x86_64.zip)을 받습니다.
   ZIP SHA-256: d48f7651d86b78fdca397057b46601f89131f37219675df736db70af44ec3379
   xdelta3.exe SHA-256: 732980d52f9220dc81817ccdd0c295eadce8a0048a24c2a771a73f791ac824e9
3. PowerShell에서 패키지 폴더로 이동한 뒤, 실제 원본·도구 경로로 바꿔 아래를 실행합니다. 스크립트는 원본·패치·도구 해시를 검사한 뒤 결과 해시를 검사하며 기존 결과 파일을 덮어쓰지 않습니다.

    .\Apply-Patch.ps1 -Role base -Source ".\Youkai Watch 3 - Sukiyaki (Japan)-decrypted.cci" -Output ".\YW3_Sukiyaki_KO_base.cci" -Xdelta ".\xdelta3.exe"

    .\Apply-Patch.ps1 -Role update -Source ".\Youkai Watch 3 - Sukiyaki Update v4.0 (Japan) (Patch)-decrypted.cia" -Output ".\YW3_Sukiyaki_KO_update4.cia" -Xdelta ".\xdelta3.exe"

직접 명령줄로 적용할 때도 **전후 SHA-256 확인이 필수**입니다.

    xdelta3 -d -s "Youkai Watch 3 - Sukiyaki (Japan)-decrypted.cci" "YW3_Sukiyaki_KO_base_v0.9.xdelta" "YW3_Sukiyaki_KO_base.cci"

    xdelta3 -d -s "Youkai Watch 3 - Sukiyaki Update v4.0 (Japan) (Patch)-decrypted.cia" "YW3_Sukiyaki_KO_update_v0.9.xdelta" "YW3_Sukiyaki_KO_update4.cia"

Windows xdelta UI 또는 Delta Patcher에서는 원본(Source/Original file), 해당 역할의 패치(Patch), 새 결과(Output)를 각각 선택해 두 번 적용합니다. GUI 자체는 이번 작업에서 실행 검증하지 않았습니다. 표준 VCDIFF 스트림이며 응용 헤더·추가 압축·신형 armor를 사용하지 않습니다. GUI가 거부하면 위 공식 CLI를 사용합니다.
PowerShell의 Get-FileHash -LiteralPath "파일 경로" -Algorithm SHA256으로 표와 대조하십시오. xdelta 창 체크섬은 참조하지 않은 원본 영역의 변화를 놓칠 수 있어 명령 성공만으로 전체 원본 일치를 판단하면 안 됩니다. 체크섬 오류를 무시하는 옵션은 사용하지 마십시오.

## 설치와 제거

Azahar 포터블에서는 OpenGL 렌더러를 사용하고, 생성한 Update CIA를 설치한 뒤 생성한 본편 CCI를 실행합니다. 예전 LayeredFS 모드·code.ips·icon override·RomFS sidecar가 겹치지 않는 별도 포터블 사용자 폴더를 사용하십시오. 필요한 아카이브·코드·제목 정보는 컨테이너 안에 포함되어 별도 모드 파일 복사가 필요 없습니다. 한쪽만 패치하면 번역이 누락됩니다.

실기 3DS에서는 해당 기기의 복호화·변경 콘텐츠 지원 환경과 설치 도구 절차에 따라 적용합니다. 본편 결과는 CCI, 업데이트 결과는 CIA입니다. CCI를 CIA 설치 파일처럼 취급하지 마십시오. 기기용 본편 변환·설치 도구는 이 패키지에 포함하지 않습니다. 정품 디지털 서명은 재생성하지 않았으며 변경 콘텐츠의 해시 일치와 서명 유효성은 다릅니다. 순정 3DS용 정식 서명 배포물이 아닙니다.

제거할 때는 필요한 세이브를 먼저 보관하고 한글 업데이트를 제거한 뒤 같은 원본 Update 4.0과 원본 본편으로 되돌립니다. 세이브 호환성·하위 버전 복원 안전성은 별도 확인이 필요합니다.

## 검증 범위

제작팀 제공 확인:

에뮬레이터(Azahar)와 실기 3DS에서 검증을 완료했습니다.

패키지 제작 과정에서는 에뮬레이터를 새로 실행하지 않고 정적 검증을 수행했습니다. 본편·업데이트 패치 왕복 SHA-256 일치 2건, 손상 원본·잘못된 컨테이너 거부 4건, 적용 스크립트 정상/거부 검사 2건을 통과했습니다. RomFS 파일 5,315개(교체 아카이브 2개, 불변 파일 5,313개), ExeFS·NCCH·IVFC·TMD 내용 해시와 별도 도구의 IVFC 검증을 통과했습니다.

한국어 이미지 2,076개의 발생 위치 2,157곳을 포함한 빌드 재디코드 검증에서 기대 픽셀 불일치는 0입니다. 기대 픽셀은 원본 픽셀 형식으로 변환한 결과이며 PNG 원본과의 무손실 일치를 뜻하지 않습니다. 같은 별명 검사 코드의 한글·영문 별명 저장·재로드 2건은 유지됨을 확인했습니다. 전체 플레이 경로와 모든 장면을 관찰했다는 뜻은 아닙니다.

패키지 원본·완성 게임 파일, 키·세이브·토큰·개인 경로 검사는 발견 0건입니다. 패치 추가 데이터와 원본의 4KiB 중복 표본 검사도 발견 0건입니다. 짧거나 정렬이 다른 원본 유래 바이트가 전혀 없다는 증명은 아닙니다.

## 권리와 문의

게임·상표·원본 자산의 권리는 각 권리자에게 있습니다. 제작 결과물 사용 조건은 위 고지와 LICENSES.md를 따릅니다. xdelta3 라이선스는 LICENSE-xdelta3.txt에 있습니다.
문제는 이 패치를 받은 제작팀 배포처로 알려 주십시오. 패치 버전, 원본·패치·결과 SHA-256, 도구 버전, 사용 환경, 재현 단계와 개인정보를 지운 화면을 포함하고 게임 원본·키·세이브 전체는 보내지 마십시오.
