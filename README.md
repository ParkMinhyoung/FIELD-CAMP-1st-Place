# FIELD-CAMP-1st-Place


## 🏆 [2026 FIELD CAMP 최우수상] 기상-발전 데이터 관계 추론 기반 풍력 발전량 예측 및 AI 데이터센터 입지 최적화

### 🚀 AI 데이터센터 최적 입지 선정 및 풍력 발전량 기반 ESS 운영 파이프라인


본 프로젝트는 <b>SCADA 및 기상 데이터를 활용한 풍력 발전량 예측(Phase 2)</b>과 <b>예측된 풍력 잉여전력을 연계한 경주시 AI 데이터센터 최적 입지 선정 및 ESS(에너지저장장치) 용량 최적화(Phase 3)</b>를 통합한 End-to-End 에너지-데이터센터 최적화 파이프라인입니다.

### 👥 Role & Business Impact


* **팀 구성**: 2026 FIELD CAMP 14B조 (8명) / **대상(1st Place) 수상**[cite: 1]

* **핵심 기여**:

  * **Phase 1**: 물리 법칙($P \propto p/T$) 기반 기온·기압 파생변수 및 나셀 풍속/풍향 데이터 재식별

  * **Phase 2**: LightGBM 구축, 3-Fold Walk-forward CV 검증, 정비/저온 도메인 피처 설계를 통한 NMAE 0.0934 달성

  * **Phase 3**: Gurobi 2-Stage 최적화 모델 구축 및 ESS 예산 민감도 시뮬레이션 설계


* **Business Impact**:

  * **계통 안정화**: 출력제어(Curtailment) 전력을 AI 데이터센터와 ESS로 흡수하여 제주/영남권 전력망 주파수 변동성 완화

  * **투자 효율성 도출**: 100억 원 예산 조건 하에서 80MW 최대 수용 용량을 도출하고, 20억 원 추가 투자가 가져오는 +20MW 확장성 입증


---

## 📋 Table of Contents


