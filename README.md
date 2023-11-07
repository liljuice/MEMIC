# MEMIC

Django version>=3.0\
```
pip install pillow django-bootstrap4 pytube librosa soundfile pydub parselmouth spleeter
```

로컬 파일 올리기 > http://127.0.0.1:8000/fileupload <p>
유튜브 따오기 > http://127.0.0.1:8000/fileupload/youtube <p>
관리자 > http://127.0.0.1:8000/admin

--------

### 피드백 (임시 버전)
```
1. 전체 점수 제공 (MFCC)
2. 사용자에게 점수를 올리는 방법을 알려주는 보고서
     : 따라하려는 목소리(이하 피모사 음성)의 주요 Formant 구간(peak-picking)에 대해 사용자의 목소리(이하 사용자 음성)의 주파수 비교.
       차이가 극심한 1순위, 2순위, 3순위의 평가 지표에 대해 보고서를 제공함.
       해당 구간에 대해 컷팅된 음성 다시 듣기(피모사 음성, 사용자 음성)를 제공함.

                e.g.) /ㅂ/, /ㅃ/, /ㅍ/와 같은 폐쇄음의 발음에 집중하세요!
                      > 상세보기 (이유)
                        따라하려는 목소리에서는 1,000~2,400 Hz의 구간이 특징적입니다.
                        이 주파수는 ㅂ, ㅃ, ㅍ와 같은 폐쇄음 발음에 해당합니다.
                        해당하는 구간을 다시 한번 들어보고, 발음을 더 정확하게 해보세요.
                      > [피모사 음성 듣기] [사용자 음성 듣기]
                      > [다시 시도하기]

  * 평가 지표
  1) 음소 유형 : 모음 그룹, 자음 그룹(ㄴ,ㅁ,ㄹ / ㄱ,ㄲ,ㅋ,ㅂ,ㅃ,ㅍ,ㅎ / ㄷ,ㄸ,ㅌ,ㅈ,ㅉ,ㅊ,ㅅ,ㅆ)
                Formant 주파수의 차이가 큰 지점에 해당하는 음소 그룹에 대한 피드백 제공
                수치와 평가 근거 참고 문헌 - 한국어 음소의 주파수 특성에 관한 연구 https://www.e-asr.org/upload/pdf/asr-1-1-59.pdf

  2) 템포, 높낮이 : 서브 평가지표로 최대 3순위에 해당
```

--------

### 서버에 구현 된 기능

비디오/오디오 파일 업로드\
유튜브 링크 업로드\
비디오 -> 오디오 변환\
오디오 -> 데이터 변환\
녹음 API

--------

### 나머지 기능 (서버에 포함되지 않음)
MFCC 평가 알고리즘\
Formant 선별 알고리즘(DTW)

--------

### 구현 해야 할 기능
Formant 기준 평가 알고리즘\
오디오 높낮이 그래프\
오디오 Formant 그래프\
그래프 비교 기능