- [1. 프로젝트 개요](#1-프로젝트-개요)

- [2. 기술 스택](#2-기술-스택)

- [3. 디렉토리 구조](#3-디렉토리-구조)

- [4. 파이프라인 상세](#4-파이프라인-상세)

  - [Phase 1: 물리 법칙 기반 데이터 역추적 및 마스킹 컬럼 재식별](#%EF%B8%8F-phase-1--task-1--물리-법칙-기반-데이터-역추적-및-마스킹-컬럼-재식별)

  - [Phase 2: 풍력 발전량 예측 모델링](#%EF%B8%8F-phase-2-풍력-발전량-예측-모델링)

  - [Phase 3: AI 데이터센터 입지 및 ESS 최적화](#%EF%B8%8F-phase-3-ai-데이터센터-입지-및-ess-최적화)

- [5. 핵심 분석 인사이트 & Lessons Learned](#5-핵심-분석-인사이트--lessons-learned)

- [6. 환경 설정 및 실행 방법](#6-환경-설정-및-실행-방법)

- [7. Contact](#7-contact)

---

## 1. 프로젝트 개요


* **프로젝트명**: AI 데이터센터 입지 최적화 및 풍력 발전량 기반 ESS 운영 파이프라인

* **주요 목적**:

  * **Phase 1**: 물리 법칙(이상기체 방정식, Betz's Law 등)을 적용하여 익명화된 SCADA 및 기상 데이터를 역추적하고 핵심 피처를 재식별.

  * **Phase 2**: SCADA 센서 데이터 및 환경 변수를 활용하여 12월 10분 단위 유효전력생산량(kWh)을 고도화된 머신러닝 모델로 예측.

  * **Phase 3**: 예측된 풍력 잉여전력 프로파일을 바탕으로 경주시 내 최적 부지를 선정하고, Gurobi 수리 최적화를 통해 AI 데이터센터 전력 충당을 위한 ESS 용량을 산정.


📄 **[FIELD CAMP 최우수상 최종 발표자료 (PDF) 바로보기](./FIELD_CAMP_1st_Place_Presentation.pdf)**


**✨ Key Achievements**

- 실증 테스트 기준 **NMAE 0.0934** 달성 (v6 모델 채택)

- AI 데이터센터 전력 충당률 극대화를 위한 **ESS 최적 용량 산정 및 부지 도출**

  
---


## 2. 기술 스택


| 구 분 | 기술 / 라이브러리 |

| :--- | :--- |

| **언어** | Python 3.12+ |

| **데이터 처리** | Pandas, NumPy |

| **머신러닝 / 예측** | LightGBM, Optuna, Scikit-learn |

| **수리 최적화** | Gurobi (`gurobipy`) |

| **시각화** | Matplotlib, Seaborn |


---



## 3. 디렉토리 구조

```text

├── data/

│   ├── train(1월~11월).csv                # Phase 2 학습용 SCADA 데이터

│   ├── train(12월).csv                    # Phase 2 평가/예측 대상 데이터

│   ├── terrain_grid_100m.csv              # 경주시 100m x 100m 격자 데이터

│   ├── substation_locations.csv           # 변전소 위치 및 Capacity 데이터

│   └── gyeongju_boundary.csv              # 경주시 지리적 경계 데이터

├── Phase2_Task2_코드 파일_14B.ipynb        # Phase 2 풍력 발전량 예측 노트북

├── Phase3_최적화 코드 파일_14B.ipynb       # Phase 3 입지 및 ESS 최적화 노트북

├── outputs/

│   ├── Phase2_Task2_평가셋예측.csv         # Phase 2 최종 예측 결과

│   └── phase3_outputs/                    # Phase 3 최종 부지 리포트 및 시각화 그래프

└── README.md                              # 프로젝트 안내 문서

```

---


## 4. 파이프라인 상세


**📊 전체 파이프라인 흐름도**

```mermaid

flowchart LR

    subgraph Phase 1 [Phase 1: 물리 법칙 기반 데이터 역추적]

        direction TB

        A["SCADA 및 기상<br>블라인드 데이터"] --> B("물리 법칙 기반<br>데이터 역추적")

        B --> C("익명화 마스킹<br>컬럼 재식별")

    end



    subgraph Phase 2 [Phase 2: 풍력 발전량 예측]

        direction TB

        D("도메인 지식 기반<br>피처 엔지니어링") --> E("LightGBM 활용<br>발전량 예측 모델링")

        E --> F["12월 10분 단위<br>풍력 잉여전력 도출"]

    end



    subgraph Phase 3 [Phase 3: 입지 및 ESS 최적화]

        direction TB

        G("경주시 100m 격자 공간<br>필터링 및 후보지 도출") --> H("Gurobi Multi-Stage<br>최적화")

        H --> I["최적 AI 데이터센터<br>부지 선정 및 ESS 용량 산정"]

    end



    %% 서브그래프 간의 연결

    C --> D

    F --> G

```


#### ⚙️ Phase 1 & Task 1 : 물리 법칙 기반 데이터 역추적 및 마스킹 컬럼 재식별

* **물리 법칙 기반 데이터 역추적(Reversing)**:

  * **이상기체 방정식($P = \rho RT$)**: 기온 및 기압 블라인드 변수의 비선형 관계를 추론하여 대기 밀도(`air_density_calc`) 파생변수 생성.

  * **Betz's Law & 유효 풍속**: 나셀 풍속과 요 정렬 오차(`yaw_misalign`)를 결합하여 풍력 에너지 플럭스(`wind_power_flux`) 산출.

* **익명화(Masking) 컬럼 재식별**:

  * $\sin^2\theta + \cos^2\theta = 1$ 원형 패턴 분석을 통해 `Feature_10`, `Feature_15`를 풍향 sin/cos 벡터로 식별 및 각도(Degree) 복원.


### ⚙️ Phase 2: 풍력 발전량 예측 모델링


### 📊 Model Benchmark & Feature Iterations

**1) 모델별 Walk-forward 교차검증 성능 비교 (3-Fold Avg)**
| Model | Sept NMAE | Oct NMAE | Nov NMAE | Mean NMAE | 비고 |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **LightGBM (Final)** | **0.022** | **0.128** | **0.063** | **0.071** | **최종 단일 모델 채택** |
| Extra Trees | 0.043 | 0.123 | 0.108 | 0.092 | Hidden Stop 2-Stage 보정 |
| Random Forest | 0.027 | 0.133 | 0.134 | 0.099 | Expanding-Window 적용 |
| LSTM | 0.064 | 0.157 | 0.132 | 0.119 | Sequence Time-step 튜닝 |

* **앙상블 검증**: LightGBM(95%) + Extra Trees(5%) 조합 시 NMAE 0.0711로 단일 LightGBM(0.0714) 대비 개선폭이 0.0003에 불과하여 복잡도를 낮추고 재현성을 높이기 위해 **LightGBM 단독 모델** 채택.

**2) 도메인 피처 결합 단계별 Test NMAE (12월 실제 평가)**
| Version | Feature Engineering Strategy | Test NMAE | 비고 |
| :--- | :--- | :---: | :--- |
| **Baseline (v1)** | 기본 식별 변수만 적용 | 0.0944 | 초기 모델 |
| **v2 (Final)** | **정비주기(70일) + 저온(-10°C) 성능저하 피처** | **0.0934** | **최종 채택 (NMAE 21.91% → 9.34% 개선)** |
| v3 | 정비주기 + 저온(-7°C) 정밀 조정 | 0.0936 | 과적합 우려로 제외 |
| v4 | 정비주기 + 저온(-10°C) + 저기압/폭풍방향 | 0.0942 | 노이즈 증가로 성능 하락 |

1. **도메인 지식 기반 피처 식별 (Task 1)**

   - Phase 1에서 탐구한 풍력 발전 물리 법칙 및 기상(기온, 기압) 요인 분석 결과 활용.

   - 익명화(Masking)된 `Feature_1~18` 컬럼을 물리적 인과관계에 기반하여 나셀 풍속, 나셀 풍향(sin/cos), 기온, 기압, 로터 회전수 등으로 논리적 재식별.



2. **예측 모델링 및 대회 제약조건 반영 (Task 2)**

   - 1~11월 실측 데이터를 학습하여 12월 평가셋의 10분 단위 유효전력생산량 예측.

   - **대회 룰 준수**: 외부 데이터 결합을 일절 배제하고, 예측 시점의 설명 변수만 사용하는 엄격한 조건 하에 모델 설계.



3. **물리·시계열 피처 엔지니어링 (Feature Engineering)**

   - **물리 기반 파생변수**: 이상기체 상태방정식 기반 공기밀도(`air_density_calc`), Betz 이론 기반 풍력 에너지 플럭스(`wind_power_flux`), 요 정렬 오차(`yaw_misalign`) 및 유효 풍속 도출.

   - **시간/계절 순환 피처**: 외삽 위험을 차단하기 위해 연월일 단순 달력 변수를 제거하고 순환 인코딩(`hour_sin/cos`, `doy_sin/cos`) 적용.



4. **Data Leakage 차단 및 모델 검증 (Walk-forward CV)**

   - `op_switch`, `forced_stop_min` 등 과거 타겟값을 내포하거나 사후에만 알 수 있는 집계 컬럼을 원천 제외하여 Data Leakage 차단.

   - 시계열 구조에 맞춘 Walk-forward CV 검증 수행 및 최종 실증 평가셋(12월) 기준 **v6 모델 (NMAE 0.0934)** 최종 채택.



---  



### 🏛️ Phase 3: AI 데이터센터 입지 및 ESS 최적화



1. **후보지 생성 및 제약조건 (Candidate Generation)**

   - **격자 필터링**: 경주시 100m × 100m 격자(총 90,000개 셀) 대상 공간 필터링:

     - 경주시 행정구역 내부 영역

     - 경사도 15도 이하 안전 지형

     - 문화재 보호 구역 버퍼 외부

     - 3개 변전소(경주, 입실, 양북) 최소 안전 이격거리 2.07071km 이상 확보

   - **부지 형상 및 인구지표**: 30MW(3개 형상) 및 50MW(5개 형상) 직사각형 후보지 약 309,533개 생성. 인구 지표는 상대적 백분위 점수(`population_score`)로 정규화.



2. **풍력 잉여전력 프로파일 연계**

   - Phase 2 예측 결과(7기 풍력터빈 10분 단위 발전량) 기반 70% 잉여전력(MW) 프로파일 생성 및 최적화 연동.



3. **Gurobi 기반 Multi-Stage Optimization**

   - **Stage 1 (부지 최적 선정)**:

     - 예산 한도, 변전소 용량 제한, 송전선 설치 예산, 격자 중첩 방지 제약 반영.

     - 계층적 다목적 함수: 1순위 경사등급 최소화 → 2순위 송전선 비용 최소화 → 3순위 인구지표 백분위 최소화.

   - **Stage 2 (ESS 용량 산정 및 시뮬레이션)**:

     - AI 데이터센터 전력 충당률 극대화 및 미충당 전력 최소화를 위한 ESS 최적 용량 산정.

     - 예산 증설 시나리오별 수리적 시뮬레이션 수행.



### 📍 Phase 3: 입지 최적화 & ESS 예산 민감도 분석

**1) 최종 최적 입지 및 ESS 산출 결과 (총 budget 150,000억 원 / ESS budget 100억 원 기준)**
| 구분 | 30MW급 데이터센터 | 50MW급 데이터센터 | 최종 합계 / 특징 |
| :--- | :--- | :--- | :--- |
| **부지 ID** | `30_S30_063731` (2×5) | `50_S50_128054` (2×8) | **총 실현 용량: 80MW (최대화)** |
| **위도 / 경도** | 35.776604°N / 129.423590°E | 35.827895°N / 129.242502°E | 부지 간 중첩 없음 (이격 충족) |
| **연결 변전소** | 양북변전소 (2.39km) | 경주변전소 (2.14km) | **송전선 총비용: 45.35억 원** |
| **ESS 필요용량**| 16.098 MWh | 24.148 MWh | **총 ESS 용량: 40.246 MWh** |
| **ESS 설치비용**| 32.20억 원 | 48.29억 원 | **총 ESS 비용: 80.49억 원 (19.51억 절감)** |

* **타당성 검증**: 농업용수 수요(농경지 밀집도)를 목적함수에 추가 반영하여 최적화를 재수행한 결과, 기존 최적 부지와 동일한 입지가 도출되어 시뮬레이션의 높은 견고성을 검증함.

**2) ESS 예산 증설 시뮬레이션 (Sensitivity Analysis)**
| ESS 예산 | 최대 실현 용량 | 최적 규모 조합 | 필요 ESS 용량 | 총 ESS 비용 | 비고 |
| :---: | :---: | :--- | :---: | :---: | :--- |
| **100억 원** | **80MW** | **30MW 1기 + 50MW 1기** | **40.246 MWh** | **80.49억 원** | **현재 기준** |
| **120억 원** | **100MW** | **50MW 2기** | **55.740 MWh** | **111.48억 원** | **최고 가성비 구간 (+20MW 확장)** |
| 150억 원 | 100MW | 50MW 2기 | 55.740 MWh | 111.48억 원 | 용량 정체 구간 |
| 200억 원 | 110MW | 30MW 2기 + 50MW 1기 | 76.858 MWh | 153.72억 원 | 추가 송전선 비용 발생 |

> **Key Insight**: 입지 확장을 제약하는 핵심 병목은 **ESS 예산**이며, ESS 예산을 **20억 원 증액(120억 원 확보)**할 때 용량이 80MW에서 100MW로 늘어나 한계 효용이 가장 극대화됩니다.

---



## 5. 핵심 분석 인사이트 & Lessons Learned



1. **Leakage 컬럼의 역발상 활용 (EDA/기초 분석)**

   - `강제정지시간(분)` 등 사후 데이터는 예측 피처로 직접 사용할 경우 Data Leakage가 발생하지만, **탐색적 분석(EDA)의 타깃**으로 활용하여 저기압 threshold 및 특정 남-남서풍 폭풍 방향 등의 물리적 특성을 추정하는 핵심 열쇠로 활용함.

2. **CV 점수와 Test NMAE 간의 괴리 대응**

   - 겨울철 데이터 부재로 인해 단순 CV 점수에만 의존할 경우 오버피팅 발생 위험 확인. 실증 테스트 NMAE를 지속 점검하여 과도한 복잡도를 가진 v9 모델 대신 일반화 성능이 뛰어난 v6 모델을 선별 채택함.



---


## 6. 🛠️ 환경 설정 및 실행 방법 (How to Run)

> [!NOTE]
> 본 프로젝트는 **Python 3.12+** 및 **Gurobi Optimizer** (Academic / Commercial License) 환경에서 작성되었습니다.

---

### 💻 1. 설치 및 환경 구축 (Installation)

터미널(Cmd 또는 Git Bash)에서 아래 명령어를 순서대로 실행합니다.

```bash
# 1. 리포지토리 클론 & 폴더 이동
git clone [https://github.com/ParkMinhyoung/FIELD-CAMP-1st-Place.git](https://github.com/ParkMinhyoung/FIELD-CAMP-1st-Place.git)
cd FIELD-CAMP-1st-Place

# 2. 필요 패키지 일괄 설치
pip install pandas numpy lightgbm optuna scikit-learn gurobipy matplotlib seaborn jupyter
```

---
### 🚀 2. 파이프라인 실행 가이드 (Execution Pipeline)

> **💡 Tip**: 실행 파일명 링크를 클릭하면 해당 주피터 노트북 코드로 이동합니다.

| 단계 | 주요 과제 | 실행 파일 (`.ipynb`) | 필요 입력 데이터 | 최종 출력 결과물 |
| :---: | :--- | :--- | :--- | :--- |
| **Phase 2** | **풍력 발전량 예측** | 📄 [`Phase2_Task2_코드 파일_14B.ipynb`](./Phase2_Task2_코드%20파일_14B.ipynb) | `train(1월~11월).csv`<br>`train(12월).csv` | 12월 10분 단위 유효전력생산량 예측 CSV |
| **Phase 3** | **입지 & ESS 최적화** | 📄 [`Phase3_최적화 코드 파일_14B.ipynb`](./Phase3_최적화%20코드%20파일_14B.ipynb) | `terrain_grid_100m.csv`<br>`substation_locations.csv`<br>`gyeongju_boundary.csv` | AI 데이터센터 최적 부지 리포트 & ESS 시뮬레이션 |


### 🖥️ 3. CLI 터미널 실행 (선택 사항)

주피터 UI 없이 터미널(cmd)에서 명령어로 직접 자동 실행할 때 사용합니다.

```bash
# Phase 2 노트북 커널 실행
jupyter nbconvert --to notebook --execute "Phase2_Task2_코드 파일_14B.ipynb"

# Phase 3 노트북 커널 실행
jupyter nbconvert --to notebook --execute "Phase3_최적화 코드 파일_14B.ipynb"

```
---



## 7. Contact

* **Email**: minhung0725@naver.com

* **GitHub**: [ParkMinhyoung](https://github.com/ParkMinhyoung)

  

---
